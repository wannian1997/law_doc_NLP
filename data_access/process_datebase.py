import os
import re
import random
from Paper import *
from process_doc import paras2sentences_ltp, list2txt, read_docx

def papers_check_0(filepath,tag0=3,tag1=0):
    """批量文件处理，并将tag0转换为tag1"""
    path_list = os.listdir(filepath)
    sentences = []  # 存储入txt文件
    for pl in path_list:
        filename_t, type_t = os.path.splitext(pl)
        if type_t != '.docx':  # 过滤文件类型
            continue
        path_temp = os.path.join(filepath, pl)
        paper = Paper(path_temp)  # 实例化一个文书类型
        # 存储指定范围段落至一个文件
        n = 0
        while n <= 7:
            if n != 3:  # 过滤标签，只保留这个标签
                n += 1
                continue
            sentence_t = paper.sentence_tag_s(n)  # 句子标注(只标注一个标签的第一句话)
            sentence_t = sentence_t.replace(f'\t{tag0}', f'\t{tag1}\n')
            sentences.append(sentence_t)
            n += 1
    list2txt(sentences, "C:\\Users\\songwannian\\Desktop\\0.txt")  # 将列表存储为.txt文件


def papers_check_1(filepath, tag0 ='5', tag1='1'):
    """批量文件处理，并将tag0转换为tag1"""
    path_list = os.listdir(filepath)
    sentences = []
    for pl in path_list:
        filename_t, type_t = os.path.splitext(pl)
        if type_t != '.docx':  # 过滤文件类型
            continue
        path_temp = os.path.join(filepath, pl)
        paper = Paper(path_temp)
        # 存储指定范围段落至一个文件
        for p in paper.sentences:
            if p[-2] == tag0:
                # 过滤
                if p[0] == '因':
                    continue
                if p[1] == '因':
                    continue
                if p[0:1] == '本院':
                    continue
                if '取保候审' in p:
                    continue
                if '拘留' in p:
                    continue
                if '羁押于' in p:
                    continue
                if '辩护人' in p:
                    continue
                if len(p) <15:
                    continue
                if ('年' in p[0:15]) and ('月' in p[0:15]) :
                    continue
                if p[0:3] != '被告人':
                    continue
                p_save = p.replace(f'\t{tag0}\n', f'\t{tag1}\n')
                sentences.append(p_save)
    list2txt(sentences, "C:\\Users\\songwannian\\Desktop\\1.txt")  # 将列表存储为.txt文件

def papers_check_2(filepath, tag0='5', tag1='2'):
    """经鉴定"""
    path_list = os.listdir(filepath)
    sentences = []
    for pl in path_list:
        filename_t, type_t = os.path.splitext(pl)
        if type_t != '.docx':  # 过滤文件类型
            continue
        path_temp = os.path.join(filepath, pl)
        paper = Paper(path_temp)
        # 存储指定范围段落至一个文件
        for p in paper.sentences:
            if not ('经' in p[0:15]):
                continue
            if not ('鉴定'in p[0:15]):
                continue
            if p[0:3] == '上述事实':
                continue
            if '辩护人' in p[0:15]:
                continue
            if len(p) <= 10:
                continue
            p_save = p.replace(f'\t{p[-2]}\n', f'\t{tag1}\n')
            sentences.append(p_save)
    list2txt(sentences, "C:\\Users\\songwannian\\Desktop\\2.txt")  # 将列表存储为.txt文件

def papers_check_3(filepath, tag0='5', tag1='3'):
    """案由"""
    path_list = os.listdir(filepath)
    sentences = []
    for pl in path_list:
        filename_t, type_t = os.path.splitext(pl)
        if type_t != '.docx':  # 过滤文件类型
            continue
        path_temp = os.path.join(filepath, pl)
        paper = Paper(path_temp)
        # 存储指定范围段落至一个文件
        for p in paper.sentences:
            if not ('本院认为' in p):
                continue
            if not ('构成' in p):
                continue
            p_save = p.replace(f'\t{p[-2]}\n', f'\t{tag1}\n')
            sentences.append(p_save)
    list2txt(sentences, f"C:/Users/songwannian/Desktop/{tag1}.txt")  # 将列表存储为.txt文件

def papers_check_4(filepath, tag0='5', tag1='4'):
    """影响判决的因素"""
    path_list = os.listdir(filepath)
    sentences = []
    for pl in path_list:
        filename_t, type_t = os.path.splitext(pl)
        if type_t != '.docx':  # 过滤文件类型
            continue
        path_temp = os.path.join(filepath, pl)
        paper = Paper(path_temp)
        index0 = 0
        index1 = 1
        extract_flag = 0  # 成功抽取标志
        # 存储指定范围段落至一个文件
        for p in paper.sentences:
            if ('本院认为' in p) and ('构成' in p):
                index0 = paper.sentences.index(p)  # 案由段落索引
            if ('根据' in p) and ('判决如下' in p):
                index1 = paper.sentences.index(p)  # 判决段落索引
        if index1 > index0 > 0:
            extract_flag = 1
        if extract_flag:
            index0 += 1
            while index0 < index1:
                p_save = paper.sentences[index0].replace(f'\t{p[-2]}\n', f'\t{tag1}\n')
                sentences.append(p_save)
                index0 += 1
    list2txt(sentences, f"C:/Users/songwannian/Desktop/{tag1}.txt")  # 将列表存储为.txt文件

def papers_check_41(filepath, tag0='5', tag1='4'):
    """影响判决的因素,主犯从犯"""
    path_list = os.listdir(filepath)
    sentences = []
    for pl in path_list:
        filename_t, type_t = os.path.splitext(pl)
        if type_t != '.docx':  # 过滤文件类型
            continue
        path_temp = os.path.join(filepath, pl)
        paper = Paper(path_temp)
        # 存储指定范围段落至一个文件
        for p in paper.sentences:
            # if p[-2] == 'F':
            #     break
            if '被告人在' in p:
                continue
            if '被告人于' in p:
                continue
            if ('第' in p[0:5]) and ('条' in p[0:20]):
                continue
            if len(p) <=15:
                continue
            if '人以上共同过失犯' in p:
                continue
            if ('辩称' in p) or ('辩护人' in p):
                continue
            if '二人系共同犯罪' in p:
                continue
            if '本院认为' in p[0:10]:
                continue
            if '《中华人民共和国刑法》' in p:
                continue
            if p[0] == '第':
                continue
            if ('主犯' in p) or ('从犯' in p) or ('共同犯罪' in p) or ('累犯' in p):
                sentences.append(p.replace(f'\t{p[-2]}\n', f'\t{tag1}\n'))
    list2txt(sentences, f"C:/Users/songwannian/Desktop/{tag1}.txt")  # 将列表存储为.txt文件

def papers_check_5(filepath, tag0='5', tag1='5'):
    """法律依据"""
    path_list = os.listdir(filepath)
    sentences = []
    for pl in path_list:
        filename_t, type_t = os.path.splitext(pl)
        if type_t != '.docx':  # 过滤文件类型
            continue
        path_temp = os.path.join(filepath, pl)
        paper = Paper(path_temp)
        # 存储指定范围段落至一个文件
        for p in paper.sentences:
            if not ('《中华人民共和国刑法》' in p):
                continue
            if not ('判决如下' in p):
                continue
            p_save = p.replace(f'\t{p[-2]}\n', f'\t{tag1}\n')
            sentences.append(p_save)
    list2txt(sentences, f"C:/Users/songwannian/Desktop/{tag1}.txt")  # 将列表存储为.txt文件


def papers_check_6(filepath, tag0='5', tag1='6'):
    """判决结果"""
    path_list = os.listdir(filepath)
    sentences = []
    for pl in path_list:
        filename_t, type_t = os.path.splitext(pl)
        if type_t != '.docx':  # 过滤文件类型
            continue
        path_temp = os.path.join(filepath, pl)
        paper = Paper(path_temp)
        # 存储指定范围段落至一个文件(索引策略)
        index0 = 0
        index1 = 0
        index1_flag = 1
        for p in paper.sentences:
            if p[-2] == 'F':
                index0 = paper.sentences.index(p) + 1
            elif p[-2] == '8':
                if index1_flag:
                    index1 = paper.sentences.index(p)
                index1_flag = 0
        # 向前继续检索index1
        if index1 > 10 :
            index1_search_flag = index1 - 3
            while index1 >= index1_search_flag:
                if ('不服' in paper.sentences[index1]) and ('上诉' in paper.sentences[index1]):
                    break
                index1 -= 1

        extract_flag = 0
        if index1 > index0 > 0:
            extract_flag = 1
        if extract_flag:
            while index0 < index1:
                if paper.sentences[index0][0] == '（':
                    index0 += 1
                    continue
                if paper.sentences[index0][-4] == '）':
                    index0 += 1
                    continue
                if len(paper.sentences[index0]) < 20:
                    index0 += 1
                    continue
                if '判决如下' in paper.sentences[index0]:
                    index0 += 1
                    continue
                if '判决如下' in paper.sentences[index0]:
                    index0 += 1
                    continue
                if '判决执行' in paper.sentences[index0]:
                    index0 += 1
                    continue
                if '年' in paper.sentences[index0][0:20]:
                    index0 += 1
                    continue
                if ('(' in paper.sentences[index0][0:30]) or (')' in paper.sentences[index0][0:30]) or ('（' in paper.sentences[index0][0:30]) or ('）' in paper.sentences[index0][0:30]) :
                    index0 += 1
                    continue
                p_save = paper.sentences[index0].replace(f'\t{p[-1]}\n', f'\t6\n')
                p_save = p_save.replace('一、', '')
                p_save = p_save.replace('二、', '')
                p_save = p_save.replace('三、', '')
                p_save = p_save.replace('四、', '')
                p_save = p_save.replace('五、', '')
                p_save = p_save.replace('六、', '')
                p_save = p_save.replace('七、', '')
                p_save = p_save.replace('八、', '')
                p_save = p_save.replace('九、', '')
                p_save = p_save.replace('一.', '')
                p_save = p_save.replace('二.', '')
                p_save = p_save.replace('三.', '')
                p_save = p_save.replace('四.', '')
                p_save = p_save.replace('五.', '')
                p_save = p_save.replace('六.', '')
                p_save = p_save.replace('七.', '')
                p_save = p_save.replace('八.', '')
                p_save = p_save.replace('九.', '')
                p_save = p_save.replace('1.', '')
                p_save = p_save.replace('2.', '')
                p_save = p_save.replace('3.', '')
                p_save = p_save.replace('4.', '')
                sentences.append(p_save)
                index0 += 1
    list2txt(sentences, f"C:/Users/songwannian/Desktop/{tag1}.txt")  # 将列表存储为.txt文件

def paper_check(path):
    """单文档标注混合纠错"""
    paper = Paper(path)  # 实例化
    dic = paper.dict_label
    for i, k in dic.items():
        print(f"{i}:{k}")
        for kt in k:
            print(kt, paper.paras[kt])
    list2txt(paper.sentence_tag_s(5), 'C:\\Users\\songwannian\\Desktop\\1.txt')  # 将列表存储为.txt文件
    print(paper.sentence_tag_s(0))

def entropy():
    """处理数据集,将桌面1256文件夹里面的数据换成你处理过的数据集"""

    txt_path0 = r'C:\Users\songwannian\Desktop\1256\0.txt'
    txt_path1 = r'C:\Users\songwannian\Desktop\1256\1.txt'
    txt_path2 = r'C:\Users\songwannian\Desktop\1256\2.txt'
    txt_path3 = r'C:\Users\songwannian\Desktop\1256\3.txt'
    txt_path4 = r'C:\Users\songwannian\Desktop\1256\4.txt'
    txt_path5 = r'C:\Users\songwannian\Desktop\1256\5.txt'
    txt_path6 = r'C:\Users\songwannian\Desktop\1256\6.txt'

    f = open(txt_path0, "r", encoding='UTF-8')  # 设置文件对象
    list0 = f.readlines()  # 直接将文件中按行读到list里，效果与方法2一样
    f.close()  # 关闭文件

    f = open(txt_path1, "r", encoding='UTF-8')  # 设置文件对象
    list1 = f.readlines()  # 直接将文件中按行读到list里，效果与方法2一样
    f.close()  # 关闭文件

    f = open(txt_path2, "r", encoding='UTF-8')  # 设置文件对象
    list2 = f.readlines()  # 直接将文件中按行读到list里，效果与方法2一样
    f.close()  # 关闭文件f = open(txt_path0, "r", encoding='UTF-8')  # 设置文件对象

    f = open(txt_path3, "r", encoding='UTF-8')  # 设置文件对象
    list3 = f.readlines()  # 直接将文件中按行读到list里，效果与方法2一样
    f.close()  # 关闭文件

    f = open(txt_path4, "r", encoding='UTF-8')  # 设置文件对象
    list4 = f.readlines()  # 直接将文件中按行读到list里，效果与方法2一样
    f.close()  # 关闭文件

    f = open(txt_path5, "r", encoding='UTF-8')  # 设置文件对象
    list5 = f.readlines()  # 直接将文件中按行读到list里，效果与方法2一样
    f.close()  # 关闭文件

    f = open(txt_path6, "r", encoding='UTF-8')  # 设置文件对象
    list6 = f.readlines()  # 直接将文件中按行读到list里，效果与方法2一样
    f.close()  # 关闭文件

    sentences = []
    nn = min(len(list0),len(list1),len(list2),len(list3),len(list4),len(list5),len(list6)) - 1  # 设置数据量
    nn = 461
    nnt = nn * 7
    nk = 1
    n0, n1, n2, n3, n4, n5, n6 = 0, 0, 0, 0, 0, 0, 0
    while nk <= nnt:
        flag_t = random.randint(0, 6)  # 随机数
        nk += 1
        if flag_t == 0:
            if n0 < nn:
                sentences.append(list0[n0])
            else:
                nk -= 1
            n0 += 1
        elif flag_t == 1:
            if n1 < nn:
                sentences.append(list1[n1])
            else:
                nk -= 1
            n1 += 1
        elif flag_t == 2:
            if n2 < nn:
                sentences.append(list2[n2])
            else:
                nk -= 1
            n2 += 1
        elif flag_t == 3:
            if n3 <= nn:
                sentences.append(list3[n3])
            else:
                nk -= 1
            n3 += 1
        elif flag_t == 4:
            if n4 <= nn:
                sentences.append(list4[n4])
            else:
                nk -= 1
            n4 += 1
        elif flag_t == 5:
            if n5 <= nn:
                sentences.append(list5[n5])
            else:
                nk -= 1
            n5 += 1
        elif flag_t == 6:
            if n6 <= nn:
                sentences.append(list6[n6])
            else:
                nk -= 1
            n6 += 1
    list2txt(sentences,r'C:\Users\songwannian\Desktop\T.txt')

def entropy_1():
    """处理数据集,将桌面1256文件夹里面的数据换成你处理过的数据集"""

    txt_path0 = r'C:\Users\songwannian\Desktop\1256\0.txt'
    txt_path1 = r'C:\Users\songwannian\Desktop\1256\1.txt'
    txt_path2 = r'C:\Users\songwannian\Desktop\1256\2.txt'
    txt_path3 = r'C:\Users\songwannian\Desktop\1256\3.txt'
    txt_path4 = r'C:\Users\songwannian\Desktop\1256\4.txt'
    txt_path5 = r'C:\Users\songwannian\Desktop\1256\5.txt'
    txt_path6 = r'C:\Users\songwannian\Desktop\1256\6.txt'

    f = open(txt_path0, "r", encoding='UTF-8')  # 设置文件对象
    list0 = f.readlines()  # 直接将文件中按行读到list里，效果与方法2一样
    f.close()  # 关闭文件

    f = open(txt_path1, "r", encoding='UTF-8')  # 设置文件对象
    list1 = f.readlines()  # 直接将文件中按行读到list里，效果与方法2一样
    f.close()  # 关闭文件

    f = open(txt_path2, "r", encoding='UTF-8')  # 设置文件对象
    list2 = f.readlines()  # 直接将文件中按行读到list里，效果与方法2一样
    f.close()  # 关闭文件f = open(txt_path0, "r", encoding='UTF-8')  # 设置文件对象

    f = open(txt_path3, "r", encoding='UTF-8')  # 设置文件对象
    list3 = f.readlines()  # 直接将文件中按行读到list里，效果与方法2一样
    f.close()  # 关闭文件

    f = open(txt_path4, "r", encoding='UTF-8')  # 设置文件对象
    list4 = f.readlines()  # 直接将文件中按行读到list里，效果与方法2一样
    f.close()  # 关闭文件

    f = open(txt_path5, "r", encoding='UTF-8')  # 设置文件对象
    list5 = f.readlines()  # 直接将文件中按行读到list里，效果与方法2一样
    f.close()  # 关闭文件

    f = open(txt_path6, "r", encoding='UTF-8')  # 设置文件对象
    list6 = f.readlines()  # 直接将文件中按行读到list里，效果与方法2一样
    f.close()  # 关闭文件

    sentences = []

    n0, n1, n2, n3, n4, n5, n6 = len(list0), len(list1), len(list2), len(list3), len(list4), len(list5), len(list6)
    nk0, nk1, nk2, nk3, nk4, nk5, nk6 = 0,0,0,0,0,0,0
    n_total = n0+n1+n2+n3+n4+n5+n6
    nk_total = 0
    while nk_total <= n_total:
        flag_t = random.randint(0, 6)  # 随机数
        if flag_t == 0:
            if nk0 < n0:
                sentences.append(list0[nk0])
                nk0 += 1
        elif flag_t == 1:
            if nk1 < n1:
                sentences.append(list1[nk1])
                nk1 += 1
        elif flag_t == 2:
            if nk2 < n2:
                sentences.append(list2[nk2])
                nk2 += 1
        elif flag_t == 3:
            if nk3 < n3:
                sentences.append(list3[nk3])
                nk3 += 1
        elif flag_t == 4:
            if nk4 < n4:
                sentences.append(list4[nk4])
                nk4 += 1
        elif flag_t == 5:
            if nk5 < n5:
                sentences.append(list5[nk5])
                nk5 += 1
        elif flag_t == 6:
            if nk6 < n6:
                sentences.append(list6[nk6])
                nk6 += 1
        nk_total+=1
    list2txt(sentences,r'C:\Users\songwannian\Desktop\T1.txt')


if __name__ == '__main__':
    # 批量处理
    # filter_path = r'C:\Users\songwannian\Desktop\1'
    # papers_check_0(filter_path)
    # papers_check_1(filter_path)
    # papers_check_2(filter_path)
    # papers_check_3(filter_path)
    # papers_check_4(filter_path)
    # papers_check_41(filter_path)
    # papers_check_5(filter_path)
    # papers_check_6(filter_path)

    # path1 = 'E:\\NLP\\02 Database\\Document\\非法采伐、毁坏国家重点保护植物罪(新)\\docx\\宋元坤非法采伐国家重点保护植物罪一审刑事判决书.docx'
    # paper_check(path1)

    # 数据集数据处理
    entropy_1()