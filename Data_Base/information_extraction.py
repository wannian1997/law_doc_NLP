import os

from utils import minDistance
from Data_Access.Paper import Paper


class PaperInfo(Paper):
    """对裁判文书进行信息抽取"""
    # 状态信息

    # paper_info 表格信息
    case_ID = ''
    cause_of_action = ''
    paper_name = ''
    court = ''
    paper_type = ''
    prosecution = ''   # 原告，检察院
    indictment_ID = ''  # 起诉书编号
    time_of_case = ''  # 起诉日期
    date = ''  # 裁判文书判决日期

    def __init__(self, docx_path):
        super().__init__(docx_path)  # 调用父类的构造函数
        self.extract_paper_info()

    def extract_paper_info(self):
        self.case_ID = self.paras[self.dict_label['label30'][0]]
        self.cause_of_action = self.cause_of_action_func()
        self.paper_name = self.case_name
        self.court = self.paras[self.dict_label['label10'][0]]
        self.paper_type = self.paras[self.dict_label['label20'][0]]
        self.prosecution = self.prosecution_func()
        self.indictment_ID = self.indictment_ID_func()
        pass

    def cause_of_action_func(self):
        """提取案由"""
        # 处理文件名，去掉路径信息
        dir, file_name = os.path.split(self.case_name)
        self.case_name = file_name.split('.')[0]

        # 通过文本匹配算法进行案由抽取
        anyou = ''
        f01 = open(r'..\Data_Access\data\anyou.txt', "r")  # 设置文件对象，其中txt文件编码类型为ANSI
        all_cause_of_action = f01.readlines()  # 直接将文件中按行读到list里，效果与方法2一样
        f01.close()  # 关闭文件

        # 文本匹配算法（编辑距离）
        all_distance = []
        for ay in all_cause_of_action:
            ay = ay.replace('\n', '')  # 删除回车
            all_distance.append(minDistance(ay, self.case_name))
            if ay[1:len(ay)-1] in self.case_name:
                anyou = ay
        if anyou == '':
            miniDistance = 99999999
            miniDistance_index = -1
            for i in range(len(all_distance)):
                if all_distance[i]<miniDistance:
                    miniDistance_index = i
            anyou = all_cause_of_action[miniDistance_index]
        return anyou.replace('\n', '')

    def prosecution_func(self):
        """提取公诉机关"""
        para = self.paras[self.dict_label['label40'][0]]  # 定位指定段落
        para = para.replace('公诉机关', '')
        para = para.replace('暨附带民事公益诉讼起诉人', '')
        para = para.replace('暨附带公益诉讼起诉人', '')
        para = para.replace('：', '')
        return para

    def indictment_ID_func(self):
        # 获取指控段第一段
        para = str
        for label, paras_index in self.dict_label.items():
            if label[5] == '6':
                print(label,paras_index)
                para = self.paras[paras_index[0]].split()
                break
        print(para)
        return para


def temp(path):
    # 单文档标注测试
    paper = PaperInfo(path)
    for key, value in paper.dict_label.items():
        print(key, value)
    for p in paper.paras:
        print(p)
    # for s in paper.sentences:
    #     print(s)


if __name__ == '__main__':
    path = r'E:\docx\暨附带民非法采伐毁坏国家重点保护植物一审刑事判决书.docx'
    paper_info = PaperInfo(path)
    temp(path)