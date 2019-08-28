# 行為歷程分析研究小工具

## 行為歷程資料爬蟲 SQLite 版 xapi_crawler_sqlite.py

1. 比對 sqlite01.db 裡 pretestXapi2019 與 pretestUser2019 兩個資料表中的使用者資料後，篩選出未被儲存進入資料庫的使用者。
2. 啟動爬蟲自動抓取並解析使用者的 xapi 資料後存入 sqlite01.db

`* 啟動程式後 xapi 官方伺服器不定時會檔 IP 導致報錯，只要重新啟動程式重抓即可。`

## 滯後序列分析

1. 按照 require_template.txt 製作所需轉換成 csv 的資料需求 txt 檔
2. 將檔案存放於 require 資料夾下
3. 啟動 LSA_csv.py
4. 程式會將將轉換完畢的 csv 檔案會放置 result 資料夾下

## 自動轉換行為探勘資料 txt_to_execl.py

1. 把學生的原始資料 (.txt) 放入演算法，跑出來的行為歷程分析檔 (.txt)
2. 將行為歷程分析檔 (.txt) 放入跟 cleanTxt.py 程式同一層的 output 資料夾（必須是命名為 output 的資料夾）
3. 執行 txt_to_execl.py 程式後，即可生成 output.xlsx
