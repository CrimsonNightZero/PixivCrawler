# -*- coding: utf8 -*-
# coding: utf8
# In[16]:

import requests 
from bs4 import BeautifulSoup as bs 
import shutil
import os
import time
from time import sleep
import csv

success=0

def file_url_and_name(soup3):
	if 0!=len(soup3.select('._work.manga.multiple')):
		for href in soup3.select('._work.manga.multiple'):
			#print(href['href']+",1")
			res5=href['href']
			name=href.find('img')['alt']
			return(res5,name)
	elif 0!=len(soup3.select('._work.multiple')):
		for href in soup3.select('._work.multiple'):
			#print(href['href']+",2")
			res5=href['href']
			name=href.find('img')['alt']
			return(res5,name)
	elif 0!=len(soup3.select('._work.manga')):
		for href in soup3.select('._work.manga'):
			#print(href['href']+",3")
			res5=href['href']
			name=href.find('img')['alt']
			return(res5,name)
	else:
		for name in soup3.select('.work-info'):
			name=name.select('.title')[0].text
			for href in soup3.select('.full-screen._ui-tooltip'):
				##print(href['href']+",4")
				res5=href['href']
				print(res5)
				return(res5,name)

def sign(name):
	import re
     
	ill_sign=['"','|','/','?','<','>',':','*','!','\\','\n','\r','\t',' ']
	for sign in ill_sign:
		name=name.replace(sign,"")
	return name

def file(file_path,name,res,url,success):
	repeat_file=os.path.isfile(file_path.replace("%s",sign(name.split("_")[0]+"_0")))
	##print(file_path+",,,,"+sign(name.split("_")[0]))
	##sign(name)去除不能命名的符號
	try:
		f=open(file_path %(sign(name)),"wb")
	except OSError:
		return success
	shutil.copyfileobj(res.raw,f)

	if (repeat_file==False)and os.path.isfile(f.name):
		f.close()
		return success+1
	elif repeat_file==True:
		return success
	else:
		csv_fill(url,res,"失敗",w)
		f.close()
		return success
		
def csv_fill(url,res,fail,w):
	data=[
		 [url,res,fail]
		 ]
	w.writerows(data)


##rs=requests.session()
res=requests.get("http://www.pixiv.net/ranking.php?mode=daily")
#res.encoding='UTF-8'
soup=bs(res.text, "html.parser")

url=list(range(1000))
i=0

##print(soup.select('._layout-thumbnail'))

##print(soup.select('.ranking-image-item'))

folder = time.strftime(r"%Y-%m-%d_%H-%M-%S",time.localtime())
path="E:\\圖"
os.makedirs(r'%s/%s'%(path,folder))
abs_file_path = os.path.join(path)

csv_file=open("fail.csv","w")
w=csv.writer(csv_file)	
count=100

for url in soup.select('.menu-items'):
	for li in url.select('li'):
		if ("rookie" in (li.find('a')['href'].split("&"))[0])or("female" in (li.find('a')['href'].split("&"))[0]):
			continue
		elif ("daily" in (li.find('a')['href'].split("&"))[0]):
			count=500
		else:
			count=100
		p=1
		while p <= int(count/50):
			urlsp=li.find('a')['href'].split("&")
			urlsp=urlsp[0].split("=")
			urlsp[1]=urlsp[1]+"_"+str(p)
			print(urlsp[1])
			path_temp=path+"\\"+folder
			os.makedirs(r'%s/%s'%(path_temp,urlsp[1]))
			print("http://www.pixiv.net/ranking.php"+li.find('a')['href']+"&p="+str(p))
			res=requests.get("http://www.pixiv.net/ranking.php"+li.find('a')['href']+"&p="+str(p))
			#res.encoding='UTF-8'
			soup=bs(res.text, "html.parser")
		
			for img in soup.select('.ranking-image-item'):
				url[i]="http://www.pixiv.net/"+img.find('a')['href']
				print(str(i))
	
				headers={
				'Cookie':'p_ab_id=2; login_ever=yes; module_orders_mypage=%5B%7B%22name%22%3A%22hot_entries%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22everyone_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22sensei_courses%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22spotlight%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22featured_tags%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22contests%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22following_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22mypixiv_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22booth_follow_items%22%2C%22visible%22%3Atrue%7D%5D; ki_t=1467788344590%3B1468687259800%3B1468687259800%3B4%3B8; ki_r=; a_type=1; device_token=701158ce26579aaf4760f14c89e6684d; crtg_rta=; PHPSESSID=12033914_77f48f5c72fc7831995c26d603bb729d; _ga=GA1.2.2036180445.1463923021; __utmt=1; __utma=235335808.2036180445.1463923021.1468924698.1468990586.66; __utmb=235335808.10.10.1468990586; __utmc=235335808; __utmz=235335808.1468920128.64.40.utmcsr=facebook.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmv=235335808.|2=login%20ever=yes=1^3=plan=normal=1^5=gender=male=1^6=user_id=12033914=1'
				,'Referer':'http://www.pixiv.net'
				}
				res3=requests.get(url[i],headers=headers)
				#res3.encoding='UTF-8'
				soup2=bs(res3.text, "html.parser")
				if 0!=len(soup2.select('.original-image')):
					##print(len(soup.select('.original-image')))
					for org in soup2.select('.original-image'):
						print(url[i])
						print(org['data-src'])
						res4=requests.get(org['data-src'],stream=True,headers=headers, timeout=30)
						#res4.encoding='UTF-8'
						#if i%10==0:
							#sleep(10)
						##print(res3.text)
						print("name="+str(org['alt'].encode("utf8"))+"\n")
						file_path=abs_file_path+"\\"+folder+"\\"+urlsp[1]+"\\%s.png"
						##輸出檔案
						success=file(file_path,org['alt'],res4,url[i],success)
						i+=1
				else:
					print(url[i]+"")
					refer=url[i]
					res4=requests.get(url[i],headers=headers)
					#res4.encoding='UTF-8'
					##print(res.text)
					soup3=bs(res4.text, "html.parser")
					print(0!=len(soup3.select('._work.manga.multiple')))
					print(0!=len(soup3.select('._work.multiple')))
					print(0!=len(soup3.select('._work.manga')))
					print(0!=len(soup3.select('.full-screen._ui-tooltip')))
					##取得檔案網址與名稱
					res5,name=file_url_and_name(soup3)
					print("http://www.pixiv.net/"+res5+"")
					headers={
						'Cookie':'p_ab_id=2; login_ever=yes; module_orders_mypage=%5B%7B%22name%22%3A%22hot_entries%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22everyone_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22sensei_courses%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22spotlight%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22featured_tags%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22contests%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22following_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22mypixiv_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22booth_follow_items%22%2C%22visible%22%3Atrue%7D%5D; ki_t=1467788344590%3B1468687259800%3B1468687259800%3B4%3B8; ki_r=; a_type=1; device_token=701158ce26579aaf4760f14c89e6684d; crtg_rta=; PHPSESSID=12033914_77f48f5c72fc7831995c26d603bb729d; _ga=GA1.2.2036180445.1463923021; __utmt=1; __utma=235335808.2036180445.1463923021.1468924698.1468990586.66; __utmb=235335808.10.10.1468990586; __utmc=235335808; __utmz=235335808.1468920128.64.40.utmcsr=facebook.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmv=235335808.|2=login%20ever=yes=1^3=plan=normal=1^5=gender=male=1^6=user_id=12033914=1'
						,'Referer':refer
					}
					res5=requests.get("http://www.pixiv.net/"+res5,headers=headers)
					#res5.encoding='UTF-8'
					soup4=bs(res5.text, "html.parser")
					j=0
					if 0!=len(soup3.select('._work.multiple')):
						for bb in soup4.select(".full-size-container._ui-tooltip"):
							print(str(i)+"_"+str(j))
							print("http://www.pixiv.net/"+bb['href'])
							res6=requests.get("http://www.pixiv.net/"+bb['href'],headers=headers)
							res6.encoding='UTF-8'
							#if j%10==0:
								#sleep(10)
							##print(res3.text)
							soup5=bs(res6.text, "html.parser")
							for cc in soup5.select("img"):
								print(url[i])
								print(cc['src'])
								res6=requests.get(cc['src'],stream=True,headers=headers, timeout=30)
								res6.encoding='UTF-8'
								print("name="+str(name.encode("utf8"))+"\n",)
								file_path=abs_file_path+"\\"+folder+"\\"+urlsp[1]+"\\%s.png"
								##輸出檔案
								success=file(file_path,name+"_"+str(j),res6,url[i],success)
								j+=1
							if j>15:
								break
						i+=1
					elif 0!=len(soup3.select('._work.manga')):
						for cc in soup4.select("img"):
							print(cc['src'])
							res6=requests.get(cc['src'],stream=True,headers=headers, timeout=30)
							#res6.encoding='UTF-8'
							#if i%10==0:
								#sleep(10)
							print("name="+str(name.encode("utf8"))+"\n")
							file_path=abs_file_path+"\\"+folder+"\\"+urlsp[1]+"\\%s.png"
							##輸出檔案
							success=file(file_path,name,res6,url[i],success)
						i+=1
					elif 0!=len(soup3.select('.full-screen._ui-tooltip')):
						print("name="+str(name.encode("utf8"))+".gif\n")
						#if i%10==0:
							# sleep(10)
						i+=1
				##break測試中斷點
			p+=1
	break
	
if i==success:
	print("檔案傳輸皆成功")
else:
	print("總數:"+str(i)+"成功數:"+str(success))
csv_file.close()
##error:
##sleep(5)
##Remote Disconnected('Remote end closed connection without response  python
##結論
##session()
