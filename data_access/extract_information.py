"""批量处理"""
import os
import json
from extract_list import list_output


# 传入文件路径、案由文件路径（txt文件编码类型为ANSI），获取案件名（文件名）、案由、案件类型、文书类型
def case_name(filepath, anyoutxt, leixingtxt, papertypetxt, casetypetxt):
    # 获取案件名
    (path, filename) = os.path.split(filepath)
    (casename, ext) = os.path.splitext(filename)
    if casename == '':
        print('未找到案件名')
    # 获取案由
    anyou = ''
    f01 = open(anyoutxt, "r")  # 设置文件对象，其中txt文件编码类型为ANSI
    data01 = f01.readlines()  # 直接将文件中按行读到list里，效果与方法2一样
    f01.close()  # 关闭文件
    for ay in data01:
        ay = ay.replace('\n', '')  # 删除回车
        if ay in casename:
            anyou = ay
    if anyou == '':
        print("未找到案由！")
    # 获取审理程序
    chengxu = ''
    f02 = open(leixingtxt, "r")  # 设置文件对象
    data02 = f02.readlines()  # 直接将文件中按行读到list里，效果与方法2一样
    f02.close()  # 关闭文件
    for ay in data02:
        ay = ay.replace('\n', '')  # 删除回车
        if ay in casename:
            chengxu = ay
    if chengxu == '':
        print("匹配审理程序失败！")
    # 获取文书类型
    papertype = ''
    f03 = open(papertypetxt, "r")  # 设置文件对象
    data03 = f03.readlines()  # 直接将文件中按行读到list里，效果与方法2一样
    f03.close()  # 关闭文件
    for ay in data03:
        ay = ay.replace('\n', '')  # 删除回车
        if ay in casename:
            papertype = ay
    if papertype == '':
        print("解析文书类型失败！")
    # 获取案件类型
    casetype = ''
    f04 = open(casetypetxt, "r")  # 设置文件对象
    data04 = f04.readlines()  # 直接将文件中按行读到list里，效果与方法2一样
    f04.close()  # 关闭文件
    for ay in data04:
        ay = ay.replace('\n', '')  # 删除回车
        if ay in casename:
            casetype = ay
    if casetype == '':
        print("解析案件类型失败！")
    return (casename, anyou, chengxu, papertype, casetype)


# 传入读取的文件段落列表,获取案件基本信息:法院，文书性质，案号,判决日期
def case_base_information(paras):
    case_court = paras[0]
    case_type = paras[1]
    case_number = paras[2]
    # 变量名分配
    prosecution_organ = ''
    defendants = []  # 被告人
    # 遍历检索
    for p in paras:
        # 提取公诉机关（检察院）
        if len(prosecution_organ) <= 0:
            if '公诉机关' in p:
                prosecution_organ = p
        # 提取被告人信息
        elif '被告人' and '族' and ('男' or '女') in p:
            defendants.append(p)
        # 案由段，暂时未提取！！！！！！！
        elif '已审理终结' in p:
            anyou = p
        # 提取裁判日期
        elif len(p) <= 12:
            if '年' and '月' and '日' in p:
                judge_day = p
    if prosecution_organ == '':
        print('未提取到公诉机关')
    if defendants == []:
        print('未提取到被告人信息')
    return (case_court, case_type, case_number, judge_day, defendants, prosecution_organ)


# 获取指控段落。效果：仍然无法普遍性提取（暂未使用）
def paragragh_accuse(paras):
    accuse_list = []
    # 找出段落
    paragragh_accuse = 0
    sentence_paragragh = 0
    for p in paras:
        if paragragh_accuse == 0:  # 取第一次出现“指控”的段落
            if '指控' and '罪' in p:
                paragragh_accuse = paras.index(p)
                print(paragragh_accuse)
        if sentence_paragragh == 0:
            if '本院认为' in p:
                sentence_paragragh = paras.index(p)
                print(sentence_paragragh)
    # 拼接段落
    n = paragragh_accuse
    while n < sentence_paragragh:
        accuse_list.append(paras[n])
        n += 1
    return accuse_list  # 返回


# 字典转json文件（savefile_load是文件夹路径）
def dict2json(info_dict, casename, savefile_load):
    b = json.dumps(info_dict, ensure_ascii=False)
    savefile_load = savefile_load + '/' + casename + '.json'
    f2 = open(savefile_load, 'w')
    f2.write(b)
    f2.close()


if __name__ == "__main__":
    # 文件路径
    folder_path0 = "E:\\NLP\\02 Database\\Document\\非法采伐、毁坏国家重点保护植物罪(新)"  # doc文件所在文件夹路径
    docx_path = os.path.join(folder_path0, 'docx')  # docx文件的文件夹
    json_path = os.path.join(folder_path0, 'json')  # json文件的文件夹
    docx_name_list = os.listdir(docx_path)  # 读取docx文件夹下的文件名列表（带后缀）

    # 循环运行部分
    kk = 0
    for dnl in docx_name_list:
        kk += 1
        filepath = os.path.join(folder_path0, 'docx', dnl)
        info_list = list_output(filepath)
        for i in info_list:
            print(i)
    print(kk)  # 处理的文件数
