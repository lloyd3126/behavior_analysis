# -*- coding: utf-8 -*
import csv
import sqlite3
import time
import os
from os import walk
from os.path import join

# 指定要列出所有檔案的目錄
file_path = "./require"
path_arr = []
filename_arr = []

# 遞迴列出所有檔案的絕對路徑
for root, dirs, files in walk(file_path):
    for f in files:
        fullpath = join(root, f)
        path_arr.append(fullpath)
        filename_arr.append(fullpath.rstrip('.txt').lstrip('./require/'))

# print(path_arr)
# print(filename_arr)


def transform_one_txt(file_path, file_name):
    f = open(file_path, 'r')
    text = []
    for line in f:
        line = line.rstrip('\n')
        text.append(line)
    level_num_arr = text[1].lstrip('[').rstrip(']').split(',')
    temp_txt = ''
    for level_num in level_num_arr:
        temp_txt += '\'第'+level_num+'關\', '
    level_str = temp_txt.rstrip(', ')
    name_arr = text[3:]
    temp_txt = ''
    for name in name_arr:
        temp_txt += '\''+name+'\', '
    name_str = temp_txt.rstrip(', ')
    SQL = 'SELECT code FROM pretestLSA2019 WHERE level IN (' + \
        level_str + ') AND name IN (' + name_str + ')'
    conn = sqlite3.connect('../sqlite.db')
    c = conn.cursor()  # 建立 cursor 來執行 SQL 語句
    cursor = conn.execute(SQL).fetchall()
    code_arr = []
    for i in cursor:
        code_arr.append(''.join(i))
    conn.close()

    path = './result/'

    global temp_time
    temp_time = time.localtime(time.time())
    if temp_time.tm_mon < 10:
        path += str(temp_time.tm_year) + '0' + \
            str(temp_time.tm_mon) + str(temp_time.tm_mday)
    else:
        path += str(temp_time.tm_year) + \
            str(temp_time.tm_mon) + str(temp_time.tm_mday)

    if not os.path.isdir(path):
        os.mkdir(path)

    filename = path + '/'+file_name+'.csv'

    print('輸出 ------> ' + file_name+'.csv')

    # 使用者編號, 序列編號, 事件

    # 開啟輸出的 CSV 檔案
    with open(filename, 'w', newline='') as csvfile:
        # 建立 CSV 檔寫入器
        writer = csv.writer(csvfile)
        # 寫入一列資料
        user_num = 0
        for user_code in code_arr:
            user_num += 1
            sequential_num = 0
            user_code = user_code.lstrip('[').rstrip(']').split(', ')
            # print(user_code)
            for event in user_code:
                sequential_num += 1
                # print(user_num, sequential_num, event)
                writer.writerow([user_num, sequential_num, event])


for idx, path in enumerate(path_arr):
    name = filename_arr[idx]
    print('輸出 ------> ' + name+'.txt')
    # print(name, path)
    transform_one_txt(path, name)
