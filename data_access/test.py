import re
from pyltp import SentenceSplitter

text = 'You say goodbye and I say hello.'

tt = re.split('（\W+）?',text)
print(tt)

sents = SentenceSplitter.split('元芳你怎么看？我就趴窗口上看呗！')  # 分句
print('\n'.join(sents))