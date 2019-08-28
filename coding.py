import time
import sqlite3

conn = sqlite3.connect('sqlite.db')
c = conn.cursor()  # 建立 cursor 來執行 SQL 語句

all_user_arr = []
save_user_arr = []
unsave_user_arr = []

# all_user_arr
SQL = "SELECT DISTINCT searchcode FROM pretestXapi2019"
cursor = conn.execute(SQL).fetchall()

for i in cursor:
    all_user_arr.append(''.join(i))

# all_Xapi_data
SQL = 'SELECT * FROM pretestXapi2019 ORDER BY timestamp ASC'
cursor = conn.execute(SQL).fetchall()


def self_data_range(name):
    tag1 = 'started'
    tag2 = 'passed'

    junk_tag = '五連方積木拼圖遊戲'
    split = [['第1關', 0, 0, []], ['第2關', 0, 0, []], ['第3關', 0, 0, []],
             ['第4關', 0, 0, []], ['第5關', 0, 0, []], ['第6關', 0, 0, []]]

    n = 0
    for value in cursor:
        if value[0] == name:
            for i in value:
                if i == tag1 or i == tag2:
                    if value[3] != '五連方積木拼圖遊戲':
                        level = int(value[3][3:4]) - 1
                        split[level][3].append(n)
                        split[level][1] = min(split[level][3])
                        split[level][2] = max(split[level][3])
                        # print(n, value)sss
            n += 1
    new_split = []
    for value in split:
        new_split.append(value[:-1])
    return new_split


def self_original_data(name):
    arr = []
    for value in cursor:
        if value[0] == name:
            arr.append(value)
    return arr


def self_clear_data(name):
    all_arr = []
    for item in self_data_range(name):
        arr = []
        start_num = item[1]
        end_num = item[2]
        for item in self_original_data(name)[start_num:end_num+1]:
            verb = item[2:][0]
            # print(verb)
            if verb != 'started' and verb != 'passed':
                arr.append(item[2:])
        all_arr.append(arr)
    return all_arr


def self_clear_data_ans(name, level):
    arr = []
    arr2 = []
    arr3 = []
    n = 0
    for i in self_clear_data(name)[level]:
        verb = i[0]
        if verb == 'solved':
            arr.append(i[3].split(' '))
            arr2.append(i[3].split(' '))
            n = 0
        else:
            arr.append('')
            n += 1
        arr3.append(n)
    arr4 = []
    n = 0
    for i in arr3:
        if i == 0:
            arr4.append(arr3[n-1] + 1)
        n += 1
    arr5 = []
    n = 0
    for i in arr2:
        for j in range(arr4[n]):
            # print(i)
            arr5.append(i)
        n += 1
    for i in arr[len(arr5):]:
        arr5.append([''])
    return arr5


# Print iterations progress
def printProgressBar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 *
                                                     (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end='\r')
    # Print New Line on Complete
    if iteration == total:
        print()


def coding(searchcode, level):
    new_arr = ['StL', 'StS']
    loading = 0
    for i in range(len(self_clear_data_ans(searchcode, level))):
        now_verb = self_clear_data(searchcode)[level][i][0]
        now_block_method = self_clear_data(searchcode)[level][i][1][0:2]
        now_block = self_clear_data(searchcode)[level][i][1][-1]
        now_ans = (searchcode, level)[i]
        now_old_code = self_clear_data(searchcode)[level][i][2]
        if now_ans != ['']:
            if now_verb == 'operate':
                if now_block_method == '拖曳':
                    if now_block in now_ans:
                        new_arr.append('DrT')
                    else:
                        new_arr.append('DrF')
                if now_block_method == '旋轉':
                    if now_block in now_ans:
                        new_arr.append('RoT')
                    else:
                        new_arr.append('RoF')
                if now_block_method == '反轉':
                    if now_block in now_ans:
                        new_arr.append('ReT')
                    else:
                        new_arr.append('ReF')

            elif now_verb == 'solved':
                new_arr.append('So')
                new_arr.append('StS')
            elif now_verb == 'snap':
                if self_clear_data(searchcode)[level][i][1][2:3] in now_ans:
                    new_arr.append('SnT')
                else:
                    new_arr.append('SnF')
            elif now_verb == 'repeated':
                new_arr.append('Rp')
        else:
            new_arr.append('Ch')

    new_arr.append('Fi')

    if 'So' in new_arr:
        SoL_last_num = [i for i, e in enumerate(new_arr) if e == 'So'][-1]
        new_arr[SoL_last_num] = 'SoL'

    Sts_last_num = [i for i, e in enumerate(new_arr) if e == 'StS'][-1]
    arr1 = new_arr[:Sts_last_num]+new_arr[Sts_last_num+1:]

    name = searchcode.replace(" ", "")[7:10]
    level_str = '第' + str(level+1)+'關'

    # print(name, level_str)

    arr_str = ', '.join(arr1)
    arr_str = '[' + arr_str + ']'

    sql_arr = [name, searchcode, level_str, arr_str]

    sqlstr = 'insert into pretestLSA2019 values('+str(
        sql_arr).strip('[]')+')'

    c.execute(sqlstr)
    conn.commit()

    return arr1


# print(coding(now, 0))
# print(all_user_arr)
# now = 'mailto:巫銘紘123@gmail.com'

num = 0

for user_code in all_user_arr:
    num += 1
    print('-----')
    print(user_code.replace(" ", "")[7:10], '----> 目前執行到第 ' + str(num) +
          '/' + str(len(all_user_arr)) + ' 人')
    # print(self_data_range(now))

    # A List of Items
    items = list(range(0, 6))
    l = len(items)

    # Initial call to print 0% progress
    printProgressBar(0, l, prefix='Progress:', suffix='Complete', length=50)
    for i, item in enumerate(items):
        # Do stuff...

        coding(user_code, i)
        time.sleep(0.1)
        # Update Progress Bar
        printProgressBar(i + 1, l, prefix='Progress:',
                         suffix='Complete', length=50)

    print('-----')


conn.close()
