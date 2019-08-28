# !/usr/bin/python3
# coding:utf-8

import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
from datetime import timedelta
from collections import Counter
import sqlite3
from time import sleep
import json
import random

conn = sqlite3.connect('sqlite.db')
c = conn.cursor()

all_user_arr = []
save_user_arr = []
unsave_user_arr = []

# all_user_arr
SQL = "SELECT searchcode FROM pretestUser2019"
cursor = conn.execute(SQL).fetchall()

for i in cursor:
    all_user_arr.append(''.join(i))

# save_user_arr
SQL = "SELECT DISTINCT searchcode FROM pretestXapi2019"
cursor = conn.execute(SQL).fetchall()

for i in cursor:
    save_user_arr.append(''.join(i))

# unsave_user_arr
unsave_user_arr = list(set(all_user_arr).difference(set(save_user_arr)))
total = len(unsave_user_arr)


# test_arr = ['mailto:孫逸翔80@gmail.com', 'mailto:徐炫喆01@gmail.com']


now_web = []
all_data = []
anscode_arr = ['', 'L', 'N', 'P', 'T', 'U', 'V', 'X', 'Y', 'Z', 'F', 'W', 'I']

http_arr = ['http://198.161.237.181:80',
            'http://38.86.51.100:3128', 'http://153.92.5.186:8080']

http_num = 0
second = 0


proxies = {
    "http":  http_arr[http_num]
}

my_headers = {
    'Authorization': 'Basic YTEyNjg0OTAwMjpwcmluY2VwYW4=',
    'Content-Type': 'application/json',
    'Origin': 'https://cuesplateform.servehttp.com',
    'Referer': 'https://cuesplateform.servehttp.com/original_prototypes/StatementViewer/index.html',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
    'X-Experience-API-Version': '1.0.1'}


def get_data(searchcode):
    http_num = random.randint(0, len(http_arr)-1)
    proxies['http'] = http_arr[http_num]
    if searchcode.startswith('/'):
        r = requests.get('https://lrs.adlnet.gov' +
                         searchcode, headers=my_headers,  proxies=proxies)
    else:
        my_params = {
            'agent': '{"mbox":"' + searchcode + '"}',
            'limit': '0',
            'format': 'exact'
        }
        r = requests.get('https://lrs.adlnet.gov/xapi/statements',
                         params=my_params, headers=my_headers,  proxies=proxies)
    # print(requests.get('http://icanhazip.com', proxies=proxies).text)
    # if r.status_code == 200:
    return r.json()


def search_more(data):
    if data['more'] != "":
        return True
    else:
        return False


def get_all_data(name):
    time.sleep(1)
    if search_more(get_data(name)) == False:
        print('> '+'目前處理最後一頁')
        all_data.append(get_data(now_web[-1]))
        print('      ')
        return all_data
    else:
        if len(now_web) == 0:
            now_web.append(name)
        print('> '+'目前處理第 '+str(len(now_web)) + ' 頁')
        all_data.append(get_data(now_web[-1]))
        now_web.append(get_data(now_web[-1])['more'])
        # print(now_web)
        return get_all_data(now_web[-1])


def clear_data(data):
    for i in data:
        for j in i['statements']:
            arr = ['', '', '', '',
                   '', '', '', '', '']
            # arr = [timestamp, verb, description, code, matrixcode, completedSolutions, completedTime, matrix]
            type_id = j['verb']['display']['en-US']
            description = j['object']['definition']['description']['zh-TW']
            timestamp = datetime.strptime(
                j['timestamp'][0:j['timestamp'].find('+')], '%Y-%m-%dT%H:%M:%S.%f') + timedelta(hours=8)
            arr[0] = j['actor']['mbox']
            arr[1] = timestamp.strftime('%Y-%m-%dT%H:%M:%S.%f')
            arr[2] = type_id
            arr[3] = description
            if type_id == 'solved':
                temp = []
                arr[5] = list(Counter(j['result']['extensions']['ext:matrix'].replace(
                    '-2', '').replace('-1', '').replace('|', ' ').replace(',', ' ').split()).keys())
                for k in arr[5]:
                    # print(k)
                    temp.append(anscode_arr[int(k)])
                arr[5] = ' '.join(temp)
                arr[6] = j['result']['extensions']['ext:completedSolutions']
                if j['result']['extensions']['ext:completedSolutions'] == None:
                    arr[6] = 'None'
                else:
                    arr[6] = j['result']['extensions']['ext:completedSolutions']
                arr[7] = str(j['result']['extensions']['ext:completedTime'])
                arr[8] = j['result']['extensions']['ext:matrix']
            elif type_id == 'snap':
                temp = []
                arr[5] = list(Counter(j['result']['extensions']['ext:matrix'].replace(
                    '-2', '').replace('-1', '').replace('|', ' ').replace(',', ' ').split()).keys())
                for k in arr[5]:
                    # print(k)
                    temp.append(anscode_arr[int(k)])
                arr[5] = ' '.join(temp)
                arr[8] = j['result']['extensions']['ext:matrix']
            elif type_id == 'passed':
                arr[6] = j['result']['extensions']['ext:completedSolutions']
                if j['result']['extensions']['ext:completedSolutions'] == None:
                    arr[6] = 'None'
                else:
                    arr[6] = j['result']['extensions']['ext:completedSolutions']
                arr[7] = str(j['result']['extensions']['ext:completedTime'])
            elif type_id == 'operate':
                arr[4] = j['result']['extensions']['ext:code'].strip()
            sqlstr = 'insert into pretestXapi2019 values('+str(
                arr).strip('[]')+')'
            c.execute(sqlstr)
            conn.commit()


num = 0


if len(unsave_user_arr) != 0:
    print('使用者共有 ' + str(len(all_user_arr)) + ' 位')
    print('資料庫已儲存 ' + str(len(save_user_arr)) + ' 位')
    print('目前資料庫有 ' + str(len(unsave_user_arr)) + ' 個需要處理')
    print('  ')
    print(all_user_arr)
    print(save_user_arr)
    print(unsave_user_arr)
    print('  ')
    for user in unsave_user_arr:
        num += 1
        second = random.randint(2, 5)
        print(user+' '+str(num)+'/'+str(total))
        clear_data(get_all_data(user))
        now_web.clear()
        all_data.clear()
        for i in range(second):
            print('等待 '+str(second - i)+' 秒')
            time.sleep(1)
        print('開始執行下一個 user')
        print('  ')
else:
    print('使用者共有 ' + str(len(all_user_arr)) + ' 位')
    print('資料庫已儲存 ' + str(len(save_user_arr)) + ' 位')
    print('目前資料庫有 ' + str(len(unsave_user_arr)) + ' 個需要處理')
    print('> 無資料需要更新')


conn.close()
