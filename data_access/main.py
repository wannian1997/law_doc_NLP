import os
import re
from TPaper import *
from process_doc import paras2sentences, list2txt, read_docx


def papers_check(filepath):
    """批量文件句子人工混合标注纠错"""
    path_list = os.listdir(filepath)
    sentences = []
    for pl in path_list:
        filename_t, type_t = os.path.splitext(pl)
        if type_t != '.docx':  # 过滤文件类型
            continue
        path_temp = os.path.join(filepath, pl)
        paper = TPaper(path_temp)
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


def paper_check(path):
    """单文档标注混合纠错"""
    paper = TPaper(path)  # 实例化
    dic = paper.dict_label
    for i, k in dic.items():
        print(f"{i}:{k}")
        for kt in k:
            print(kt, paper.paras[kt])
    list2txt(paper.sentence_tag_s(5), 'C:\\Users\\songwannian\\Desktop\\1.txt')  # 将列表存储为.txt文件
    print(paper.sentence_tag_s(0))


if __name__ == '__main__':
    # filter_path = 'E:\\NLP\\02 Database\\Document\\非法采伐、毁坏国家重点保护植物罪(新)\\docx'
    # papers_check(filter_path)

    path1 = 'E:\\NLP\\02 Database\\Document\\非法采伐、毁坏国家重点保护植物罪(新)\\docx\\宋元坤非法采伐国家重点保护植物罪一审刑事判决书.docx'
    paper_check(path1)