"""单个文件等级地处理,extract_list重构"""
# 程序实现：段落标注
import json
import os
from process_doc import paras2sentences_ltp, list2txt,read_docx


# 传入文件段落和案件名（文件名），输出字典
def paras_label(paras, case_name):
    paras.insert(0, case_name)
    dict_label = {'label00': paras[0], 'label01': paras[1], 'label02': paras[2], 'label03': paras[3]}
    pn = len(paras)  # 总段落数（已经去除了空行）
    pi = len(dict_label)  # 动态索引（正常为5
    # 判断paras[4]是否为公诉机关信息
    if '公诉机关' in paras[4]:  # 先按顺序提取
        save_t = paras[4]
        part_people_index0 = 5
        if 12 < len(paras[5]):
            kp = 12
        else:
            kp = (paras[5])
        pa1 = paras[5][0:kp]  # 检查公益诉讼的情况
        if ('附带' or '民事公益' or '公益诉讼' or '民事诉讼') in pa1:
            save_t = paras[4]+'<con>'+paras[5]
            part_people_index0 = 6
        dict_label['label04'] = save_t
    else:
        part_people_index0 = 4
    # 遍历检索关键索引
    part_people_index1 = 0  # 初始化
    law_index0 = 0  # 法律条文开始段落
    prosecution_organ = ''  # 公诉机关
    accuse_index0 = 0  # 指控段落索引
    fact_index0 = 0  # 法院认为
    adjudicatory_index0 = 0
    judge_day_index = 0  # 审判日期索引初始化
    for p in paras:
        # 提取公诉机关（检察院）
        if '公诉机关' in p:
            if len(prosecution_organ) <= 0:
                prosecution_organ = p.replace('公诉机关', '')
                prosecution_organ = prosecution_organ.replace('。', '')
        # 指控段和被告人末尾段索引
        if (len(prosecution_organ) > 0) and ((prosecution_organ and '指控') in p) and part_people_index1 == 0:
            accuse_index0 = paras.index(p)
            part_people_index1 = accuse_index0 - 1
        # 本院认为
        if '本院认为' in p:
            fact_index0 = paras.index(p)
        # 判决日期
        if '年' and '月' and '日' in p:
            if len(p) <= 12:
                judge_day_index = paras.index(p)
        # 相关法律条文起始段索引
        if '相关法律' in p or '法律条文' in p:
            law_index0 = paras.index(p)
        if '审判员' in p:
            if adjudicatory_index0 == 0:
                adjudicatory_index0 = paras.index(p)
    # 标注被告人信息（包括辩护人）
    if part_people_index0 == part_people_index1:  # 被告人只有一段的情况
        dict_label['label05'] = paras[part_people_index0]
    else:
        defendants = ''
        pi = part_people_index0
        while pi <= part_people_index1:
            if defendants == '' :
                defendants = paras[pi]
            else:
                defendants = defendants + '<con>' + paras[pi]   # 每段之间用<con>连接
            pi += 1
        dict_label['label05'] = defendants
    # 标注起诉信息
    accuse_index1 = fact_index0 - 1
    if accuse_index0 == accuse_index1:
        dict_label['label06'] = paras[accuse_index0]
    else:
        accuse = ''
        pi = accuse_index0
        while pi <= accuse_index1:
            if accuse == '':
                accuse = paras[pi]
            else:
                accuse = accuse + '<con>' + paras[pi]   # 每段之间用<con>连接
            pi += 1
        dict_label['label06'] = accuse
    # 审判人员信息
    if judge_day_index != 0:
        ain1 = judge_day_index  # 向前检索
        while ain1 >= judge_day_index - 7:
            pa1 = paras[ain1]
            pa1.replace(" ", "")
            if len(pa1) <= 12:
                adjudicatory_index0 = ain1
            else:
                break
            ain1 -= 1

        ain2 = judge_day_index  # 向后检索
        # 添加判断是否附法律条文的信息
        while ain2 <= len(paras)-1:
            pa2 = paras[ain2]
            pa2.replace(" ", "")
            if len(pa2) <= 12:
                break_flag = 0
                list_t = ['法律', '条文', ':', '相关']
                for t in list_t:
                    if t in pa2:
                        break_flag = 1
                        break
                if break_flag == 1:
                    break
                adjudicatory_index1 = ain2
            else:
                break
            ain2 += 1
        adjudicatory = ''
        pi = adjudicatory_index0
        while pi <= adjudicatory_index1:
            if adjudicatory == '':
                adjudicatory = paras[pi]
            else:
                adjudicatory = adjudicatory + '<con>' + paras[pi]  # 每段之间用<con>连接
            pi += 1
        dict_label['label08'] = adjudicatory
    else:
        adjudicatory_index1 = law_index0 - 1
        if adjudicatory_index0 == adjudicatory_index1:
            dict_label['label08'] = paras[adjudicatory_index0]
        else:
            adjudicatory = ''
            pi = adjudicatory_index0
            while pi <= adjudicatory_index1:
                if adjudicatory == '' :
                    adjudicatory = paras[pi]
                else:
                    adjudicatory = adjudicatory + '<con>' + paras[pi]   # 每段之间用<con>连接
                pi += 1
            dict_label['label08'] = adjudicatory
    # 法院认定事实和判决
    fact_index1 = adjudicatory_index0 - 1  # 依赖于审判人员段落
    if fact_index0 == fact_index1:
        dict_label['label07'] = paras[fact_index0]
    else:
        fact = ''
        pi = fact_index0
        while pi <= fact_index1:
            if fact == '':
                fact = paras[pi]
            else:
                fact = fact + '<con>' + paras[pi]   # 每段之间用<con>连接
            pi += 1
        dict_label['label07'] = fact
    # 相关法律条文
    laws = ''
    if law_index0 > 0:
        pi = law_index0
        while pi < len(paras):
            if laws == '':
                laws = paras[pi]
            else:
                laws = laws + '<con>' + paras[pi]
            pi += 1
        dict_label['label09'] = laws
    return dict_label


# 传入段落标签字典自动句子标记,返回类型为列表
def sentence_tag(dict_label):
    sentence72 = []
    sentence82 = []
    sentence92 = []
    sentences = []
    for i, k in dict_label.items():  # i是标签，k是字符串
        if "<con>" in k:
            k = k.split('<con>')  # 将段落拆开
        if i == 'label00':
            sentences.append(k + '\t0\n')
        elif i == 'label01':
            sentences.append(k + '\t1\n')
        elif i == 'label02':
            sentences.append(k + '\t2\n')
        elif i == 'label03':
            sentences.append(k + '\t3\n')
        elif i == 'label04':
            if isinstance(k, str):  # 判断数据格式
                sentences.append(k + '\t4\n')
            elif isinstance(k, list):
                k = paras2sentences_ltp(k)
                for ki in k:
                    sentences.append(ki + '\t4\n')
        elif i == 'label05':
            if isinstance(k, str):  # 判断数据格式
                sentences.append(k + '\t5\n')
            elif isinstance(k, list):
                k = paras2sentences_ltp(k)
                for ki in k:
                    sentences.append(ki + '\t5\n')
        elif i == 'label06':
            if isinstance(k, str):
                sentences.append(k + '\t6\n')
            elif isinstance(k, list):
                k = paras2sentences_ltp(k)
                for ki in k:
                    sentences.append(ki + '\t6\n')
        elif i == 'label07':
            if isinstance(k, str):
                sentence71 = k + '\t7\n'
            elif isinstance(k, list):
                k = paras2sentences_ltp(k)
                for ki in k:
                    sentence72.append(ki + '\t7\n')
        elif i == 'label08':
            if isinstance(k, str):
                sentence81 = k + '\t8\n'
            elif isinstance(k, list):
                k = paras2sentences_ltp(k)
                for ki in k:
                    sentence82.append(ki + '\t8\n')
        elif i == 'label09':
            if isinstance(k, str):
                sentence92 = k + '\t9\n'
            elif isinstance(k, list):
                k = paras2sentences_ltp(k)
                for ki in k:
                    sentence92.append(ki + '\t9\n')
    if len(sentence72) > 0:
        for s72 in sentence72:
            sentences.append(s72)
    if len(sentence82) > 0:
        for s82 in sentence82:
            sentences.append(s82)
    if len(sentence92) > 0:
        for s92 in sentence92:
            sentences.append(s92)
    return sentences


# 抽取特定一个标签的段落进行存储，且只存储第一句
def sentence_tag_s(dict_label, s):
    sentences = []
    for i, k in dict_label.items():  # i是标签，k是字符串
        if "<con>" in k:
            k = k.split('<con>')  # 将段落拆开
        if s == 0:
            if i == 'label00':
                k = k.replace('.docx', '')
                sentences.append(k + '\t0\n')
        elif s == 1:
            if i == 'label01':
                sentences.append(k + '\t1\n')
        elif s == 2:
            if i == 'label02':
                sentences.append(k + '\t2\n')
        elif s == 3:
            if i == 'label03':
                sentences.append(k + '\t3\n')
        elif s == 4:
            if i == 'label04':
                k = k.replace('。', '')
                sentences.append(k + '\t4\n')
        elif s == 5:
            if i == 'label05':
                if isinstance(k, str):  # 判断数据格式
                    k_t = [k]
                    k_t = paras2sentences_ltp(k_t)
                    nk = 0  # 只存储第一句
                    for ki in k_t:
                        if nk == 1:
                            break
                        sentences.append(ki + '\t5\n')
                        nk += 1
                elif isinstance(k, list):
                    k = paras2sentences_ltp(k)
                    nk = 0  # 只存储第一句
                    for ki in k:
                        if nk == 1:
                            break
                        sentences.append(ki + '\t5\n')
                        nk += 1
        elif s == 6:
            if i == 'label06':
                if isinstance(k, str):
                    sentences.append(k + '\t6\n')
                elif isinstance(k, list):
                    k = paras2sentences_ltp(k)
                    nk = 0  # 只存储第一句
                    for ki in k:
                        if nk == 1:
                            break
                        sentences.append(ki + '\t6\n')
                        nk += 1
        elif s == 7:
            if i == 'label07':
                if isinstance(k, str):
                    sentence71 = k + '\t7\n'
                elif isinstance(k, list):
                    k = paras2sentences_ltp(k)
                    nk = 0  # 只存储第一句
                    for ki in k:
                        if nk == 1:
                            break
                        sentences.append(ki + '\t7\n')
                        nk += 1
        elif s == 8:
            if i == 'label08':
                if isinstance(k, str):
                    sentence81 = k + '\t8\n'
                elif isinstance(k, list):
                    k = paras2sentences_ltp(k)
                    nk = 0  # 只存储第一句
                    for ki in k:
                        if nk == 1:
                            break
                        sentences.append(ki + '\t8\n')
                        nk += 1
        elif s == 9:
            if i == 'label09':
                if isinstance(k, str):
                    sentence92 = k + '\t9\n'
                elif isinstance(k, list):
                    k = paras2sentences_ltp(k)
                    nk = 0  # 只存储第一句
                    for ki in k:
                        if nk == 1:
                            break
                        sentences.append(ki + '\t9\n')
                        nk += 1
        else:
            print('请输入正确格式的标签，例如“0”。')
    sentence = sentences[0]
    return sentence


# 字典转json文件（savefile_load是文件夹路径）
def dict2json(info_dict, savefile_load, casename):
    b = json.dumps(info_dict, ensure_ascii=False)
    savefile_load = savefile_load + '/' + casename + '.json'
    f2 = open(savefile_load, 'w')
    f2.write(b)
    f2.close()


if __name__ == '__main__':
    # 多文档标注测试   Ctrl + /
    # list4 = []
    # list5 = []
    # list6 = []
    # path = 'E:\\NLP\\02 Database\\Document\\非法采伐、毁坏国家重点保护植物罪(新)\\docx'
    # path_list = os.listdir(path)
    # nn = 0  # 文件总数
    # n00 = n01 = n02 = n03 = n04 = n05 = n06 = n07 = n08 = n09 = 0  # 计数
    # for pl in path_list:
    #     filename_t, type_t = os.path.splitext(pl)
    #     if type_t != '.docx':   # 过滤文件类型
    #         continue
    #     path_temp = os.path.join(path, pl)
    #     paras = read_docx(path_temp)
    #     labels = paras_label(paras, pl)  # 打开一个文件
    #     sentences = sentence_tag(labels)
    #     nn += 1
    #     len_h = 2  # 假设有文字的段落的长度
    #     print(f"{nn}")
    #     # 数据统计
    #     for i, k in labels.items():
    #         print(f"{i}:{k}")
    #         if i == 'label00':
    #             if len(k) >= len_h:
    #                 n00 += 1
    #         elif i == 'label01':
    #             if len(k) >= len_h:
    #                 n01 += 1
    #         elif i == 'label02':
    #             if len(k) >= len_h:
    #                 n02 += 1
    #         elif i == 'label03':
    #             if len(k) >= len_h:
    #                 n03 += 1
    #         elif i == 'label04':
    #             if len(k) >= len_h:
    #                 n04 += 1
    #             else:
    #                 list4.append(labels["label00"])
    #         elif i == 'label05':
    #             if len(k) >= len_h:
    #                 n05 += 1
    #             else:
    #                 list5.append(labels["label00"])
    #         elif i == 'label06':
    #             if len(k) >= len_h:
    #                 n06 += 1
    #             else:
    #                 list6.append(labels["label00"])
    #         elif i == 'label07':
    #             if len(k) >= len_h:
    #                 n07 += 1
    #         elif i == 'label08':
    #             if len(k) >= len_h:
    #                 n08 += 1
    #         elif i == 'label09':
    #             if len(k) >= len_h:
    #                 n09 += 1
    #         else:
    #             continue
    # print(f"共计{nn}篇文书")
    # recall_rate00 = n00 / nn  # 计算召回率
    # recall_rate01 = n01 / nn
    # recall_rate02 = n02 / nn
    # recall_rate03 = n03 / nn
    # recall_rate04 = n04 / nn
    # recall_rate05 = n05 / nn
    # recall_rate06 = n06 / nn
    # recall_rate07 = n07 / nn
    # recall_rate08 = n08 / nn
    # recall_rate09 = n09 / nn
    # print(f"label00:{recall_rate00 * 100}%")
    # print(f"label01:{recall_rate01 * 100}%")
    # print(f"label02:{recall_rate02 * 100}%")
    # print(f"label03:{recall_rate03 * 100}%")
    # print(f"label04:{recall_rate04 * 100}%")
    # print(f"label05:{recall_rate05 * 100}%")
    # print(f"label06:{recall_rate06 * 100}%")
    # print(f"label07:{recall_rate07 * 100}%")
    # print(f"label08:{recall_rate08 * 100}%")
    # print(f"label09:{recall_rate09 * 100}%")
    # list2txt(list4, 'C:\\Users\\songwannian\\Desktop\\list4.txt')  # 将列表存储为.txt文件
    # list2txt(list5, 'C:\\Users\\songwannian\\Desktop\\list5.txt')  # 将列表存储为.txt文件
    # list2txt(list6, 'C:\\Users\\songwannian\\Desktop\\list6.txt')  # 将列表存储为.txt文件

    # 批量文件句子标注处理(分开存储文件)
    # path = 'E:\\NLP\\02 Database\\Document\\非法采伐、毁坏国家重点保护植物罪(新)\\docx'
    # txt_path = 'E:\\NLP\\02 Database\\Document\\非法采伐、毁坏国家重点保护植物罪(新)\\txt'
    # path_list = os.listdir(path)
    # for pl in path_list:
    #     filename_t, type_t = os.path.splitext(pl)
    #     if type_t != '.docx':  # 过滤文件类型
    #         continue
    #     path_temp = os.path.join(path, pl)
    #     name = pl.split('.')
    #     paras = read_docx(path_temp)
    #     labels = paras_label(paras, pl)
    #     sentences = sentence_tag(labels)
    #     list2txt(sentences, os.path.join(txt_path, name[0] + '.txt'))  # 将列表存储为.txt文件

    # 批量文件句子标注存储
    path = 'E:\\NLP\\02 Database\\Document\\非法采伐、毁坏国家重点保护植物罪(新)\\docx'
    path_list = os.listdir(path)
    sentences = []
    for pl in path_list:
        filename_t, type_t = os.path.splitext(pl)
        if type_t != '.docx':  # 过滤文件类型
            continue
        path_temp = os.path.join(path, pl)
        name = pl.split('.')
        paras = read_docx(path_temp)
        labels = paras_label(paras, pl)
        # 存储指定范围段落至一个文件
        n = 0
        while n <= 7:
            if n != 5:  # 过滤标签
                n += 1
                continue
            sentence_t = sentence_tag_s(labels, n)  # 句子标注(只标注一个标签的第一句话)
            if not ('被告人' in sentence_t):
                sentence_t = sentence_t.replace('\n', '')
                sentence_t = sentence_t + f"{filename_t}\n"
                sentences.append(sentence_t)
                n += 1
                continue
            n += 1
    list2txt(sentences, "C:\\Users\\songwannian\\Desktop\\5_erro.txt")  # 将列表存储为.txt文件

    # 单文档标注测试
    # path1 = 'E:\\NLP\\02 Database\\Document\\非法采伐、毁坏国家重点保护植物罪(新)\\docx\\双桦人民检察院诉郑树利非法采伐国家重点保护植物一案一审刑事判决书.docx'
    # paras1 = read_docx(path1)
    # labels1 = paras_label(paras1, '文件名')
    # for i, k in labels1.items():
    #     print(f"{i}:{k}")
    # sentences = sentence_tag(labels1)
    # list2txt(sentences, 'C:\\Users\\songwannian\\Desktop\\1.txt')  # 将列表存储为.txt文件
    # for s in sentences:
    #     print(s)
