# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup as bs
import json
import os
import time
from aes_crypto import Cryption


def login_get_cookie(headers, user_default):
    path = r"C:\Users\foryou\user_default.json"
    cookie_key = ('PHPSESSID', 'device_token', 'module_orders_mypage', 'p_ab_id', 'p_ab_id_2', 'a_type',
                  'is_sensei_service_user')

    # 檢查cookie
    if check_cookie(path):
        with open(path) as r:
            user_json = json.load(r)

            cryption = Cryption()
            key = cryption.sha1(os.path.dirname(os.path.abspath(__file__)))
            headers['Cookie'] = cryption.decryption(key, user_json['Iv'], user_json['Cookie'])
            print("headers['Cookie']", headers['Cookie'])
            return headers

    data = {'pixiv_id': user_default.account,
            'password': user_default.password,
            'source': 'pc',
            'ref': 'wwwtop_accounts_index',
            'return_to': 'https://www.pixiv.net/'}

    session = requests.Session()
    url_login = 'https://accounts.pixiv.net/login?lang=zh_tw&source=pc&view_type=page&ref=wwwtop_accounts_index/get'

    login_res = session.get(url_login)
    login_soup = bs(login_res.text, "html.parser")
    json_data = login_soup.select('.json-data')[0]['value']
    post_key = json.loads(json_data)['pixivAccount.postKey']
    data['post_key'] = post_key

    session.post(url_login, data=data, headers=headers)
    str_cookie = ''
    index = 0
    for cookie in session.cookies.keys():
        print(cookie, cookie_key[index])
        if not (cookie == cookie_key[index]):
            return None
        str_cookie += format("%s=%s;" % (cookie, session.cookies.get(cookie)))
        index += 1
        print(str_cookie)

    headers['Cookie'] = str_cookie
    return headers


def check_cookie(path):
    if not (os.path.isfile(path)):
        return False
    else:
        file_day = time.strftime(r"%d", time.gmtime(os.path.getmtime(path)))
        correct_day = time.strftime(r"%d", time.localtime())

        if int(correct_day) - int(file_day) > 7:
            return False
        else:
            return True


def read_cookie(path):
    file = open(path, "r")
    cookie_temp = file.read()
    file.close()
    return cookie_temp


def write_cookie(cookie, path):
    file = open(path, "w")
    file.write(cookie)
    file.close()


# test
if __name__ == "__main__":
    print(os.path.abspath(__file__))
    print(os.path.dirname(os.path.abspath(__file__)))
    import os
    import win32api

    drives = win32api.GetLogicalDriveStrings()
    drive = drives.split("\\")
    print(drive, drives)
    a = {'a': list()}
    print(a)
    print(b" the spammish repetition")

#    aa=[1,2,5,3,3,4]
#    print(set(aa))
#    from flask import Flask, request
#    app = Flask(__name__)
#    app.run(host='127.0.0.1', port=8888, debug=True)
#    print(request.user_agent)
#    print(request.headers.get('User-Agent'))
#    print(request.user_agent.string)

#    headers = {'User-Agent':'python-requests/2.13.0'
#          ,'Referer':'https://www.pixiv.net/ranking.php'}
#    login_get_cookie(headers)


#    cookie = 'aa'
#    path = r"C:\Users\foryou\cookie.xml"
#    if check_cookie(path):
#       print('read',read_cookie(path))
#    else:
#        print('write',write_cookie(cookie, path))
