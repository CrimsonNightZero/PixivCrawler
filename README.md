# PixivCrawler

專案開發時間 : 2016/07/08~2017/06/30 

此專案自從Pixiv頁面改版後就沒再繼續維護了。

對圖片網站Pixiv做網路爬蟲，過濾不必要的圖片，上傳到Google Driver做資料庫。

Runing mode : 1.搜圖模式, 2.建Pixiv圖庫

1.搜圖模式 : 爬取Pixiv圖片，透過otsu演算法、各顏色分布、圖片標籤、檔案大小過濾掉一部分不需要的圖，儲存到local端。

2.建Pixiv圖庫 : 在搜圖模式層面上，增加上傳Google Driver功能。

Extra function :

第一次輸入帳密上取得cookie後做AES加密，爾後登入直接利用已取得的cookie直接登入。

利用multiprocessing方式加速網路爬蟲、圖片下載處理速度。

pixiv_model.csv 、 fail.csv : 圖片資訊紀錄。

