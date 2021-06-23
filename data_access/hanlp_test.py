# coding:utf-8
import docx
from pyhanlp import *
import win32com.client as wc

print(HanLP.segment('你好，NLP'))


# 加载某文件夹下的所有doc文件，返回doc绝对路径列表
def load_doc_path(file_path):
    doc_path_list = []  # 保存文件地址和名称
    files = os.listdir(file_path)
    for _file in files:
        if not os.path.splitext(_file)[1] == '.doc':  # 判断是否为doc文件
            continue
        abso_path = os.path.join(file_path, _file)
        doc_path_list.append(abso_path)
    return doc_path_list


# 读取docx文档,并将每段存入一个列表
def read_docx(path):
    doc = docx.Document(path)
    paras_temp = []  # 用来存储段落
    for p in doc.paragraphs:
        p1 = p.text.replace(" ", "")  # 去除空格,并以字符串的形式存储在列表中
        paras_temp.append(p1)
    print(path + "文件读取成功\n")
    return paras_temp


# 标注
def words_tag(paras):
    paras_temp = []
    for p in paras:
        p1 = HanLP.segment(p)
        paras_temp.append(p1)
    print("标注成功！\n")
    return paras_temp


# 提取特定主体段落;subject_list为要抽取的对象，pn为要抽取前n段
def subject_extract(subject_list, pn):
    subject_para = []
    for sl01 in subject_list:
        pi = 0
        for p2 in paras_list01:
            if pi < pn:  # 只取前几段
                pi = 1 + pi
                if sl01 in p2:
                    print(p2)
                    subject_para.append(p2)


# 以整个文书为基础进行分析关键字和自动摘要
def total_paper_analyse(paras):
    # 合并字符串
    str01 = ""
    for p in paras:
        str01 = str01 + p + "\n"

    print(str01)

    # 提取关键字
    print("\n提取关键字：")
    ek = HanLP.extractKeyword(str01, 10)
    for e in ek:
        print(e)
    # 自动摘要
    print("\n自动摘要：")
    es = HanLP.extractSummary(str01, 10)
    for e in es:
        print(e)


print(".............测试部分..............\n")
file_path = "E:\\NLP\\裁判文书\\重大环境污染罪\\通知书1"    # doc文件夹路径
doc_path_list = load_doc_path(file_path)

paras_list01 = read_docx()
paras_list02 = words_tag(paras_list01)
for pl in paras_list02:
    print(pl)
print("显示结束。")

