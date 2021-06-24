# coding=utf8
# the above tag defines encoding for this document and is for Python 2.x compatibility
from extract_list import read_docx
import os
from process_doc import paras2sentences
import math
import jieba
print('测试正则表达式区域')
import re

regex = r"相关.?法律文本"
test_str = "测试测试相关的法律文本,相关z法律文本，，相关法律文本"
matches = re.finditer(regex, test_str, re.MULTILINE)
for m1, m2 in enumerate(matches, start=0):
    print(m2.group())
print(matches)
print('.....')
for matchNum, match in enumerate(matches, start=0):
    print("Match {matchNum} was found at {start}-{end}: {match}".format(matchNum=matchNum, start=match.start(),
                                                                        end=match.end(), match=match.group()))
    for groupNum in range(0, len(match.groups())):
        groupNum = groupNum + 1
        print("Group {groupNum} found at {start}-{end}: {group}".format(groupNum=groupNum, start=match.start(groupNum),
                                                                        end=match.end(groupNum),
                                                                        group=match.group(groupNum)))


# 调试区域（待调试错误）
pa1 = '被告单位：信丰众城矿业有限公司（以下简称众城公司），统一社会信用代码：91360722MA35G1YK7R，住所地位于江西省赣州市信丰县嘉定镇水北计委办公楼09#店面，法定代表人：刘丙秀。'
pa2 = '附带民事诉讼原告人黑龙江省桦南重点国有林管理局'

if r'被告' in pa1:
    print('1')
txt1 = r'附带(民事)?(公益)?(诉讼)?'
print(txt1)
if txt1 in pa2:
    print('2')