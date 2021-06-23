# coding:utf-8
with open("C:\\Users\\songwannian\\Desktop\\txt\\5.txt", "r", encoding='utf-8') as f:  # 打开文件
    data = f.readlines()  # 读取文件
list_n = []
for d in data:
    if '被告人' in d:
        continue
    d = d.replace('\n', '')
    list_n.append(d)
for l in list_n:
    print(l)