import csv
import re

puzzle_str = ['F', 'I', 'L', 'N', 'P', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
target_csv = 'target.csv'

def func_arr_code(code):  # 目前行為拖移的序列
    arr1 = []
    for i in code[:-3].split(' -1 '):
        arr1.append(i[4:])
    arr2 = []
    for i in arr1:
        arr2.append(re.sub("\(\d\)", "", i))
    arr3 = []
    for i in arr2:
        temp = i.split(' ')
        arr4 = []
        j = 0
        # print(temp)
        for i in temp:
            # print(i)
            if i != "":
                j = int(i)
                if j <= 12:
                    # print(j)
                    arr3.append(str(j))
    arr4 = []
    for i in arr3:
        j = int(i)-1
        arr4.append(puzzle_str[j])

    split_code = arr4
    return split_code


new_arr = []
with open(target_csv) as csvfile:
    rows = csv.reader(csvfile)
    i = 0
    for row in rows:
        new_row_arr = []
        if i > 0:
            l = 1
            for k in func_arr_code(row[2]):
                new_row_compose_arr = []
                new_row_compose_arr.append(row[0])
                new_row_compose_arr.append(row[1])
                new_row_compose_arr.append(l)
                new_row_compose_arr.append(k)
                new_row_arr.append(new_row_compose_arr)
                l += 1
        i += 1
        new_arr.append(new_row_arr)

with open('new'+target_csv, 'w') as csvfile:
    f = csv.writer(csvfile)
    for data in new_arr:
        for i in data:
            f.writerow(i)

for num in range(6):
    level_num = str(num+1)
    with open('new'+target_csv) as csvfile:
        rows = csv.reader(csvfile)
        new_arr = []
        for row in rows:
            if row[1] == level_num:
                new_arr.append(row)
        print(new_arr)

    with open(level_num+'_new'+target_csv, 'w') as csvfile:
        f = csv.writer(csvfile)
        for data in new_arr:
            f.writerow(data)

for num in range(6):
    level_num = str(num+1)
    with open(level_num+'_new'+target_csv) as csvfile:
        rows = csv.reader(csvfile)
        new_arr1 = []
        for row in rows:
            new_arr = []
            new_arr.append(row[0])
            new_arr.append(row[2])
            new_arr.append(row[3])
            new_arr1.append(new_arr)
        print(new_arr1)

    with open(level_num+'_new'+target_csv, 'w') as csvfile:
        f = csv.writer(csvfile)
        for data in new_arr1:
            f.writerow(data)
