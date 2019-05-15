# 行為歷程分析研究小工具

## 行為歷程資料爬蟲 SQLite 版 xapi_crawler_sqlite.py

1. 比對 sqlite01.db 裡 pretestXapi2019 與 pretestUser2019 兩個資料表中的使用者資料後，篩選出未被儲存進入資料庫的使用者。
2. 啟動爬蟲自動抓取並解析使用者的 xapi 資料後存入 sqlite01.db

`* 啟動程式後 xapi 官方伺服器不定時會檔 IP 導致報錯，只要重新啟動程式重抓即可。`

## 行為歷程資料爬蟲 Selenium 版 xapi_crawler_selenium.py

1. 把要爬取學生的 searchcode 放入 searchcode_arr
2. 爬蟲啟動後會開啟 Chrome 自動抓取資料並存入清單
3. 將清單輸出成 csv 並命名為「年月日\_小時分鐘\_data.csv」 例：20190502_1513_data.csv

## 行為歷程梳理 change_behavior_code.py

1. 讀入 target.csv（請參考 target_template.csv 的資料格式）
2. 梳理拖移、旋轉和反轉的行為序列，只保留拖移
3. 分各關卡輸出成 csv 並命名為「關卡\_newtarget.csv」例：1_newtarget.csv

## 自動轉換行為探勘資料 txt_to_execl.py

1. 把學生的原始資料 (.txt) 放入演算法，跑出來的行為歷程分析檔 (.txt)
2. 將行為歷程分析檔 (.txt) 放入跟 cleanTxt.py 程式同一層的 output 資料夾（必須是命名為 output 的資料夾）
3. 執行 txt_to_execl.py 程式後，即可生成 output.xlsx
