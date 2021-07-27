from pyltp import Segmentor, SentenceSplitter, Postagger, NamedEntityRecognizer
import jieba
import jieba.posseg as psg
import os
import re


print('-----------------------正则表达式测试-----------------------')
sentence_t = '被告人王某某'
tt = r'被告[人|单]位?'
if not re.search(tt, sentence_t) is None:
    print('true')

print('-----------------------jieba模型调用测试-----------------------')
text = '公诉机关广西壮族自治区西林县人民检察院'
seg_list = jieba.cut(text, cut_all=False)
print(seg_list)
for i in seg_list:
    print(i)
    for pi in psg.cut(i):
        print(pi)

seg = psg.cut(text)
print()
for ele in seg:
    print (ele)

print('-----------------------pyltp模型调用测试-----------------------')
sents = SentenceSplitter.split('元\n芳,你;怎:么看？我就趴窗口上看呗！')  # 分句
print('\n'.join(sents))

# 分词
LTP_DATA_DIR=r'D:\projects_pycharm\ltp_data_v3.4.0'
cws_model_path=os.path.join(LTP_DATA_DIR, 'cws.model')
segmentor=Segmentor()
segmentor.load(cws_model_path)
words=segmentor.segment('公诉机关广西壮族自治区西林县人民检察院')
print(type(words))
print('\t'.join(words))
segmentor.release()

# 词性标注
pos_model_path = os.path.join(LTP_DATA_DIR, 'pos.model')  # 词性标注模型路径，模型名称为`pos.model`
postagger = Postagger() # 初始化实例
postagger.load(pos_model_path)  # 加载模型
postags = postagger.postag(words)  # 词性标注
print('\t'.join(postags))
postagger.release()  # 释放模型

# 命名实体识别
ner_model_path = os.path.join(LTP_DATA_DIR, 'ner.model')  # 命名实体识别模型路径，模型名称为`pos.model`
recognizer = NamedEntityRecognizer()  # 初始化实例
recognizer.load(ner_model_path)  # 加载模型
netags = recognizer.recognize(words, postags)  # 命名实体识别
print('\t'.join(netags))
recognizer.release()  # 释放模型


# 依存语法关系
par_model_path = os.path.join(LTP_DATA_DIR, 'parser.model')  # 依存句法分析模型路径，模型名称为`parser.model`
from pyltp import Parser
parser = Parser()  # 初始化实例
parser.load(par_model_path)  # 加载模型

words = ['元芳', '你', '怎么', '看']
postags = ['nh', 'r', 'r', 'v']
arcs = parser.parse(words, postags)  # 句法分析

print("\t".join("%d:%s" % (arc.head, arc.relation) for arc in arcs))

# 语义角色标注
from ltp import LTP

ltp = LTP()

seg, hidden = ltp.seg(["元芳你怎么看"])
srl = ltp.srl(hidden)
print(srl)