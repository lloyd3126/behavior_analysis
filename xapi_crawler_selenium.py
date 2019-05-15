# !/usr/bin/python3
# coding:utf-8 

import json
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import time
import csv
import numpy as np


searchcode_arr = ['徐炫喆01', '陳靖丰03',' 王彥勳103', '李坤祐88', '許逸翔04', '黃宸語05', '楊子涵06', '胡迪07', '紀程翔08', '張又晨09', '曾國任10', '張允齊11', '巫奇軒12', '李沂恩14', '楊予彤15', ' 黃安妤16', '袁于哲17', '賴嵩鈞19', '王若頤17', '陳羽婕23', '陳謙恩24', '賴亭羽25', '蔡欣渝26', '吳泓緯16', '鄭宇桐29', '宋牧穎31','張㛢甄32', '黨弘哲6', '鄧明鈞34', '王廷熙55', ' 張翔程59', '戴裕珉67', '蘇立螢70', '周言71', '孫逸翔80', '陳卷喁90', '陳元豪91', '林柏宇97', '何侑錡102', '郝宇宏104_2', '葉于禎105', '陳冠辰021', '蘇冠宇039', '黃冠銘101', '陳威辰106', '陳崇安107', '許瑜珊108', '盧冠宇109', '沈宬賦110', '包守策112']
test_arr = ['王若頤17']

def getFileName():
    localtime = time.localtime(time.time())
    if (localtime[1]<10): 
        month = '0' + str(localtime[1]) 
    else:
        month =str(localtime[1])

    if (localtime[2]<10): 
        date = '0' + str(localtime[2]) 
    else:
        date =str(localtime[2])

    if (localtime[3]<10): 
        hours = '0' + str(localtime[3]) 
    else:
        hours =str(localtime[3])

    if (localtime[4]<10): 
        minute = '0' + str(localtime[4])
    else:
        minute =str(localtime[4])

    return str(localtime[0]) + month + date + '_' + hours + minute+'_data.csv'

def getAllStage(searchcode, verb):
    my_headers = {'Authorization': 'Basic YTEyNjg0OTAwMjpwcmluY2VwYW4=', 'Content-Type': 'application/json', 'Origin': 'https://cuesplateform.servehttp.com', 'Referer': 'https://cuesplateform.servehttp.com/original_prototypes/StatementViewer/index.html',
                  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36', 'X-Experience-API-Version': '1.0.1'}
    my_params = {
        'verb': 'http://adlnet.gov/expapi/verbs/'+verb, 
        'agent':'{"mbox":"mailto:'+ searchcode +'@gmail.com"}',
        'limit':'0',
        'format':'exact'
        }
    r = requests.get('https://lrs.adlnet.gov/xapi/statements', params = my_params, headers = my_headers)
    data = r.json()
    return data['statements']

def getSingleStage(searchcode, verb, stage):
    my_headers = {'Authorization': 'Basic YTEyNjg0OTAwMjpwcmluY2VwYW4=', 'Content-Type': 'application/json', 'Origin': 'https://cuesplateform.servehttp.com', 'Referer': 'https://cuesplateform.servehttp.com/original_prototypes/StatementViewer/index.html',
                  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36', 'X-Experience-API-Version': '1.0.1'}
    my_params = {
        'verb': 'http://adlnet.gov/expapi/verbs/'+verb, 
        'activity': 'http://adlnet.gov/pentominoXapi/stage'+str(stage), 
        'agent':'{"mbox":"mailto:'+ searchcode +'@gmail.com"}',
        'limit':'0',
        'format':'exact'
        }
    r = requests.get('https://lrs.adlnet.gov/xapi/statements', params = my_params, headers = my_headers)
    data = r.json()
    return data['statements']

def getBehaviorData(searchCode, stage):
    actorEmail = driver.find_element_by_id("actorEmail")
    verb = driver.find_element_by_id("verb")
    activityId = driver.find_element_by_id("activityId")
    refreshStatements = driver.find_element_by_id("refreshStatements")
    actorEmail.clear()
    verb.clear()
    activityId.clear()
    actorEmail.send_keys(searchCode+"@gmail.com")
    verb.send_keys("http://adlnet.gov/expapi/verbs/attempted")
    activityId.send_keys("http://adlnet.gov/pentominoXapi/stage"+str(stage))
    refreshStatements.click()
    sleep(4)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    behaviorCode = soup.select('#behaviorCode')[0].text
    behaviorTimes = soup.select('#behaviorTimes')[0].text
    arr = []
    arr.append(behaviorTimes)
    arr.append(behaviorCode)
    sleep(1)
    return arr


driver = webdriver.Chrome()
driver.get("https://cuesplateform.servehttp.com/original_prototypes/StatementViewer/index.html")
assert "Experience" in driver.title
sleep(3)

correct_arr = []
error_arr = []
num = 1
for searchcode in searchcode_arr:
    print('處理第' + str(num) + '位，總共：' + str(len(searchcode_arr)) + '位')
    num += 1
    checkPassedData = getAllStage(searchcode,'passed')
    name = checkPassedData[0]['actor']['name'].replace(' ', '')
    mbox = checkPassedData[0]['actor']['mbox']
    if len(checkPassedData) < 6:
        error_arr.append(name)
        error_arr.append(mbox)
    else: 
        arr = []
        arr.append(name)
        arr.append(mbox)
        for stage in range(5,-1,-1):
            print('第'+str(6-stage)+'關'+'')
            solutions = checkPassedData[stage]['result']['extensions']['ext:completedSolutions']
            completedTime = checkPassedData[stage]['result']['extensions']['ext:completedTime']
            if solutions == None:
                solutions = 0
            print('----> 搜尋 solutions')
            arr.append(int(solutions))
            if completedTime == 1:
                checkSingleStageData = getSingleStage(searchcode, 'solved', 6-stage)
                if len(checkSingleStageData) > 0:
                    completedTime = checkSingleStageData[0]['result']['extensions']['ext:completedTime']
                else:
                    completedTime = '無數據'
            print('----> 搜尋 time')
            arr.append(completedTime)
            getBehaviorDataArr = getBehaviorData(searchcode, 6-stage)
            behaviorTimes = getBehaviorDataArr[0]
            behaviorCode = getBehaviorDataArr[1]
            print('----> 搜尋 behaviorTimes')
            arr.append(behaviorTimes)
            print('----> 搜尋 behaviorCode')
            arr.append(behaviorCode)
            sleep(1)
        correct_arr.append(arr)
        arr = []

driver.close()

print(correct_arr)
print(error_arr)

title = ['姓名','查詢碼','完成第一關解數','完成第一關時間','完成第一關操作次數','完成第一關行為歷程','完成第二關解數','完成第二關時間','完成第二關操作次數','完成第二關行為歷程','完成第三關解數','完成第三關時間','完成第三關操作次數','完成第三關行為歷程','完成第四關解數','完成第四關時間','完成第四關操作次數','完成第四關行為歷程','完成第五關解數','完成第五關時間','完成第五關操作次數','完成第五關行為歷程','完成第六關解數','完成第六關時間','完成第六關操作次數','完成第六關行為歷程']
filename = getFileName()
with open(filename,'w' , newline='', encoding='utf-8') as csvfile:
    f = csv.writer(csvfile)
    f.writerow(title)
    for data in correct_arr:
        f.writerow(data)
    f.writerow(error_arr)

print('done') 



