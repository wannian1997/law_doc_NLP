from Paper import Paper
from process_doc import paras2sentences_ltp, list2txt
import os
from ltp import LTP
from pyltp import SentenceSplitter

print('\n-----------------------打开文件-----------------------')
path_temp = r'D:\projects_pycharm\LawProcess\Demo_Filter\8赵光成非法采矿罪一审刑事判决书.doc'
paper = Paper(path_temp)

# 特定部分分句处理 label06，return sentences
list_paras_temp = []  # 用来存储特定段落,二维
for pl in paper.dict_label['label06']:
    list_paras_temp.append(paper.paras[pl])
sentences = []
for lp in list_paras_temp:
    sents = SentenceSplitter.split(lp)  # 分句
    if len(sents[-1]) < 2:  # 过滤
        sents[-2] = sents[-2] + sents[-1]
        del sents[-1]
    sents_t = []  # 转换VectorOfString类型，返回字符串列表
    for s in sents:
        sents_t.append(s)
    sentences.append(sents_t)
print(sentences)

print('\n-----------------------pyltp模型文书处理调用测试-----------------------')
ltp = LTP()  # 调用pyltp模型


for sentence in sentences:  # 遍历分析
    sentence = sentence[0]  # 只分析每段的第一句
    print(sentence)
    seg, hidden = ltp.seg([sentence])
    srl = ltp.srl(hidden)  # 语义角色标注
    pos = ltp.pos(hidden)  # 词性标注
    print(seg)
    print(srl)
    print(pos)
    a0, a1, a1v = '', '', ''
    for sr in srl[0]:
        if len(sr) > 0:
            for s in sr:
                tag, start, end = s
                if tag == 'A0':  # 解析实体,触发者
                    a0 = "".join(seg[0][start:end + 1])
                    print('a0：', a0)
                    a1v = seg[0][end + 1]
                    print('v：', a1v)
                if tag == 'A1':
                    a1 = "".join(seg[0][start:end + 1])  # 解析受事者
                    a1v = seg[0][start - 1]
                    print('v：', a1v)
                    # print('a1：', a1)
                print(tag, ':', "".join(seg[0][start:end + 1]))

print('\n-----------------------pyltp模型标准调用测试-----------------------')
txt = '徐州市云龙区人民检察院以云检诉刑诉[2017]17号起诉书指控被告人赵光成犯非法采矿罪，于2017年1月22日向本院提起公诉。'
print(txt)

seg, hidden = ltp.seg([txt])
print(seg)
# 词性标注
pos = ltp.pos(hidden)
print('词性标注：\n', pos)
# 命名实体识别
ner = ltp.ner(hidden)
print('命名实体识别：\n', ner[0])
# for ne in ner[0]:
#     tag, start, end = ne
#     print(tag, ":", "".join(seg[0][start:end + 1]))

# 依存句法分析
dep = ltp.dep(hidden)
print('依存句法分析：\n', dep)

# 语义角色标注
srl = ltp.srl(hidden, keep_empty = False)
print('语义角色标注：\n', srl)
