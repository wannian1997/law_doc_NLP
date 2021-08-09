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


