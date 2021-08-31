import os
import re
import random
from Paper import *
from process_doc import paras2sentences_ltp, list2txt, read_docx


def papers_check(filepath):
    """批量文件句子人工混合标注纠错"""
    path_list = os.listdir(filepath)
    sentences = []
    for pl in path_list:
        filename_t, type_t = os.path.splitext(pl)
        if type_t != '.docx':  # 过滤文件类型
            continue
        path_temp = os.path.join(filepath, pl)
        paper = Paper(path_temp)
        # 存储指定范围段落至一个文件
        n = 0
        while n <= 7:
            if n != 5:  # 过滤标签
                n += 1
                continue
            sentence_t = paper.sentence_tag_s(n)  # 句子标注(只标注一个标签的第一句话)
            tt = r'被告[人|单]位?'
            if re.search(tt, sentence_t) is None:
                sentence_t = sentence_t.replace('\n', '')
                sentence_t = sentence_t + f"{filename_t}\n"
                sentences.append(sentence_t)
                n += 1
                continue
            n += 1
    list2txt(sentences, "C:\\Users\\songwannian\\Desktop\\5.txt")  # 将列表存储为.txt文件


def papers_check6(filepath):
    """批量文件label6标注检测"""
    path_list = os.listdir(filepath)
    path_list.sort()  # 排序，保证调试顺序
    list_t = []
    index_same = []
    for pl in path_list:
        filename_t, type_t = os.path.splitext(pl)
        list_t.append('\n.............' + filename_t + '.............')
        if type_t != '.docx':  # 过滤文件类型
            continue
        path_temp = os.path.join(filepath, pl)
        paper = Paper(path_temp)  # 读取文件处
        dic = paper.dict_label
        for i, k in dic.items():
            if i[-2] != '6':
                continue
            list_t.append(f"\n{i}:")
            print(f"\n{i}:")
            for ki in k:
                list_t.append(paper.paras[ki])
                print(paper.paras[ki])
        # 统计
        index_list_sat = paper.list_index_sa  # 读取的这篇文书的相同标签
        new_flag = True
        write_index = 100
        for ils in index_list_sat:
            for iw in index_same:
                if iw[0] == ils[0]:  # 重写
                    write_index = index_same.index(iw)
                    new_flag = False
                    break
            if new_flag:  # 增加
                index_same.append(ils)
            else:  # 重新
                if write_index < 100:
                    index_same[write_index] = [ils[0], ils[1] + index_same[write_index][1]]
        print(index_same)

    # 排序
    def takeSecond(elem):
        return elem[0]
    index_same.sort(key=takeSecond)
    print(index_same)
    list_t.append('\n' + '重复统计：' + str(index_same))
    list2txt(list_t, "C:\\Users\\songwannian\\Desktop\\6test.txt")


if __name__ == '__main__':
    papers_check6(r'E:\NLP\02Database\Document\非法采伐、毁坏国家重点保护植物罪(新)\docx')


