# coding:utf-8
with open("C:\\Users\\songwannian\\Desktop\\文书全篇文字划分.txt", "r") as f:  # 打开文件
    data = f.readlines()  # 读取文件
print(data)
list_n = []
for d in data:
    if '被告人' in d:
        continue
    d = d.replace('\n', '')
    list_n.append(d)
for l in list_n:
    print(l)