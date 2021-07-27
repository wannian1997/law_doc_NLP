# coding:utf-8
from pyhanlp import *

print(HanLP.segment('公诉机关广西壮族自治区西林县人民检察院'))


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


