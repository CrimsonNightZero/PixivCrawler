import requests
from bs4 import BeautifulSoup as bs
import shutil
import os
import time
from io import BytesIO
import multiprocessing
import pixiv3_cookie
from imageFilter import Image_judge
from pixiv4_csv import Csv_operate
from aes_crypto import Cryption
import json
from google_drive_quickstart import GoogleDrive


class PixivImage:
    def __init__(self):
        self.id = None
        self.name = None
        self.author = None
        self.download_url = None
        self.refer = None


class UserDefault:
    tag_filter = ['漫画', '創作BL', 'BL松', 'おそ松さん', '腐', 'ホモ', 'ゲイ', '筋肉']

    def __init__(self):
        self.root_directory = UserDefault.root_directory
        self.account = None
        self.password = None
        self.tag_filter = self.tag_filter


headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/58.0.3029.96 Safari/537.36 "
    , 'Referer': 'https://www.pixiv.net/ranking.php'}

picture_download_boolean = True
run_mode = 1
file_date_current = None
googleDrive = GoogleDrive()


def makedirs_create(path, folder):
    folder_month = folder.split('-')[1]
    # dirPath:所有子目錄, dirs:所有目錄下所包括的目錄, files:所有目錄及檔案
    if os.path.isdir(path):
        for dirPath, dirs, files in os.walk(path):
            for dir in dirs:
                dir_month = dir.split('-')[1]
                print("this month:%r" % (dir_month == folder_month))
                if dir_month in folder_month:
                    return dir
    os.makedirs(r'%s/%s' % (path, folder))
    return folder


def xml_data_create(mode, run_mode, date_current):
    path = None
    if run_mode == 1:
        path = r"C:\Users\foryou\pixiv_update.xml"
        if not (os.path.isfile(path)):
            open(path, "w")
            return None
    elif run_mode == 2:
        path = r"C:\Users\foryou\model_update.xml"
        default_date = "20070913"
        if not (os.path.isfile(path)):
            file = open(path, "w")
            file.close()
            xml_write(path, default_date)
        return default_date
    # folder_csv = time.strftime(r"%Y-%m-%d",time.gmtime(os.path.getmtime(file_csv)))

    if mode in 'r':
        return xml_read(path)
    elif mode in 'a':
        xml_write(path, date_current)


def xml_read(path):
    file = open(path, "r")
    text_temp = None
    for text in file.readlines():
        text_temp = text.rstrip('\n')
    file.close()
    return text_temp


def xml_write(path, date_current):
    if os.path.getsize(path) < 400:
        file = open(path, "a")
        file.write(date_current)
        file.write("\n")
        file.close()
    else:
        file = open(path, "w")
        file.write(date_current + "\n")
        file.close()


def after_day(res):
    # folder_year = file_time.split('-')[0]
    # folder_month = file_time.split('-')[1]
    # folder_day = file_time.split('-')[2]
    # print(folder_year,folder_month,folder_day)

    soup = bs(res.text, "html.parser")
    for item in soup.select('.sibling-items'):
        # for current in item.select('.current'):
        current_time = item.select('.current')[0]['href'].split('=')[2]
        try:
            day_after = item.select('.before')[0].find('a')['href'].split('=')[2]

            # current_year = current.text.split('年')[0]
            # current_month = current.text.split('年')[1].split('月')[0]
            # current_day = current.text.split('月')[1].split('日')[0]
            # if(( int(folder_year) == int(current_year) ) and ( int(folder_month) == int(current_month) ) and ( int(folder_day) >= int(current_day) )):
            # print(int(file_time),int(afterDay))
            # if( int(file_time) >= int(afterDay) ):
            # return False,afterDay
            # else:
            # afterDay = item.select('.before')[0].find('a')['href'].split('=')[2]
            return True, day_after
        except TypeError:
            return False, current_time


def file_url_and_name(member_illust_soup):
    # print(member_illust_soup.text)
    for works_display in member_illust_soup.select('.works_display'):
        if 0 != len(works_display.select('._work.manga.multiple')):
            for href in works_display.select('._work.manga.multiple'):
                print(href['href'], ",1", href)
                img_res = href['href']
                img_name = href.find('img')['alt']
                return img_res, img_name
        elif 0 != len(works_display.select('._work.multiple')):
            for href in works_display.select('._work.multiple'):
                print(href['href'] + ",2")
                img_res = href['href']
                img_name = href.find('img')['alt']
                return img_res, img_name
        elif 0 != len(works_display.select('._work.manga')):
            for href in works_display.select('._work.manga'):
                print(href['href'] + ",3")
                img_res = href['href']
                img_name = href.find('img')['alt']
                return img_res, img_name
        else:
            for img_name in member_illust_soup.select('.work-info'):
                img_name = img_name.select('.title')[0].text
            for href in works_display.select('.full-screen._ui-tooltip'):
                print(href['href'] + ",4")
                img_res = href['href']
                return img_res, img_name


# 標籤過濾
def tag_rule_out(soup):
    tags_ill = ['漫画', '創作BL', 'BL松', 'おそ松さん', '腐', 'ホモ', 'ゲイ', '筋肉']
    for tag_container in soup.select('.tags-container'):
        for tag in tag_container.select('.text'):
            print("all", tag.text)
            for tag_ill in tags_ill:
                if tag_ill in tag.text:
                    print("out", tag.text)
                    return False
    return True


def sign(img_name):
    ill_sign = ['"', '|', '/', '?', '<', '>', ':', '*', '!', '\\', ' ']
    for sign in ill_sign:
        img_name = img_name.replace(sign, "")
    # ,'\n','\r','\t'
    return img_name.strip()


def file_download3(file_path, pixiv_image, res, success, file_date_current, l):
    # file_path = r"E:\aa"
    file_path = r"D:\aa"
    connect_response = 200
    if not (res.status_code == connect_response):
        return False
    file_raw = BytesIO(res.content)

    pixiv_image.download_url = res.url
    # file_raw = r'C:\Users\foryou\Desktop\temp\14456634_934945396612215_486369719_o.jpg'
    image_judge = Image_judge(file_raw)
    w, h = image_judge.image_get_size()
    pixiv_image.id = pixiv_image.refer.split("=")[2].split("&")[0]
    print(file_path)
    print(file_date_current)
    folder = os.path.join(file_path, file_date_current)
    file_name = sign(pixiv_image.name) + "(" + pixiv_image.id + ")"
    file_path = os.path.join(folder, file_name + ".xml")
    '''
    q = "name = '"+ file_date_current +"' and mimeType = 'application/vnd.google-apps.folder'"
    folder_id = googleDrive.search_folder(q)
    '''
    q = "name = '" + file_name.replace("'", "_") + "' and mimeType = 'application/vnd.google-apps.document'"
    file_id = googleDrive.search_folder(q)

    if not file_id:
        body = {"name": file_name.replace("'", "_"),
                "kind": "drive#file",
                "parents": ['0B_zC2JhWq_REQUt6X0dxaU1YOWM'],
                "mimeType": "application/vnd.google-apps.document"}
        file_id = googleDrive.create(body)['id']

    file_id = file_id
    content = image_judge.img_xml(file_path)
    print("!!!", file_id, content)
    googleDrive.update(file_id, content)

    # if imageJudge.img_write_xml(file_path):
    file_size = image_judge.image_get_file_size()
    gray_rate = image_judge.black_white_judge2()
    csv_path = r"C:\Users\foryou\pixiv_model.csv"
    csv_operate = Csv_operate(csv_path)

    l.acquire()
    csv_operate.fill(file_date_current, pixiv_image.author, sign(pixiv_image.name), pixiv_image.refer,
                     pixiv_image.download_url, file_path, w, h, file_size, gray_rate)
    l.release()

    image_judge.close()
    return True


def file_download2(file_path, pixiv_image, res, success):
    file_raw = BytesIO(res.content)
    file_raw2 = BytesIO(res.content)

    image_judge = Image_judge(file_raw)
    if image_judge.img_compare():
        return True;
    image_judge.close()

    file_path_new = file_path

    try:
        f = open(file_path_new % (sign(pixiv_image.name)), "wb")
    except OSError:
        res.close()
        return True

    buffer_size = 16000
    shutil.copyfileobj(file_raw2, f, buffer_size)

    return False


def file_download(file_path, pixiv_image, res, success):
    # sign(pixiv_image.name)去除不能命名的符號
    multiple_picture_boolean = os.path.isfile(file_path.replace("%s", sign(pixiv_image.name.split("_")[0] + "_0")))

    # file_raw =BytesIO(res.raw.read())
    file_raw = BytesIO(res.content)
    file_raw2 = BytesIO(res.content)
    pixiv_image.download_url = res.url

    image_judge = Image_judge(file_raw)
    csv_path = r"C:\Users\foryou\fail.csv"
    csv_operate = Csv_operate(csv_path)
    # 黑白判斷
    if image_judge.size_judge():
        csv_text = image_judge.failText
        csv_operate.fill(pixiv_image.refer, pixiv_image.download_url, csv_text)
        return success
    elif image_judge.black_white_judge():
        csv_text = image_judge.failText
        csv_operate.fill(pixiv_image.refer, pixiv_image.download_url, csv_text)
        return success
    elif image_judge.pixel_point_judge():
        csv_text = image_judge.failText
        csv_operate.fill(pixiv_image.refer, pixiv_image.download_url, csv_text)
        return success
    image_judge.close()

    file_path_all = file_path.replace("%s", sign(pixiv_image.name))
    print("file_path_all2", file_path_all)
    notrepeat_file_boolean = True
    file_path_new = file_path
    if os.path.isfile(file_path_all):
        notrepeat_file_boolean, file_path_new = not_repeat_file(file_raw2, file_path_all, file_path, pixiv_image.name)
    # print("notRepeat_file_boolean:",notRepeat_file_boolean)

    if notrepeat_file_boolean:
        try:
            f = open(file_path_new % (sign(pixiv_image.name)), "wb")
        except OSError:
            res.close()
            return success

        buffer_size = 16000
        shutil.copyfileobj(file_raw2, f, buffer_size)

        if (not multiple_picture_boolean) and os.path.isfile(f.name):
            f.close()
            res.close()
            return success + 1
        elif multiple_picture_boolean:
            res.close()
            return success
        else:
            csv_operate.fill(pixiv_image.refer, pixiv_image.download_url, "失敗")
            f.close()
            res.close()
            return success
    else:
        csv_operate.fill(pixiv_image.refer, pixiv_image.download_url, "重複檔案")
        res.close()
        return success


def not_repeat_file(file_raw, file_path_all, file_path, img_name):
    picture_file_size = len(file_raw.getvalue())
    local_file_size = os.path.getsize(file_path_all)
    print("file_size:", picture_file_size, local_file_size)
    if picture_file_size == local_file_size:
        return False, file_path
    else:
        number = 1
        while os.path.isfile(file_path_all):
            local_file_size = os.path.getsize(file_path_all)

            if picture_file_size == local_file_size:
                return False, file_path

            file_path_all = file_path.replace("%s", sign(img_name) + "(" + str(number) + ")")
            file_path_new = file_path.replace("%s", "%s(" + str(number) + ")")

            # print(str(file_path2).encode("utf8"))
            number += 1

        return True, file_path_new


# 作品頁
def member_illust_img(url, file_path, count, success, headers, run_mode, l=None, file_date_current=None):
    member_illust_res = requests.get(url, headers=headers)
    member_illust_soup = bs(member_illust_res.text, "html.parser")
    if tag_rule_out(member_illust_soup):
        pixiv_image = PixivImage()
        print("member_illust.php Url: %s" % url)
        print(member_illust_res.url)
        # print(member_illust_soup.text)
        # 單圖
        pixiv_image.author = member_illust_soup.select('.user')[0].text
        pixiv_image.refer = url
        if 0 != len(member_illust_soup.select('.original-image')):
            for img_original in member_illust_soup.select('.original-image'):
                print("Image_Original Url:%s" % (img_original['data-src']))
                image_download_res = requests.get(img_original['data-src'], stream=True, headers=headers)
                # print(member_illust_res.text)
                pixiv_image.name = img_original['alt']
                print("img_name: %s\n" % (img_original['alt']))
                # 輸出檔案
                if run_mode == 1:
                    success = file_download(file_path, pixiv_image, image_download_res, success)
                elif run_mode == 2:
                    success = file_download3(file_path, pixiv_image, image_download_res, success, file_date_current, l)

        # 漫畫多圖
        elif 0 != len(member_illust_soup.select('._work.manga.multiple')):
            print(0 != len(member_illust_soup.select('._work.manga.multiple')))
            return success
        else:
            # print(member_illust_soup.text)
            print(0 != len(member_illust_soup.select('._work.multiple')))
            print(0 != len(member_illust_soup.select('._work.manga')))
            print(0 != len(member_illust_soup.select('.full-screen._ui-tooltip')))
            # 取得檔案網址與名稱
            img_res, pixiv_image.name = file_url_and_name(member_illust_soup)
            print("https://www.pixiv.net/" + img_res)
            headers['Referer'] = pixiv_image.refer
            img_res = requests.get("https://www.pixiv.net/" + img_res, headers=headers)
            img_soup = bs(img_res.text, "html.parser")

            image_count = 0
            # 多圖
            for works_display in member_illust_soup.select('.works_display'):
                if 0 != len(works_display.select('._work.multiple')):
                    print(img_res.url)
                    print('total2', img_soup.select(".total"))
                    print('total', img_soup.select(".total")[0].text)
                    if int(img_soup.select(".total")[0].text) <= 15:
                        image_name = pixiv_image.name
                        for original_images in img_soup.select(".full-size-container._ui-tooltip"):
                            print("No.%d_%d" % (count, image_count))
                            print("https://www.pixiv.net" + original_images['href'])
                            images_download_res = requests.get("https://www.pixiv.net" + original_images['href'],
                                                               headers=headers)
                            # print(member_illust_res.text)
                            images_download_soup = bs(images_download_res.text, "html.parser")
                            for img_original in images_download_soup.select("img"):
                                print("Image_Original Url:%s" % (img_original['src']))
                                images_download_res = requests.get(img_original['src'], stream=True, headers=headers)
                                print("img_name: %s\n" % (str(pixiv_image.name)))

                                pixiv_image.name = image_name + "_" + str(image_count)
                                # 輸出檔案
                                if run_mode == 1:
                                    success = file_download(file_path, pixiv_image, images_download_res, success)
                                elif run_mode == 2:
                                    success = file_download3(file_path, pixiv_image, images_download_res, success,
                                                             file_date_current, l)

                                image_count += 1
                # 漫畫
                elif 0 != len(works_display.select('._work.manga')):
                    for img_original in img_soup.select("img"):
                        print("Image_Original Url:%s" % (img_original['src']))
                        image_download_res = requests.get(img_original['src'], stream=True, headers=headers)
                        print("img_name: %s\n" % (str(pixiv_image.name)))
                        # 輸出檔案
                        if run_mode == 1 :
                            success = file_download(file_path, pixiv_image, image_download_res, success)
                        elif run_mode == 2:
                            success = file_download3(file_path, pixiv_image, image_download_res, success,
                                                     file_date_current, l)
                # gif圖
                elif 0 != len(works_display.select('.full-screen._ui-tooltip')):
                    print("img_name: %s.gif\n" % (str(pixiv_image.name)))
    return success


def main():
    import threading
    global file_date_current
    # rs=requests.session()
    # https://www.pixiv.net/ranking.php?mode=daily&date=20070913 start

    url = {}
    count = 0
    picture_download_boolean = True

    folder = time.strftime(r"%Y-%m-%d_%H-%M-%S", time.localtime())

    path = os.path.join("E:", "圖")
    path = os.path.join("D:", "圖2")
    folder = makedirs_create(path, folder)
    print(path, folder)
    file_path = os.path.join(path, folder, "%s.png")

    mode = 'r'

    file_date_current = xml_data_create(mode, run_mode, None)
    print(file_date_current)
    run_mode_first_date = False
    read_date = None
    csv_operate = None
    if run_mode == 1:
        success = 0
        csv_path = r"C:\Users\foryou\fail.csv"
        if os.path.isfile(csv_path):
            os.remove(csv_path)
        csv_operate = Csv_operate(csv_path)
        csv_operate.fill("作品網址", "圖片網址", "錯誤訊息")
    elif run_mode == 2:
        q = "name = 'xml' and mimeType = 'application/vnd.google-apps.folder'"
        parents_id = googleDrive.search_folder(q)
        q = "'0B_zC2JhWq_REQUt6X0dxaU1YOWM' in parents"
        structure = googleDrive.search_file_from_folder(q, parents_id)

        success = True
        csv_path = r"C:\Users\foryou\pixiv_model.csv"
        csv_operate = Csv_operate(csv_path)
        read_date = csv_operate.read('時間')

        if read_date is None:
            csv_operate.fill("時間", "作者", "圖片名稱", "Pixiv網址", "圖片網址", "儲存位置", "寬", "長", "像素", "灰階率")
        else:
            date_remove = read_date['時間'][len(read_date['時間']) - 1]
            csv_operate.insert(None, date_remove)
            read_date['時間'] = list(filter(lambda x: x != date_remove, read_date['時間']))

            print(date_remove, read_date['時間'][len(read_date['時間']) - 1])
        if file_date_current == "20070913":
            run_mode_first_date = True

    # my = multiprocessing.Manager()
    # mylist=my.list()
    # picture_download_boolean=my.Value('i',0)

    cpus = multiprocessing.cpu_count()
    m = multiprocessing.Manager()
    l = m.Lock()

    pool = multiprocessing.Pool(processes=int(cpus * 1.5))

    results = []
    url_pixiv = 'https://www.pixiv.net/ranking.php'

    # pixiv 網站參數值
    payloads = [{'mode': 'daily', 'p': '1', 'date': None}, {'mode': 'daily_r18', 'p': '1', 'date': None}]

    #    單圖test
    #    file_date_current='20071015'
    #    url='https://www.pixiv.net/member_illust.php?mode=medium&illust_id=73859'
    #    member_illust_img(url, file_path, count, success, headers, run_mode, l, file_date_current)
    #    result = pool.apply_async(func = member_illust_img, args = (url, file_path, count, success, headers))
    #    return
    while picture_download_boolean:
        for payload in payloads:
            p = 1
            payload['date'] = file_date_current
            payload['p'] = str(p)

            if payload['mode'] in 'daily':
                ranking_res = requests.get(url_pixiv, headers=headers, params=payload)
                if run_mode_first_date:
                    file_date_current = "20070913"
                    picture_download_boolean = True
                    run_mode_first_date = False
                else:
                    picture_download_boolean, file_date_current = after_day(ranking_res)
                if not (picture_download_boolean):
                    break

                payload['date'] = file_date_current
            elif payload['mode'] in 'daily_r18':
                ranking_res = requests.get(url_pixiv, headers=headers, params=payload)

            # 待改
            if run_mode == 2:
                try:
                    if file_date_current in read_date['時間']:
                        print(file_date_current)
                        continue
                except TypeError:
                    pass
                    # read_date['時間'] = None

                file_xml_path = r"E:\aa"
                file_xml_path = r"D:\aa"
                folder_xml = os.path.join(file_xml_path, file_date_current)
                '''
                q = "name = '"+ file_date_current +"' and mimeType = 'application/vnd.google-apps.folder'"
                folder_id = googleDrive.search_folder(q)
                
                if not folder_id:
                    
                    body = {"name":file_date_current,
                            "kind":"drive#folder",
                            "parents":['0B_zC2JhWq_REQUt6X0dxaU1YOWM'],
                            "mimeType": "application/vnd.google-apps.folder"}
                    folder_id = googleDrive.create(body)['id']
                 '''
                if not os.path.isdir(folder_xml):
                    os.makedirs(r"%s\%s" % (file_xml_path, file_date_current))

            connect_response = 200
            print(ranking_res, ranking_res.status_code == connect_response, ranking_res.url, payload['mode'])

            # ranking頁
            while ranking_res.status_code == connect_response:
                payload['p'] = str(p)
                ranking_res = requests.get(url_pixiv, headers=headers, params=payload)
                ranking_soup = bs(ranking_res.text, "html.parser")
                print("url:%s\npayload:%s\n" % (ranking_res.url, payload))
                for ranking_item in ranking_soup.select('.ranking-item'):
                    news = ranking_item.select('p.new')
                    if file_date_current == "20070913":
                        news = list(range(1))
                    for new in news:
                        for ranking_img_item in ranking_item.select('.ranking-image-item'):
                            url[count] = "https://www.pixiv.net/" + ranking_img_item.find('a')['href']
                            print("No.%d" % (count))

                            if run_mode == 1:
                                # success = member_illust_img(url[count], file_path, count, success, headers, run_mode)
                                result = pool.apply_async(func=member_illust_img, args=(
                                    url[count], file_path, count, success, headers, run_mode))
                                results.append(result)

                            elif run_mode == 2:
                                # member_illust_img(url[count], file_path, count, success, headers, run_mode, l, file_date_current)
                                result = pool.apply_async(func=member_illust_img, args=(
                                    url[count], file_path, count, success, headers, run_mode, l, file_date_current))
                                results.append(result)
                                # result = threading.Thread(target = member_illust_img, args = (url[count], file_path, count, success, headers, run_mode, file_date_current), daemon = True)
                                # result.start()

                    count += 1
                p += 1

            # delete
        # download3
        for result in results:
            print(result.get())
        results = []
        # download2
        '''if(run_mode == 2):
            for result in results:
                print(result.get())
                if not result.get():
                    print('ok')
                    return
            results = []
        '''

    pool.close()
    pool.join()

    if run_mode == 1:
        for result in results:
            success += result.get()

    print(file_date_current, success)

    mode = 'a'
    xml_data_create(mode, run_mode, file_date_current)
    if count == success:
        print("檔案傳輸皆成功")
    else:
        print("總數:%d, 成功數:%d" % (count, success))

    ##error:
    ##sleep(5)
    ##Remote Disconnected('Remote end closed connection without response  python
    ##結論
    ##session()


def set_user_default(headers):
    user_default = UserDefault()
    path = r"C:\Users\foryou\user_default.json"

    default = {
        "Root_directory": input('請問您預設的目錄為:(%s)\n' % os.path.dirname(os.path.abspath(__file__))) \
                          or os.path.dirname(os.path.abspath(__file__)),
        "Cookie": None, "Iv": None}
    user_default.root_directory = default["Root_directory"]

    while True:
        account = input('請輸入Pixiv帳號:\n')
        user_default.account = account

        while True:
            password = input('請輸入Pixiv密碼:\n')
            password2 = input('請再輸入Pixiv密碼:\n')
            if password == password2:
                user_default.password = password

                break
            else:
                print("密碼不符合")

        cryption = Cryption()
        headers = pixiv3_cookie.login_get_cookie(headers, user_default)
        key = cryption.sha1(user_default.root_directory)
        cookie_encypt = cryption.encryption(key, cryption.iv, headers['Cookie'])
        print(headers)

        if headers is None:
            print("帳密錯誤")
        else:
            default['Cookie'] = cookie_encypt
            default['Iv'] = cryption.iv
            break

    with open(path, 'w') as f:
        json.dump(default, f)
        f.close()


# 1個月10分  20070913
if __name__ == "__main__":
    path = r"C:\Users\foryou\user_default.json"

    if os.path.isfile(path) and pixiv3_cookie.check_cookie(path):
        #       import json
        #       default ='"{\'root_directory\':\'a\'}"'
        #       print(json.loads(default))
        #        password = input('請輸入Pixiv密碼:\n')
        user_default = UserDefault()
        with open(path) as r:
            user_json = json.load(r)
            user_default.root_directory = user_json["Root_directory"]
        #        user_default.password = password
        headers = pixiv3_cookie.login_get_cookie(headers, user_default)
    else:
        set_user_default(headers)

    while True:
        print("1.搜圖模式, 2.建Pixiv圖庫, exit.離開此程式")
        run_mode = input('請輸入您要使用的模式:\n')

        if run_mode == '1' or run_mode == '2':
            run_mode = int(run_mode)
            main()
            break
        elif run_mode == 'exit':
            break
        else:
            print('您輸入錯誤!!!')

# 程式中斷處理
#    try:
#        main()
#    except KeyboardInterrupt:
#        csv_path = r"C:\Users\foryou\pixiv_model.csv"
#        xlsx_path = r"C:\Users\foryou\pixiv_model.xlsx"
#        csv_operate = Csv_operate(csv_path)
#        read_date = csv_operate.read('時間')
#        print(run_mode, read_date[len(read_date) - 2])
#        xml_data_create('a', run_mode, read_date[len(read_date) - 2] )
#        csv_operate.csv_from_excel(xlsx_path)

# csv_read()
