import requests
from bs4 import BeautifulSoup as bs
import shutil
import os
import time
import csv
from io import BytesIO
from imageFilter import Image_judge
import multiprocessing
import pixiv3_cookie

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36'
          ,'Upgrade-Insecure-Requests':'1'
          ,'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
          ,'Accept-Encoding':'gzip, deflate, sdch, br'
          ,'Accept-Language':'zh-TW,zh;q=0.8,en-US;q=0.6,en;q=0.4'
          ,'Connection':'keep-alive'
          ,'Referer':'https://www.pixiv.net/ranking.php'}

csv_file = open("fail.csv","w")
w = csv.writer(csv_file)

def makedirs_create(path, folder):
    folder_month = folder.split('-')[1]
    #dirPath:所有子目錄, dirs:所有目錄下所包括的目錄, files:所有目錄及檔案
    if os.path.isdir(path):
        for dirPath, dirs, files in os.walk(path):
            for dir in dirs:
                dir_month = dir.split('-')[1]
                print("this month:%r" %(dir_month == folder_month))
                if(dir_month in folder_month):
                    return dir
    os.makedirs(r'%s/%s'%(path,folder))
    return folder
        

def file_data_create(mode, date_current):
    path = r"C:\Users\foryou\date_compare.xml"
    #folder_csv = time.strftime(r"%Y-%m-%d",time.gmtime(os.path.getmtime(file_csv)))
    if not(os.path.isfile(path)):
        open(path,"w")
        return None

    if(mode in 'r'):
        file = open(path, "r")
        text_temp = None
        for text in file.readlines():
            text_temp = text.rstrip('\n')
        return text_temp
        file.close()
    elif(mode in 'a'):
        if( os.path.getsize(path) < 400):
            file = open(path,"a")
            file.write(date_current+"\n")
            file.close()
        else:
            file = open(path,"w")
            file.write(date_current+"\n")
            file.close()

def after_day(res):
    #folder_year = file_time.split('-')[0]
    #folder_month = file_time.split('-')[1]
    #folder_day = file_time.split('-')[2]
    #print(folder_year,folder_month,folder_day)

    soup = bs(res.text, "html.parser")
    for item in soup.select('.sibling-items'):
        #for current in item.select('.current'):
        current_time = item.select('.current')[0]['href'].split('=')[2]
        try:
            afterDay = item.select('.before')[0].find('a')['href'].split('=')[2]

            #current_year = current.text.split('年')[0]
            #current_month = current.text.split('年')[1].split('月')[0]
            #current_day = current.text.split('月')[1].split('日')[0]
            #if(( int(folder_year) == int(current_year) ) and ( int(folder_month) == int(current_month) ) and ( int(folder_day) >= int(current_day) )):
            #print(int(file_time),int(afterDay))
            #if( int(file_time) >= int(afterDay) ):
                #return False,afterDay
            #else:
                #afterDay = item.select('.before')[0].find('a')['href'].split('=')[2]
            return True,afterDay
        except TypeError:
            return False,current_time
  
def file_url_and_name(member_illust_soup):
    #print(member_illust_soup.text)
    if 0 != len(member_illust_soup.select('._work.manga.multiple')):
        for href in member_illust_soup.select('._work.manga.multiple'):
            print(href['href'],",1",href)
            img_res = href['href']
            img_name = href.find('img')['alt']
            return(img_res, img_name)
    elif 0 != len(member_illust_soup.select('._work.multiple')):
        for href in member_illust_soup.select('._work.multiple'):
            print(href['href']+",2")
            img_res = href['href']
            img_name = href.find('img')['alt']
            return(img_res, img_name)
    elif 0 != len(member_illust_soup.select('._work.manga')):
        for href in member_illust_soup.select('._work.manga'):
            print(href['href']+",3")
            img_res = href['href']
            img_name = href.find('img')['alt']
            return(img_res, img_name)
    else:
        for img_name in member_illust_soup.select('.work-info'):
            img_name = img_name.select('.title')[0].text
            for href in member_illust_soup.select('.full-screen._ui-tooltip'):
                ##print(href['href']+",4")
                img_res = href['href']
                return(img_res, img_name)
            
#標籤過濾
def tag_rule_out(soup):
    tags_ill =['漫画', '創作BL', 'BL松', 'おそ松さん', '腐', 'ホモ', 'ゲイ', '筋肉']
    for tag_container in soup.select('.tags-container'):
    #print(tag_container)
    #print(tag_container.select('.text')[0].text)
        for tag in tag_container.select('.text'):
            print("all",tag.text)
            for tag_ill in tags_ill:
                if(tag_ill in tag.text):
                    print("out",tag.text)
                    return False
    return True

def sign(img_name):

    ill_sign=['"','|','/','?','<','>',':','*','!','\\','\n','\r','\t',' ']
    for sign in ill_sign:
        img_name = img_name.replace(sign,"")

    return img_name

def file_download(file_path, img_name, res, url, success):
    ##sign(img_name)去除不能命名的符號
    multiple_picture_boolean = os.path.isfile(file_path.replace("%s",sign(img_name.split("_")[0]+"_0")))

    #file_raw =BytesIO(res.raw.read())
    file_raw = BytesIO(res.content)
    file_raw2 = BytesIO(res.content)

    imageJudge = Image_judge(file_raw)
    #黑白判斷
    if imageJudge.size_judge():
        csvText = imageJudge.csv_get_text()
        csv_fill(url, res.url, csvText, w)
        return success
    elif imageJudge.black_white_judge():
        csvText = imageJudge.csv_get_text()
        csv_fill(url, res.url, csvText, w)
        return success
    elif imageJudge.pixel_point_judge():
        csvText = imageJudge.csv_get_text()
        csv_fill(url, res.url, csvText, w)
        return success
    imageJudge.close()

    file_path_all = file_path.replace("%s",sign(img_name))
    notRepeat_file_boolean = True
    file_path_new = file_path
    if    ( os.path.isfile(file_path_all) ):
        notRepeat_file_boolean,file_path_new = notRepeat_file(file_raw2,file_path_all,file_path,img_name)
    #print("notRepeat_file_boolean:",notRepeat_file_boolean)
    if    (notRepeat_file_boolean):
        try:
            f = open(file_path_new %(sign(img_name)),"wb")
        except OSError:
            res.close()
            return success

        buffer_size = 16000
        shutil.copyfileobj(file_raw2, f, buffer_size)

        if (multiple_picture_boolean == False) and os.path.isfile(f.name):
            f.close()
            res.close()
            return success + 1
        elif multiple_picture_boolean == True:
            res.close()
            return success
        else:
            csv_fill(url, res.url, "失敗", w)
            f.close()
            res.close()
            return success
    else:
        csv_fill(url, res.url, "重複檔案", w)
        res.close()
        return success

def notRepeat_file(file_raw, file_path_all, file_path, img_name):
    picture_file_size = len(file_raw.getvalue())
    local_file_size = os.path.getsize(file_path_all)
    print("file_size:", picture_file_size, local_file_size)
    if( picture_file_size == local_file_size ):
        return(False,file_path)
    else:
        number = 1
        while(os.path.isfile(file_path_all)):
            local_file_size = os.path.getsize(file_path_all)

            if( picture_file_size == local_file_size ):
                return(False, file_path)

            file_path_all = file_path.replace("%s", sign(img_name) + "("+str(number)+")")
            file_path_new = file_path.replace("%s", "%s("+str(number)+")")
            #print(str(file_path2).encode("utf8"))
            number += 1

        return(True,file_path_new)
    
#作品頁
def member_illust_img(url, file_path, count, success, headers):
    member_illust_res = requests.get(url, headers = headers)
    member_illust_soup = bs(member_illust_res.text, "html.parser")
    if(tag_rule_out(member_illust_soup)):
        print("member_illust.php Url: %s" %(url))
        #print(member_illust_soup.text)
        #單圖
        if 0 != len(member_illust_soup.select('.original-image')):
            for img_original in member_illust_soup.select('.original-image'):
                print("Image_Original Url:%s" %(img_original['data-src']))
                image_download_res = requests.get(img_original['data-src'], stream = True, headers = headers)
                ##print(member_illust_res.text)
                print("img_name: %s\n" %( img_original['alt'] ))
                ##輸出檔案
                success = file_download(file_path, img_original['alt'], image_download_res, url, success)
        #漫畫多圖
        elif 0 != len(member_illust_soup.select('._work.manga.multiple')):
            print(0 != len(member_illust_soup.select('._work.manga.multiple')))
            return success
        else:
            refer = url
            #print(member_illust_soup.text)
            print(0 != len(member_illust_soup.select('._work.multiple')))
            print(0 != len(member_illust_soup.select('._work.manga')))
            print(0 != len(member_illust_soup.select('.full-screen._ui-tooltip')))
            ##取得檔案網址與名稱
            img_res, img_name = file_url_and_name(member_illust_soup)
            print("https://www.pixiv.net/" + img_res )
            headers['Referer'] = refer
            img_res = requests.get("https://www.pixiv.net/" + img_res, headers = headers)
            img_soup = bs(img_res.text, "html.parser")

            image_count = 0
            #多圖
            if 0 != len(member_illust_soup.select('._work.multiple')):
                print(img_res)
                print('total2',img_soup.select(".total"))
                print('total',img_soup.select(".total")[0].text)
                if int(img_soup.select(".total")[0].text) <= 15:
                    for original_images in img_soup.select(".full-size-container._ui-tooltip"):
                        print("No.%d_%d" %(count, image_count))
                        print("https://www.pixiv.net" + original_images['href'])
                        images_download_res = requests.get("https://www.pixiv.net" + original_images['href'], headers = headers)
                        ##print(member_illust_res.text)
                        images_download_soup = bs(images_download_res.text, "html.parser")
                        for img_original in images_download_soup.select("img"):
                            print("Image_Original Url:%s" %(img_original['src']))
                            images_download_res = requests.get(img_original['src'], stream = True, headers = headers)
                            print("img_name: %s\n" %( str(img_name) ))
                            ##輸出檔案
                            success = file_download(file_path, img_name + "_" + str(image_count), images_download_res, url, success)
                            image_count += 1
            #漫畫
            elif 0 != len(member_illust_soup.select('._work.manga')):
                for img_original in img_soup.select("img"):
                    print("Image_Original Url:%s" %(img_original['src']))
                    image_download_res = requests.get(img_original['src'], stream = True, headers = headers)
                    print("img_name: %s\n" %( str(img_name) ))
                    ##輸出檔案
                    success = file_download(file_path, img_name, image_download_res, url, success)
            #gif圖
            elif 0 != len(member_illust_soup.select('.full-screen._ui-tooltip')):
                print("img_name: %s.gif\n" %( str(img_name) ))
    return success

def csv_fill(url, res, fail, w):
    data=[
         [url, res, fail]
         ]
    w.writerows(data)

if __name__ == "__main__":
    ##rs=requests.session()
    
    url = {}
    count = 0
    success = 0
    
    folder = time.strftime(r"%Y-%m-%d_%H-%M-%S",time.localtime())
    
    path = os.path.join("E:","圖")
    #path = os.path.join("D:","圖2")
    folder = makedirs_create(path, folder)
    print(path,folder)
    file_path = os.path.join(path, folder, "%s.png")
    
    mode = 'r'
    file_date_current = file_data_create(mode, None)
    
    picture_download_boolean = True
    
    cpus = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(processes = int(cpus * 1.5))
    results = []
    url_pixiv = 'https://www.pixiv.net/ranking.php'
    
    #pixiv 網站參數值
    payloads = [{'mode':'daily','p':'1','date':None},{'mode':'daily_r18','p':'1','date':None}]
    headers = pixiv3_cookie.login_get_cookie(headers)
    #print(headers)
    
    #單圖test
    #url='https://www.pixiv.net/member_illust.php?mode=medium&illust_id=62369693'
    #member_illust_img(url, file_path, count, success, headers)
    #result = pool.apply_async(func = member_illust_img, args = (url, file_path, count, success, headers))
    
    while(picture_download_boolean):
        for payload in payloads:
            p = 1
            payload['date'] = file_date_current
            payload['p'] = str(p)
    
            if(payload['mode'] in 'daily'):
                ranking_res = requests.get(url_pixiv, headers = headers, params = payload)
                picture_download_boolean, file_date_current = after_day(ranking_res)
                if not(picture_download_boolean):
                    break
                payload['date'] = file_date_current
            elif(payload['mode'] in 'daily_r18'):
                ranking_res = requests.get(url_pixiv, headers = headers, params = payload)
            
            connect_response = 200
            print(ranking_res, ranking_res.status_code == connect_response, ranking_res.url, payload['mode'])
            
            #ranking頁
            while ranking_res.status_code == connect_response:
                payload['p'] = str(p)
                ranking_res = requests.get(url_pixiv, headers = headers, params = payload)
                ranking_soup = bs(ranking_res.text, "html.parser")
                print("url:%s\npayload:%s\n" %(ranking_res.url, payload))
                for ranking_item in ranking_soup.select('.ranking-item'):
                    for new in ranking_item.select('p.new'):
                        for ranking_img_item in ranking_item.select('.ranking-image-item'):
                            url[count] = "https://www.pixiv.net/" + ranking_img_item.find('a')['href']
                            print("No.%d" %(count))
                            #member_illust_img(url[count], file_path, count, success, headers)
                            result = pool.apply_async(func = member_illust_img, args = (url[count], file_path, count, success, headers))
                            results.append(result)
                            #results = pool.apply_async(func = member_illust_img, args = (url[count], file_path, count, success), callback = member_illust_img(url[count], file_path, count, success))
                            #success = member_illust_img(url[count], file_path, count, success)
                            
                    count+=1
                p+=1
            #delete
    
    for result in results:
        success += result.get()
    pool.close()
    pool.join()
    
        
    print(file_date_current, success)
    
    mode = 'a'
    file_data_create(mode, file_date_current)
    if count == success:
        print("檔案傳輸皆成功")
    else:
        print("總數:%d, 成功數:%d" %(count, success))
    csv_file.close()
    ##error:
    ##sleep(5)
    ##Remote Disconnected('Remote end closed connection without response  python
    ##結論
    ##session()