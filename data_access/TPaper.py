"""面向docx，单个文件等级地处理,extract_label重构"""
import json
import os

from process_doc import paras2sentences, list2txt, read_docx


class TPaper:
    """打开docx文件，并进行段落标注"""

    def __init__(self, docx_path):
        # 索引初始化
        self.part_people_index0 = 0  # 被告人开始段落
        self.part_people_index1 = 0
        self.accuse_index0 = 0  # 指控段落

        # 成员变量
        self.dict_label = {}  # 初始化标注字典※
        self.case_name = docx_path  # 文件名
        self.paras = read_docx(docx_path)  # 文章段落列表※

        # 初始化
        self.paras_label03()  # 标注（并存入标注字典）
        self.paras_label()  # 标注（并存入标注字典）
        self.sentences = self.sentences_tag()  # 句子标注（格式：列表）

    def paras_label03(self):
        """标注标签00-03"""
        self.paras.insert(0, self.case_name)
        self.dict_label = {'label00': [0], 'label01': [1],
                           'label02': [2], 'label03': [3]}
        pn = len(self.paras)  # 总段落数（已经去除了空行）
        pi = len(self.dict_label)  # 动态索引（正常为5）
        # 判断paras[4]是否为公诉机关信息
        if '公诉机关' in self.paras[4]:  # 先按顺序提取
            save_t = [4]
            self.part_people_index0 = 5
            if 12 < len(self.paras[5]):
                kp = 12
            else:
                kp = len(self.paras[5])
            pa1 = self.paras[5][0:kp]  # 检查公益诉讼的情况(大致一句话的范围)
            if not ('被告' in pa1):
                if '公益诉讼' in pa1 or '附带' in pa1 or '民事公益' in pa1 or '民事诉讼' in pa1:
                    save_t.append(5)
                    self.part_people_index0 = 6
            self.dict_label['label04'] = save_t
        else:
            self.part_people_index0 = 4

    def paras_label(self):
        # 遍历检索关键索引
        law_index0 = 0  # 法律条文开始段落
        prosecution_organ = ''  # 公诉机关
        fact_index0 = 0  # 法院认为
        adjudicatory_index0 = 0
        judge_day_index = 0  # 审判日期索引初始化
        for p in self.paras:
            # 提取公诉机关（检察院）
            if '公诉机关' in p:
                if len(prosecution_organ) <= 0:
                    prosecution_organ = p.replace('公诉机关', '')
                    prosecution_organ = prosecution_organ.replace('。', '')
            # 指控段和被告人末尾段索引
            if (len(prosecution_organ) > 0) and ((prosecution_organ and '指控') in p) and self.part_people_index1 == 0:
                self.accuse_index0 = self.paras.index(p)
                self.part_people_index1 = self.accuse_index0 - 1
            # 本院认为
            if '本院认为' in p:
                fact_index0 = self.paras.index(p)
            # 判决日期
            if '年' and '月' and '日' in p:
                if len(p) <= 12:
                    judge_day_index = self.paras.index(p)
            # 相关法律条文起始段索引
            if '相关法律' in p or '法律条文' in p:
                law_index0 = self.paras.index(p)
            if '审判员' in p:
                if adjudicatory_index0 == 0:
                    adjudicatory_index0 = self.paras.index(p)
        # 标注被告人信息（包括辩护人）
        if self.part_people_index0 == self.part_people_index1:  # 被告人只有一段的情况
            self.dict_label['label05'] = [self.part_people_index0]
        else:
            pi = self.part_people_index0
            list_t = []
            while pi <= self.part_people_index1:
                list_t.append(pi)
                pi += 1
            self.dict_label['label05'] = list_t
        # 标注起诉信息
        accuse_index1 = fact_index0 - 1
        if self.accuse_index0 == accuse_index1:
            self.dict_label['label06'] = [self.accuse_index0]
        else:
            list_t = []
            pi = self.accuse_index0
            while pi <= accuse_index1:
                list_t.append(pi)
                pi += 1
            self.dict_label['label06'] = list_t
        # 审判人员信息
        if judge_day_index != 0:
            ain1 = judge_day_index  # 向前检索
            while ain1 >= judge_day_index - 7:
                pa1 = self.paras[ain1]
                pa1.replace(" ", "")
                if len(pa1) <= 12:
                    adjudicatory_index0 = ain1
                else:
                    break
                ain1 -= 1

            ain2 = judge_day_index  # 向后检索
            # 添加判断是否附法律条文的信息
            while ain2 <= len(self.paras) - 1:
                pa2 = self.paras[ain2]
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

            list_t = []
            pi = adjudicatory_index0
            while pi <= adjudicatory_index1:
                list_t.append(pi)
                pi += 1
            self.dict_label['label08'] = list_t
        else:
            adjudicatory_index1 = law_index0 - 1
            if adjudicatory_index0 == adjudicatory_index1:
                self.dict_label['label08'] = [adjudicatory_index0]
            else:
                list_t = []
                pi = adjudicatory_index0
                while pi <= adjudicatory_index1:
                    list_t.append(pi)
                    pi += 1
                self.dict_label['label08'] = list_t
        # 法院认定事实和判决
        fact_index1 = adjudicatory_index0 - 1  # 依赖于审判人员段落
        if fact_index0 == fact_index1:
            self.dict_label['label07'] = [fact_index0]
        else:
            list_t = []
            pi = fact_index0
            while pi <= fact_index1:
                list_t.append(pi)
                pi += 1
            self.dict_label['label07'] = list_t
        # 相关法律条文
        list_t = []
        if law_index0 > 0:
            pi = law_index0
            while pi < len(self.paras):
                list_t.append(pi)
                pi += 1
            self.dict_label['label09'] = list_t

    def sentences_tag(self):
        """传入段落标签字典自动句子标记,返回类型为列表"""
        dict_label = self.dict_label
        sentences = []
        for i, k in dict_label.items():  # i是标签，k是段落列表
            if i == 'label00':
                for ki in k:
                    sentences.append(self.paras[ki] + '\t0\n')
            elif i == 'label01':
                for ki in k:
                    sentences.append(self.paras[ki] + '\t1\n')
            elif i == 'label02':
                for ki in k:
                    sentences.append(self.paras[ki] + '\t2\n')
            elif i == 'label03':
                for ki in k:
                    sentences.append(self.paras[ki] + '\t3\n')
            elif i == 'label04':  # 还需要实现将段落分为句子
                list_tt = []
                for ki in k:
                    list_tt.append(self.paras[ki])
                list_tt = paras2sentences(list_tt)  # 句子元素列表
                for lt in list_tt:
                    sentences.append(lt + '\t4\n')
            elif i == 'label05':
                list_tt = []
                for ki in k:
                    list_tt.append(self.paras[ki])
                list_tt = paras2sentences(list_tt)  # 句子元素列表
                for lt in list_tt:
                    sentences.append(lt + '\t5\n')
            elif i == 'label06':
                list_tt = []
                for ki in k:
                    list_tt.append(self.paras[ki])
                list_tt = paras2sentences(list_tt)  # 句子元素列表
                for lt in list_tt:
                    sentences.append(lt + '\t6\n')
            elif i == 'label07':
                list_tt = []
                for ki in k:
                    list_tt.append(self.paras[ki])
                list_tt = paras2sentences(list_tt)  # 句子元素列表
                for lt in list_tt:
                    sentences.append(lt + '\t7\n')
            elif i == 'label08':
                list_tt = []
                for ki in k:
                    list_tt.append(self.paras[ki])
                list_tt = paras2sentences(list_tt)  # 句子元素列表
                for lt in list_tt:
                    sentences.append(lt + '\t8\n')
            elif i == 'label09':
                list_tt = []
                for ki in k:
                    list_tt.append(self.paras[ki])
                list_tt = paras2sentences(list_tt)  # 句子元素列表
                for lt in list_tt:
                    sentences.append(lt + '\t9\n')
        return sentences

    def sentence_tag_s(self, s):
        """抽取特定一个标签的段落进行存储，且只存储第一句"""
        sentences = []
        for i, k in self.dict_label.items():  # i是标签，k是字符串
            if s == 0:
                if i == 'label00':
                    for ki in k:
                        sentences.append(self.paras[ki] + '\t0\n')
            elif s == 1:
                if i == 'label01':
                    for ki in k:
                        sentences.append(self.paras[ki] + '\t1\n')
            elif s == 2:
                if i == 'label02':
                    for ki in k:
                        sentences.append(self.paras[ki] + '\t2\n')
            elif s == 3:
                if i == 'label03':
                    for ki in k:
                        sentences.append(self.paras[ki] + '\t3\n')
            elif s == 4:
                if i == 'label04':
                    list_tt = []
                    for ki in k:
                        list_tt.append(self.paras[ki])
                    list_tt = paras2sentences(list_tt)  # 句子元素列表
                    for lt in list_tt:
                        sentences.append(lt + '\t4\n')
            elif s == 5:
                if i == 'label05':
                    list_tt = []
                    for ki in k:
                        list_tt.append(self.paras[ki])
                    list_tt = paras2sentences(list_tt)  # 句子元素列表
                    for_flag = True  # 只存储第一句
                    for lt in list_tt:
                        while for_flag:
                            sentences.append(lt + '\t5\n')
                            for_flag = False
            elif s == 6:
                if i == 'label06':
                    list_tt = []
                    for ki in k:
                        list_tt.append(self.paras[ki])
                    list_tt = paras2sentences(list_tt)  # 句子元素列表
                    for_flag = True  # 只存储第一句
                    for lt in list_tt:
                        while for_flag:
                            sentences.append(lt + '\t6\n')
                            for_flag = False
            elif s == 7:
                if i == 'label07':
                    list_tt = []
                    for ki in k:
                        list_tt.append(self.paras[ki])
                    list_tt = paras2sentences(list_tt)  # 句子元素列表
                    for_flag = True  # 只存储第一句
                    for lt in list_tt:
                        while for_flag:
                            sentences.append(lt + '\t7\n')
                            for_flag = False
            elif s == 8:
                if i == 'label08':
                    list_tt = []
                    for ki in k:
                        list_tt.append(self.paras[ki])
                    list_tt = paras2sentences(list_tt)  # 句子元素列表
                    for_flag = True  # 只存储第一句
                    for lt in list_tt:
                        while for_flag:
                            sentences.append(lt + '\t8\n')
                            for_flag = False
            elif s == 9:
                if i == 'label09':
                    list_tt = []
                    for ki in k:
                        list_tt.append(self.paras[ki])
                    list_tt = paras2sentences(list_tt)  # 句子元素列表
                    for_flag = True  # 只存储第一句
                    for lt in list_tt:
                        while for_flag:
                            sentences.append(lt + '\t9\n')
                            for_flag = False
            else:
                print('请输入正确格式的标签，例如“0”。')
        sentence = sentences[0]
        return sentence


if __name__ == '__main__':
    # 批量文件句子标注存储
    path = 'E:\\NLP\\02 Database\\Document\\非法采伐、毁坏国家重点保护植物罪(新)\\docx'
    path_list = os.listdir(path)
    sentences = []
    for pl in path_list:
        filename_t, type_t = os.path.splitext(pl)
        if type_t != '.docx':  # 过滤文件类型
            continue
        path_temp = os.path.join(path, pl)
        paper = TPaper(path_temp)
        # 存储指定范围段落至一个文件
        n = 0
        while n <= 7:
            if n != 5:  # 过滤标签
                n += 1
                continue
            sentence_t = paper.sentence_tag_s(n)  # 句子标注(只标注一个标签的第一句话)
            sentence_t = sentence_t + f"{filename_t}\n"
            sentences.append(sentence_t)
            tt = r'被告[人|单]位?'
            # if not (tt in sentence_t):
            #     sentence_t = sentence_t.replace('\n', '')
            #     sentence_t = sentence_t + f"{filename_t}\n"
            #     sentences.append(sentence_t)
            #     n += 1
            #     continue
            n += 1
    list2txt(sentences, "C:\\Users\\songwannian\\Desktop\\5.txt")  # 将列表存储为.txt文件

    # 单文档标注测试
    # path1 = 'E:\\NLP\\02 Database\\Document\\非法采伐、毁坏国家重点保护植物罪(新)\\docx\\信丰众城矿业有限公司兰某某非法采伐毁坏国家重点保护植物一审刑事判决书.docx'
    # paper = TPaper(path1)
    # dic = paper.dict_label
    # for i, k in dic.items():
    #     print(f"{i}:{k}")
    # list2txt(paper.sentence_tag_s(5), 'C:\\Users\\songwannian\\Desktop\\1.txt')  # 将列表存储为.txt文件
    # print(paper.sentence_tag_s(5))
