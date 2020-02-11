PixivCrawler
==============

專案開發時間
--------------

2016/07/08~2017/06/30 

摘要
------

此專案自從Pixiv頁面改版後就沒再繼續維護了。

對圖片網站Pixiv做網路爬蟲，過濾不必要的圖片，上傳到Google Driver做資料庫。

Program summary
-----------------

* Main program : pixiv4.py

Runing mode : 1.搜圖模式, 2.建Pixiv圖庫、圖片比對

* 1.搜圖模式 : 爬取Pixiv圖片，透過otsu灰階過濾演算法、各HSV顏色分布過濾、圖片標籤、檔案大小過濾掉一部分不需要的圖，儲存到local端。

* 2.建Pixiv圖庫 : 在搜圖模式層面上，增加上傳Google Driver功能。


Extra function :

* 第一次輸入帳密上取得cookie後做AES加密，爾後登入直接利用已取得的cookie直接登入。

* 利用multiprocessing方式加速網路爬蟲、圖片下載處理速度。

* pixiv_model.csv 、 fail.csv : 圖片資訊紀錄。

過去開發紀錄
---------

* 建一個pixiv的圖庫模組可能要十幾個小時需要的容量大約要十幾G(2007~2017)

pixiv4
* 分為多種模式(1.圖片搜尋,2.圖片比對)
* image物件化

imageFilter
* 像素值存入xml
* 圖片縮圖像素值比對

pixiv4_csv
* csv各項基本操作模組化
* csv模組建立
* csv轉存xlsx(方便使用)(csv自動存取導致格式亂碼)

pixiv3_cookie
* SHA256製作key
* AES加密解密對cookie.xml

---------------------------------------------------

pixiv3
* 去除不必要的標籤以外的mode
* 搜尋首次登場
* 日期比對(現在與上次搜圖時
* Mutil Thread use

imageFilter
* 過濾90%up黑白顏色比例
* 過濾63%顏色一致性
* 過濾圖片太小

colorsConvert
* RGB轉換成HSV

pixiv3_cookie
* 自動登入機制
* add cookie

--------------------------------------------------

pixiv2 
* 重複檔案判定
* 所有圖檔儲存檔案在同月的同一資料夾
* Pixiv Tag 剔除不需要的圖檔
* 存檔buffer

----------------------------------------------------

pixiv1 
* 基礎搜尋

