"""单个文件等级地处理"""
# 程序实现：1.传入一个路径(doc或docx文件路径，系统会自动判断是doc文件还是docx文件，doc文件会转换为docx文件），在本路径下生成同文件名json文件。2.传入一个路径，返回一个列表（内嵌套固定类型字典）。

import os
import json
from process_doc import doc2docx_1, read_docx


# 通过文件路径解析信息（txt文件编码类型为ANSI），获取案件名（文件名）、案由、案件类型、文书类型
def case_name(filepath, anyoutxt, leixingtxt, papertypetxt, casetypetxt):
    # 获取案件名
    (path, filename) = os.path.split(filepath)
    (casename, ext) = os.path.splitext(filename)
    print(f"正在抽取：{filename}")
    # 获取案由
    anyou = ''
    f01 = open(anyoutxt, "r")  # 设置文件对象，其中txt文件编码类型为ANSI
    data01 = f01.readlines()  # 直接将文件中按行读到list里，效果与方法2一样
    f01.close()  # 关闭文件
    for ay in data01:
        ay = ay.replace('\n', '')  # 删除回车
        if ay in casename:
            anyou = ay
    # 获取审理程序
    chengxu = ''
    f02 = open(leixingtxt, "r")  # 设置文件对象
    data02 = f02.readlines()  # 直接将文件中按行读到list里，效果与方法2一样
    f02.close()  # 关闭文件
    for ay in data02:
        ay = ay.replace('\n', '')  # 删除回车
        if ay in casename:
            chengxu = ay
    # 获取文书类型
    papertype = ''
    f03 = open(papertypetxt, "r")  # 设置文件对象
    data03 = f03.readlines()  # 直接将文件中按行读到list里，效果与方法2一样
    f03.close()  # 关闭文件
    for ay in data03:
        ay = ay.replace('\n', '')  # 删除回车
        if ay in casename:
            papertype = ay
    # 获取诉讼程序
    casetype = ''
    f04 = open(casetypetxt, "r")  # 设置文件对象
    data04 = f04.readlines()  # 直接将文件中按行读到list里，效果与方法2一样
    f04.close()  # 关闭文件
    for ay in data04:
        ay = ay.replace('\n', '')  # 删除回车
        if ay in casename:
            casetype = ay
    if casename =='':
        print('未找到案件名')
        casename = 'void'
    if anyou == '':
        print("未找到案由！")
        anyou = 'void'
    if chengxu == '':
        print("匹配审理程序失败！")
        chengxu = 'void'
    if papertype == '':
        print("解析文书类型失败！")
        papertype = 'void'
    if casetype == '':
        print("解析案件类型失败！")
        casetype = 'void'
    return (casename, anyou, chengxu, papertype, casetype) # 后两项仅用于传入case_base_information函数


# 传入读取的文件段落列表,获取案件基本信息:法院，文书性质，案号,判决日期
def case_base_information(paras, papertype, casetype, papertypetxt, casetypetxt):
    case_court = paras[0]
    type = paras[1]
    case_number = paras[2]
    # 变量名分配
    prosecution_organ = ''   # 公诉机关
    part_people_index0 = 0   # 参与人第一段索引(初始化
    part_people_index1 = 0   # 参与人最后一段索引(初始化
    law_index0 = 0  # 相关法律初始段（初始化
    defendants = [] # 被告人
    law_relate = []
    # 获取文书类型
    if papertype == 'void':
        f03 = open(papertypetxt, "r")  # 设置文件对象
        data03 = f03.readlines()  # 直接将文件中按行读到list里，效果与方法2一样
        f03.close()  # 关闭文件
        for ay in data03:
            ay = ay.replace('\n', '')  # 删除回车
            if ay in type:
                papertype = ay
    # 获取诉讼程序
    if casetype == 'void':
        f04 = open(casetypetxt, "r")  # 设置文件对象
        data04 = f04.readlines()  # 直接将文件中按行读到list里，效果与方法2一样
        f04.close()  # 关闭文件
        for ay in data04:
            ay = ay.replace('\n', '')  # 删除回车
            if ay in type:
                casetype = ay
    # 遍历检索
    judge_day = 'void'
    for p in paras:
        # 提取公诉机关（检察院）
        if '公诉机关' in p:
            if len(prosecution_organ) <= 0:
                prosecution_organ = p.replace('公诉机关','')
                prosecution_organ = prosecution_organ.replace('。','')
                part_people_index0 = paras.index(p) + 1
        # 案由段，暂时未提取！！！！！！！
        elif '已审理终结' in p:
            anyou = p
        if '年' and '月' and '日' in p:
            if len(p) <= 12:
                judge_day = p
        # 相关法律条文起始段索引
        if '法律条文' in p:
            law_index0 = paras.index(p)
        if (len(prosecution_organ) > 0) and ((prosecution_organ and '指控') in p) and part_people_index1==0 :
            part_people_index1 = paras.index(p) - 1
    # 提取被告人信息（包括辩护人）
    while part_people_index0 <= part_people_index1:
        defendants.append(paras[part_people_index0])
        part_people_index0 += 1
    # 相关法律条文
    if law_index0 > 0:
        while law_index0 < len(paras):
            law_relate.append(paras[law_index0])
            law_index0 += 1
    if prosecution_organ == '':
        print('未提取到公诉机关')
        prosecution_organ = 'void'
    if defendants == []:
        print('未提取到被告人信息')
        defendants.append('void')
    if law_relate == []:
        print('文书未附相关法律条文')
        law_relate.append('void')
    if judge_day == 'void':
        print('提取判决日期失败')
    return (papertype, casetype, case_court, case_number, judge_day, defendants, prosecution_organ, law_relate)


# 将信息存入字典（在此设置字典）（暂时不用）
def information_dict(casename, anyou, chengxu, papertype, casetype, fayuan, wenshuleixing, anhao, panjueriqi, beigaoren, gongsuren):
    info_dict_temp = {'案件名': casename,  '案号':anhao, '案由':anyou, '程序': chengxu, '文书类型':papertype,
                      '案件类型': casetype, '法院':fayuan, '文书类型':wenshuleixing,
                      '判决日期': panjueriqi, '被告人':beigaoren, '公诉人':gongsuren
                      }
    return info_dict_temp


# 将信息存入列表（内嵌套字典）
def information_list(casename, anyou, chengxu, papertype, anjianleixing,
                        fayuan, anhao, panjueriqi, beigaoren, gongsuren, law_ralated):
    info_list = [
        {'案件名': casename}, {'案由': anyou}, {'程序': chengxu},
        {'文书类型': papertype}, {'案件类型': anjianleixing},
        {'法院': fayuan}, {'案号':anhao},
        { '判决日期': panjueriqi}, {'被告人': beigaoren}, { '公诉人':gongsuren}, {'相关法律': law_ralated}
    ]
    return info_list


# 字典转json文件（savefile_load是文件夹路径）
def dict2json(info_dict, savefile_load, casename):
    b = json.dumps(info_dict, ensure_ascii=False)
    savefile_load = savefile_load + '/' + casename + '.json'
    f2 = open(savefile_load, 'w')
    f2.write(b)
    f2.close()


def list_output(file_path):
    if os.path.splitext(file_path)[-1] == ".doc":  # 判断文件类型是否为doc
        print('传入文件格式为doc，将转换为docx格式。')
        doc2docx_1(file_path)
        file_path = file_path + 'x'
    # 设置引用文件路径（因为后期可能要更新相应信息，所以采用此种方式更方便一些）
    anyoutxt = 'D:/projects_pycharm/LawProcess/data_access/data/anyou.txt'
    leixingtxt = 'D:/projects_pycharm/LawProcess/data_access/data/chengxu.txt'
    papertypetxt = 'D:/projects_pycharm/LawProcess/data_access/data/paper_type.txt'
    casetypetxt = 'D:/projects_pycharm/LawProcess/data_access/data/case_type.txt'

    (casename, anyou, chengxu, papertype0, casetype0) = \
        case_name(file_path, anyoutxt, leixingtxt, papertypetxt, casetypetxt)

    paras = read_docx(file_path)  # 读取文书段落

    (papertype, casetype, fayuan, anhao, panjueriqi, beigaoren, gongsuren, law_ralated) \
        = case_base_information(paras, papertype0, casetype0, papertypetxt, casetypetxt)  # 读取基本信息

    info_list = information_list(casename, anyou, chengxu, papertype, casetype, fayuan, anhao,
                                 panjueriqi, beigaoren, gongsuren, law_ralated)
    return info_list


if __name__ == '__main__':
    path = 'E:\\NLP\\02 Database\\Document\\非法采伐、毁坏国家重点保护植物罪(新)\\docx\\蔡某非法采伐国家重点保护植物一审刑事判决书.docx'
    info_list = list_output(path)
    for i in info_list:
        print(i)