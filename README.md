# 自動化解析行為歷程分析檔 txt_to_execl.py

> 把行為歷程分析檔 (.txt) 自動化的彙整成 excel

## 操作方式

1. 把學生的原始資料 (.txt) 放入演算法，跑出來的行為歷程分析檔 (.txt)
2. 將行為歷程分析檔 (.txt) 放入跟 cleanTxt.py 程式同一層的 output 資料夾（必須是命名為 output 的資料夾）
3. 執行 txt_to_execl.py 程式後，即可生成 output.xlsx

## 提醒

- 跑出來的 output.xlsx 中資料表的命名為原行為歷程分析 txt 檔的檔名。
- 如果無法執行，確認終端機訊息，output 資料夾中不得有除了行為歷程分析檔 (.txt)以外的任何檔案。
