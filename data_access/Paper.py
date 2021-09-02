"""面向docx，单个文件等级地处理,extract_label重构
2021年7月17日 重新设置标签并改变数据结构"""
from data_access.process_doc import paras2sentences_ltp, list2txt, read_docx
import re


class Paper:
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
        self.list_index_sa = []  # label60处用来统计重复索引

        # 初始化
        self.paras_label30()  # 标注（并存入标注字典）
        self.paras_label()  # 标注（并存入标注字典）
        self.sentences = self.sentences_tag()  # 句子标注（格式：列表）

    def paras_label30(self):
        """标注标签00-30"""
        self.paras.insert(0, self.case_name)
        self.dict_label = {'label00': [0], 'label10': [1],
                           'label20': [2], 'label30': [3]}
        pn = len(self.paras)  # 总段落数（已经去除了空行）
        pi = len(self.dict_label)  # 动态索引（正常为5）
        # 判断paras[4]是否为公诉机关信息
        if len(self.paras) < 5:
            print('发生错误：\n' + '文件格式不符合规范！')
            exit(0)
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
            self.dict_label['label40'] = save_t
        else:
            self.part_people_index0 = 4

    def paras_label(self):
        """2021年7月4日，拟采用检索策略"""
        # 遍历检索关键索引
        prosecution_organ = ''  # 公诉机关
        fact_index0 = 0  # 法院认为
        adjudicatory_index0 = 0
        judge_day_index = 0  # 审判日期索引初始化
        law_index0 = 0  # 法律条文开始段落
        for p in self.paras:
            # 提取公诉机关（检察院）
            if '公诉机关' in p:
                if len(prosecution_organ) <= 0:
                    prosecution_organ_index0 = self.paras.index(p)
                    prosecution_organ = p.replace('公诉机关', '')
                    prosecution_organ = prosecution_organ.replace('。', '')  # 公诉机关提取
                    if len(prosecution_organ) == 0:  # 没提取到
                        prosecution_organ = self.paras[prosecution_organ_index0 + 1]  # 默认下一句就是
                        self.part_people_index0 += 1
                        self.dict_label['label40'].append(prosecution_organ_index0 + 1)

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
            self.dict_label['label50'] = [self.part_people_index0]
        else:
            pi = self.part_people_index0
            list_t = []
            while pi <= self.part_people_index1:
                list_t.append(pi)
                pi += 1
            self.dict_label['label50'] = list_t
        # 标注起诉信息,2021年8月18日细化
        accuse_index1 = fact_index0 - 1
        if self.accuse_index0 == accuse_index1:
            self.dict_label['label60'] = [self.accuse_index0]
        else:
            # 1审判程序，2指控，3辩护意见，4审理查明，5证据，默认未分类
            pi = self.accuse_index0  # 索引
            index_t1, index_t2, index_t3, index_t4, index_t5 = 0, 0, 0, 0, 0  # 关键索引
            while pi <= accuse_index1:  # 遍历
                # 构建正则表达式
                t1 = r'检察院以.*指控.*罪'  # 模式1
                t2 = r'公诉人|机关?.*指控'  # 模式2
                t3 = r'被告人.*(辨称)|(异议)'  # 模式3
                t4 = r'审理.*查明'  # 模式4
                t5 = r'上述事实.*[书物]?证据?'   # 模式5

                if not index_t1:  # 仅获取一次(这里考虑到效率的问题，以下未考虑)
                    if not re.search(t1, self.paras[pi]) is None:  # 模式匹配1
                        index_t1 = pi
                if not re.search(t2, self.paras[pi]) is None:  # 模式匹配2
                    if not index_t2:  # 仅获取一次
                        index_t2 = pi
                if not re.search(t3, self.paras[pi]) is None:  # 模式匹配3
                    if not index_t3:  # 仅获取一次
                        index_t3 = pi
                if not re.search(t4, self.paras[pi]) is None:  # 模式匹配4
                    if not index_t4:  # 仅获取一次
                        index_t4 = pi
                if not re.search(t5, self.paras[pi]) is None:  # 模式匹配5
                    if not index_t5:  # 仅获取一次
                        index_t5 = pi
                pi += 1
            # 解析并储存,存储策略：未提取的不存储，重复的另行解决
            print(f'审判程序1\t指控2\t辩护意见3\t审理查明4\t证据5\n'
                  f'{index_t1}\t\t{index_t2}\t\t{index_t3}\t\t{index_t4}\t\t{index_t5}')  # check

            # 检查index是否存在重复
            list_index = [(1, index_t1), (2, index_t2), (3, index_t3), (4, index_t4), (5, index_t5)]
            index_same1, index_same2, index_same3, index_same4, index_same5 = [], [], [], [], []  # 存储重复的标签
            if index_t1:
                for li in list_index:
                    if 1 == li[0]:  # 跳过自身和自身的比较
                        continue
                    if index_t1 == li[1]:  # 存在重复索引
                        if li[0] == 2:
                            index_same1.append('2')
                            index_t2 = 0
                        elif li[0] == 3:
                            index_same1.append('3')
                            index_t3 = 0
                        elif li[0] == 4:
                            index_same1.append('4')
                            index_t4 = 0
                        elif li[0] == 5:
                            index_same1.append('5')
                            index_t5 = 0
            if index_t2:
                for li in list_index:
                    if 2 == li[0]:  # 跳过自身和自身的比较
                        continue
                    if index_t2 == li[1]:  # 存在重复索引
                        if li[0] == 1:
                            index_same2.append('1')
                            index_t1 = 0
                        elif li[0] == 3:
                            index_same2.append('3')
                            index_t3 = 0
                        elif li[0] == 4:
                            index_same2.append('4')
                            index_t4 = 0
                        elif li[0] == 5:
                            index_same2.append('5')
                            index_t5 = 0
            if index_t3:
                for li in list_index:
                    if 3 == li[0]:  # 跳过自身和自身的比较
                        continue
                    if index_t3 == li[1]:  # 存在重复索引
                        if li[0] == 1:
                            index_same3.append('1')
                            index_t1 = 0
                        elif li[0] == 2:
                            index_same3.append('2')
                            index_t2 = 0
                        elif li[0] == 4:
                            index_same3.append('4')
                            index_t4 = 0
                        elif li[0] == 5:
                            index_same3.append('5')
                            index_t5 = 0
            if index_t4:
                for li in list_index:
                    if 4 == li[0]:  # 跳过自身和自身的比较
                        continue
                    if index_t4 == li[1]:  # 存在重复索引
                        if li[0] == 1:
                            index_same4.append('1')
                            index_t1 = 0
                        elif li[0] == 2:
                            index_same4.append('2')
                            index_t2 = 0
                        elif li[0] == 3:
                            index_same4.append('3')
                            index_t3 = 0
                        elif li[0] == 5:
                            index_same4.append('5')
                            index_t5 = 0
            if index_t5:
                for li in list_index:
                    if 5 == li[0]:  # 跳过自身和自身的比较
                        continue
                    if index_t5 == li[1]:  # 存在重复索引
                        if li[0] == 1:
                            index_same5.append('1')
                            index_t1 = 0
                        elif li[0] == 2:
                            index_same5.append('2')
                            index_t2 = 0
                        elif li[0] == 3:
                            index_same5.append('3')
                            index_t3 = 0
                        elif li[0] == 4:
                            index_same5.append('4')
                            index_t4 = 0

            index_list = []
            if index_t1:
                index_list.append(['1', index_t1])
            if index_t2:
                index_list.append(['2', index_t2])
            if index_t3:
                index_list.append(['3', index_t3])
            if index_t4:
                index_list.append(['4', index_t4])
            if index_t5:
                index_list.append(['5', index_t5])
            # 按索引从小到大排序，解决部分bug
            def takeSecond(elem):
                return elem[1]
            index_list.sort(key=takeSecond)

            print('index_same:\t', index_same1, index_same2, index_same3, index_same4, index_same5)

            # 索引重复统计实现, 仅影响显示，并不影响处理  start
            list_index_sa = []  # 统计列表
            if index_same1:
                list_index_sa.append(['1' + index_same1[0], 1])  # 默认只会出现两个标签重复的情况,否则需要重构
            if index_same2:
                list_index_sa.append(['2' + index_same2[0], 1])
            if index_same3:
                list_index_sa.append(['3' + index_same3[0], 1])
            if index_same4:
                list_index_sa.append(['4' + index_same4[0], 1])
            if index_same5:
                list_index_sa.append(['5' + index_same5[0], 1])
            print('list_index_sa:', list_index_sa)
            self.list_index_sa = list_index_sa  # 格式:[str,str,int]  eg:['1', '3', 1]  依次为标签1,标签2,重复次数  End

            # 存入dic
            print('list_list:\t', index_list)
            len_index_list = len(index_list)
            it = 0
            while it < len_index_list:
                if it == len_index_list - 1:  # 最后一个元素要单独处理
                    list_t = []
                    index_0 = index_list[it][1]  # 获取索引
                    index_1 = accuse_index1
                    while index_0 <= index_1:
                        list_t.append(index_0)
                        index_0 += 1
                    # 后缀标签处理
                    flag_i = index_list[it][0]  # 标签后缀
                    if flag_i == '1':
                        if index_same1:
                            for isa in index_same1:
                                flag_i = flag_i + isa
                    elif flag_i == '2':
                        if index_same2:
                            for isa in index_same2:
                                flag_i = flag_i + isa
                    elif flag_i == '3':
                        if index_same3:
                            for isa in index_same3:
                                flag_i = flag_i + isa
                    elif flag_i == '4':
                        if index_same4:
                            for isa in index_same4:
                                flag_i = flag_i + isa
                    elif flag_i == '5':
                        if index_same5:
                            for isa in index_same5:
                                flag_i = flag_i + isa
                    # 存储
                    self.dict_label[f'label6{flag_i}'] = list_t
                    it += 1
                else:
                    list_t = []
                    index_0 = index_list[it][1]  # 获取索引
                    index_1 = index_list[it + 1][1]
                    # 前后两个索引相同的情况要处理一下
                    if index_0 == index_1:
                        if it + 2 < len_index_list:  # 未超出列表范围
                            index_1 = index_list[it + 2][1]
                            if index_0 == index_1:  # 迭代一次
                                if it + 3 < len_index_list:  # 未超出列表范围
                                    index_1 = index_list[it + 3][1]
                                else:  # 超出列表范围
                                    index_1 = accuse_index1 + 1
                        else:  # 超出列表范围
                            index_1 = accuse_index1 + 1
                    # 存储
                    while index_0 < index_1:
                        list_t.append(index_0)
                        index_0 += 1
                    flag_i = index_list[it][0]  # 标签后缀
                    if index_list[it][0] == '1':
                        if index_same1:
                            for isa in index_same1:
                                flag_i = flag_i + isa
                    elif index_list[it][0] == '2':
                        if index_same2:
                            for isa in index_same2:
                                flag_i = flag_i + isa
                    elif index_list[it][0] == '3':
                        if index_same3:
                            for isa in index_same3:
                                flag_i = flag_i + isa
                    elif index_list[it][0] == '4':
                        if index_same4:
                            for isa in index_same4:
                                flag_i = flag_i + isa
                    elif index_list[it][0] == '5':
                        if index_same5:
                            for isa in index_same5:
                                flag_i = flag_i + isa
                    self.dict_label[f'label6{flag_i}'] = list_t
                    it += 1

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
            list8 = list_t
        else:
            adjudicatory_index1 = law_index0 - 1
            if adjudicatory_index0 == adjudicatory_index1:
                list8 = [adjudicatory_index0]
            else:
                list_t = []
                pi = adjudicatory_index0
                while pi <= adjudicatory_index1:
                    list_t.append(pi)
                    pi += 1
                list8 = list_t
        # 法院认定事实和判决
        fact_index1 = adjudicatory_index0 - 1  # 依赖于审判人员段落
        if fact_index0 == fact_index1:
            list7 = [fact_index0]
        else:
            list_t = []
            pi = fact_index0
            while pi <= fact_index1:
                list_t.append(pi)
                pi += 1
            list7 = list_t
        # 解决label70和label80的顺序问题
        self.dict_label['label70'] = list7
        self.dict_label['label80'] = list8
        # 相关法律条文
        list_t = []
        if law_index0 > 0:
            pi = law_index0
            while pi < len(self.paras):
                list_t.append(pi)
                pi += 1
            self.dict_label['label90'] = list_t

    def sentences_tag(self):
        """传入段落标签字典自动句子标记,返回类型为二维列表，在此函数进行第一步规则"""
        dict_label = self.dict_label
        sentences = []  # 二维数组
        for i, k in dict_label.items():  # i是标签，k是段落列表
            if i == 'label00':
                for ki in k:
                    sentences.append([self.paras[ki], '00'])
            elif i == 'label10':
                for ki in k:
                    sentences.append([self.paras[ki], '10'])
            elif i == 'label20':
                for ki in k:
                    sentences.append([self.paras[ki], '20'])
            elif i == 'label30':
                for ki in k:
                    sentences.append([self.paras[ki], '3A'])
            elif i == 'label40':  # 还需要实现将段落分为句子
                list_tt = []
                for ki in k:
                    list_tt.append(self.paras[ki])
                list_tt = paras2sentences_ltp(list_tt)  # 句子元素列表
                for lt in list_tt:
                    sentences.append([lt, '40]'])
            elif i == 'label50':
                list_tt = []
                for ki in k:
                    list_tt.append(self.paras[ki])
                list_tt = paras2sentences_ltp(list_tt)  # 句子元素列表
                for lt in list_tt:
                    sentences.append([lt, '5B'])
            elif i[5] == '6':  # 第四部分的处理
                list_tt = []
                for ki in k:
                    list_tt.append(self.paras[ki])
                list_tt = paras2sentences_ltp(list_tt)  # 句子元素列表
                for lt in list_tt:
                    if '经鉴定' in lt:
                        sentences.append([lt, '6C'])  # 标注细化，司法鉴定（2021年7月9日）
                    else:
                        sentences.append([lt, '60'])
            elif i == 'label70':
                list_tt = []
                t_list = []
                index_gaozhiyiwu0 = 0
                for ki in k:
                    list_tt.append(self.paras[ki])
                list_tt = paras2sentences_ltp(list_tt)  # 句子元素列表
                for lt in list_tt:
                    if '本院认为' in lt:
                        sentences.append([lt, '7D'])  # 标注细化，案由
                    elif '《中华人民共和国刑法》' in lt:
                        sentences.append([lt, '7F'])  # 标注细化，法律依据

                    elif ('(' == lt[0]) or ('（' == lt[0]):
                        sentences.append([lt, '7T'])  # 标注细化，刑期计算等开始
                        if not (')' == lt[-1]) or ('）' == lt[-1]):
                            t_list.append(sentences.index([lt, '7T']))
                    elif (')' == lt[-1]) or ('）' == lt[-1]):
                        sentences.append([lt, '7T'])  # 标注细化，刑期计算等结束
                        t_list.append(sentences.index([lt, '7T']))
                    elif ('不服本判决' in lt) and ('提出上诉' in lt):  # 告知义务过滤
                        sentences.append([lt, '7T'])
                        index_gaozhiyiwu0 = sentences.index([lt, '7T'])
                    else:
                        sentences.append([lt, '7G'])
                # 刑期计算等修改标签
                tl_flag = 0
                index0 = 0
                for tl in t_list:
                    if tl_flag == 0:
                        index0 = tl
                        tl_flag = 1
                    elif tl_flag == 1:
                        index1 = tl
                        if index1 - index0 > 1:
                            index0 += 1
                            while index0 < index1:
                                sentences[index0] = [sentences[index0][0], '7T']
                                index0 += 1
                        tl_flag = 0

                # 告知义务标签处理
                if index_gaozhiyiwu0 + 1 <= len(sentences) - 1:
                    if sentences[index_gaozhiyiwu0 + 1][1][0] == '7':
                        sentences[index_gaozhiyiwu0 + 1] = [sentences[index_gaozhiyiwu0+1][0], '7T']

            elif i == 'label80':
                list_tt = []
                for ki in k:
                    list_tt.append(self.paras[ki])
                list_tt = paras2sentences_ltp(list_tt)  # 句子元素列表
                for lt in list_tt:
                    sentences.append([lt, '80'])
            elif i == 'label90':
                list_tt = []
                for ki in k:
                    list_tt.append(self.paras[ki])
                list_tt = paras2sentences_ltp(list_tt)  # 句子元素列表
                for lt in list_tt:
                    sentences.append([lt, '90'])
        return sentences

    def sentence_tag_s(self, s):
        """抽取特定一个标签的段落进行存储，且只存储第一句"""
        sentences = []
        for i, k in self.dict_label.items():  # i是标签，k是字符串
            if s == 0:
                if i == 'label00':
                    for ki in k:
                        sentences.append([self.paras[ki], '0'])
            elif s == 1:
                if i == 'label10':
                    for ki in k:
                        sentences.append([self.paras[ki], '1'])
            elif s == 2:
                if i == 'label20':
                    for ki in k:
                        sentences.append([self.paras[ki], '2'])
            elif s == 3:
                if i == 'label30':
                    for ki in k:
                        sentences.append([self.paras[ki], '3'])
            elif s == 4:
                if i == 'label40':
                    list_tt = []
                    for ki in k:
                        list_tt.append(self.paras[ki])
                    list_tt = paras2sentences_ltp(list_tt)  # 句子元素列表
                    for lt in list_tt:
                        sentences.append([lt, '4'])
            elif s == 5:
                if i == 'label50':
                    list_tt = []
                    for ki in k:
                        list_tt.append(self.paras[ki])
                    list_tt = paras2sentences_ltp(list_tt)  # 句子元素列表
                    for_flag = True  # 只存储第一句
                    for lt in list_tt:
                        while for_flag:
                            sentences.append([lt, '5'])
                            for_flag = False
            elif s == 6:
                if i == 'label60':
                    list_tt = []
                    for ki in k:
                        list_tt.append(self.paras[ki])
                    list_tt = paras2sentences_ltp(list_tt)  # 句子元素列表
                    for_flag = True  # 只存储第一句
                    for lt in list_tt:
                        while for_flag:
                            sentences.append([lt, '6'])
                            for_flag = False
            elif s == 7:
                if i == 'label70':
                    list_tt = []
                    for ki in k:
                        list_tt.append(self.paras[ki])
                    list_tt = paras2sentences_ltp(list_tt)  # 句子元素列表
                    for_flag = True  # 只存储第一句
                    for lt in list_tt:
                        while for_flag:
                            sentences.append([lt, '7'])
                            for_flag = False
            elif s == 8:
                if i == 'label80':
                    list_tt = []
                    for ki in k:
                        list_tt.append(self.paras[ki])
                    list_tt = paras2sentences_ltp(list_tt)  # 句子元素列表
                    for_flag = True  # 只存储第一句
                    for lt in list_tt:
                        while for_flag:
                            sentences.append([lt, '8'])
                            for_flag = False
            elif s == 9:
                if i == 'label90':
                    list_tt = []
                    for ki in k:
                        list_tt.append(self.paras[ki])
                    list_tt = paras2sentences_ltp(list_tt)  # 句子元素列表
                    for_flag = True  # 只存储第一句
                    for lt in list_tt:
                        while for_flag:
                            sentences.append([lt, '9'])
                            for_flag = False
            else:
                print('请输入正确格式的标签，例如“0”。')
        sentence = sentences[0]
        return sentence


if __name__ == '__main__':
    # 单文档标注测试
    path1 = r'E:\NLP\02Database\Document\非法采伐、毁坏国家重点保护植物罪(新)\docx\2019湘1126刑初83号被告人欧运德滥伐林木一案刑事判决书.docx'
    paper = Paper(path1)
    dic = paper.dict_label
    for i, k in dic.items():
        print(i, '\t', k)
    for i, k in dic.items():
        if i[-2] != '6':
            continue
        print(f"\n{i}:")
        for ki in k:
            print(paper.paras[ki])
    for s in paper.sentences:
        print(s)

    # for s in paper.sentences:
    #     if s[1][0] == '6':
    #         print(s)
