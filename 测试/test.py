from pyltp import Segmentor, Postagger, \
    NamedEntityRecognizer, SementicRoleLabeller
import jieba
import jieba.posseg as psg
import re

print('-----------------------测试区域-----------------------')
from Doc2 import *
path1 = r'E:\NLP\02Database\Document\非法采伐、毁坏国家重点保护植物罪(新)\docx\2019皖1524刑初117号熊希金非法采伐国家重点保护植物案判决书.docx'
doc = Doc2(path1)

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
LTP_DATA_DIR = r'D:\projects_pycharm\ltp_data_v3.4.0'  # 加载模型
# 分句
sents = SentenceSplitter.split('元芳你怎么看？我就趴窗口上看呗！')
print('\n'.join(sents))

# 分词
cws_model_path=os.path.join(LTP_DATA_DIR, 'cws.model')
segmentor=Segmentor()
segmentor.load(cws_model_path)
words = segmentor.segment('徐州市云龙区人民检察院以云检诉刑诉[2017]17号起诉书指控被告人赵光成犯非法采矿罪，于2017年1月22日向本院提起公诉。')
print('\t'.join(words))
segmentor.release()

# 词性标注
pos_model_path = os.path.join(LTP_DATA_DIR, 'pos.model')  # 词性标注模型路径，模型名称为`pos.model`
postagger = Postagger()  # 初始化实例
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
arcs = parser.parse(words, postags)  # 句法分析
print("\t".join("%d:%s" % (arc.head, arc.relation) for arc in arcs))
parser.release()  # 释放模型

# 语义角色标注
srl_model_path = os.path.join(LTP_DATA_DIR, 'pisrl_win.model')   # 语义角色标注模型目录路径，模型目录为`srl`。注意该模型路径是一个目录，而不是一个文件。
labeller = SementicRoleLabeller()  # 初始化实例
labeller.load(srl_model_path)  # 加载模型
# arcs 使用依存句法分析的结果
roles = labeller.label(words, postags, arcs)  # 语义角色标注
for role in roles:
    print(role.index, "".join(
        ["%s:(%d,%d)" % (arg.name, arg.range.start, arg.range.end) for arg in role.arguments]))
labeller.release()  # 释放

