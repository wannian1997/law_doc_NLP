# UI运行脚本文件
"""更新日期：2021年7月8日"""
import sys
import os
import time
# PyQt5中使用的基本控件都在PyQt5.QtWidgets模块中
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.QtGui import QColor
# 导入
from data_access.Paper import Paper
from Demo import load_model, sentence2tag
from MFC import *


class MyMainForm(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        time_start = time.time()
        super(MyMainForm, self).__init__(parent)
        self.setupUi(self)

        # 成员变量
        self.index = 0  # 显示的第一条信息的索引
        self.sentences_len = 0
        self.config, self.model = load_model()  # 加载Bert模型

        # 信息栏可视化
        time_end = time.time()

        self.textBrowser_21.setText(f'程序加载成功！\nBert模型加载成功\n\ncost:{time_end - time_start}')

        # 添加登录按钮信号和槽。注意display函数不加小括号()
        self.pushButton.clicked.connect(self.openfile)  # 读取文件
        self.pushButton_1.clicked.connect(self.distest)  # 清空按钮
        self.pushButton_page_before.clicked.connect(self.page_before)
        self.pushButton_page_next.clicked.connect(self.page_next)
        self.pushButton_2.clicked.connect(self.tag0)  # 标签按钮
        self.pushButton_3.clicked.connect(self.tag1)
        self.pushButton_4.clicked.connect(self.tag2)
        self.pushButton_5.clicked.connect(self.tag3)
        self.pushButton_6.clicked.connect(self.tag4)
        self.pushButton_7.clicked.connect(self.tag5)
        self.pushButton_8.clicked.connect(self.tag6)
        self.pushButton_9.clicked.connect(self.tag7)
        self.pushButton_10.clicked.connect(self.save_sentences)
        self.pushButton_amend.clicked.connect(self.tag_amend)

        # 设置键盘事件
        self.pushButton_page_before.setShortcut('Up')  # 绑定快捷键
        self.pushButton_page_next.setShortcut('Down')  # 绑定快捷键
        self.pushButton_2.setShortcut('1')  # 标签按钮
        self.pushButton_3.setShortcut('2')
        self.pushButton_4.setShortcut('3')
        self.pushButton_5.setShortcut('4')
        self.pushButton_6.setShortcut('5')
        self.pushButton_7.setShortcut('6')
        self.pushButton_8.setShortcut('7')
        self.pushButton_9.setShortcut('8')

    def openfile(self):
        time_start = time.time()
        openfile_name, t = QFileDialog.getOpenFileName(self, '选择文件', '', '')  # 打开文件对话框
        if os.path.exists(openfile_name):
            self.paper = Paper(openfile_name)
            time_end = time.time()
            self.textBrowser_21.setText(f'100吴传宏非法捕捞水产品一审刑事判决书.doc\n文件处理成功!\ncost:{time_end - time_start}')
            # 后台处理数据
            self.sentences_len = len(self.paper.sentences)  # 获取句子列表的长度
            self.index = 0  # 初始化索引
            self.info_display10(0)
        else:
            self.textBrowser_21.setText('已取消')

    # 清空按钮
    def distest(self):
        self.textBrowser_21.setText('')
        print(self.checkBox_1.isChecked())

    def info_display10(self, index):  # index为第一条数据的索引
        """显示从index开始的10条内容"""
        # 处理文本数据
        sentences_disply10 = []  # 句子列表
        sentences_tag_display10 = []  # 标签列表
        # 索引判断
        display_len = self.sentences_len - index  # 还要要显示的消息条数
        if display_len > 10:
            display_len = 10
        n = 0
        while n < display_len:  # 只判断display_len个句子
            print(self.paper.sentences[index + n])
            print(self.paper.sentences[index + n][1])
            print(self.paper.sentences[index + n][1][1])
            tag_t = self.paper.sentences[index + n][1][1]  # 取标签信息
            sentences_disply10.append(self.paper.sentences[index+n][0])  # 取橘子
            # 句子标签转换显示
            if tag_t == '0':
                sentences_tag_display10.append('')
            elif tag_t == '1':
                sentences_tag_display10.append('')
            elif tag_t == '2':
                sentences_tag_display10.append('')
            elif tag_t == '3':
                sentences_tag_display10.append('')
            elif tag_t == '4':
                sentences_tag_display10.append('')
            elif tag_t == '5':
                sentences_tag_display10.append('')
            elif tag_t == '6':
                sentences_tag_display10.append('')
            elif tag_t == '7':
                sentences_tag_display10.append('')
            elif tag_t == '8':
                sentences_tag_display10.append('')
            elif tag_t == '9':
                sentences_tag_display10.append('')
            elif tag_t == 'T':  # 清除标记
                sentences_tag_display10.append('')
            elif tag_t == 'A':  # 清除标记
                sentences_tag_display10.append('案号')
            elif tag_t == 'B':  # 清除标记
                sentences_tag_display10.append('被告人信息')
            elif tag_t == 'C':  # 清除标记
                sentences_tag_display10.append('司法鉴定')
            elif tag_t == 'D':  # 清除标记
                sentences_tag_display10.append('案由')
            elif tag_t == 'E':  # 清除标记
                sentences_tag_display10.append('影响判决的因素')
            elif tag_t == 'F':  # 清除标记
                sentences_tag_display10.append('法律依据')
            elif tag_t == 'G':  # 清除标记
                sentences_tag_display10.append('判决结果')
            elif tag_t == 'a':  # 清除标记
                sentences_tag_display10.append('案号t')
            elif tag_t == 'b':  # 清除标记
                sentences_tag_display10.append('被告人信息t')
            elif tag_t == 'c':  # 清除标记
                sentences_tag_display10.append('司法鉴定t')
            elif tag_t == 'd':  # 清除标记
                sentences_tag_display10.append('案由t')
            elif tag_t == 'e':  # 清除标记
                sentences_tag_display10.append('影响判决的因素t')
            elif tag_t == 'f':  # 清除标记
                sentences_tag_display10.append('法律依据t')
            elif tag_t == 'g':  # 清除标记
                sentences_tag_display10.append('判决结果t')
            else:
                sentences_tag_display10.append('未分类标签！')
            n += 1

        # 十条信息显示
        if display_len >= 1:
            self.textBrowser_1.setText(sentences_disply10[0])  # 文本信息
            # 需要设置颜色的情况
            print(sentences_tag_display10[0])
            if (len(sentences_tag_display10[0])>0) and (sentences_tag_display10[0][-1] == 't'):
                flag_color = sentences_tag_display10[0].replace('t', '')
                qc = QColor(0, 0, 255)  # 设置为蓝色
                self.textBrowser_11.setTextColor(qc)
                self.textBrowser_11.setText(flag_color)  # 标签
                qc = QColor(0, 0, 0)  # 设置为黑色
                self.textBrowser_11.setTextColor(qc)
            else:
                self.textBrowser_11.setText(sentences_tag_display10[0])  # 标签

            self.n1.setText(str(index))  # 序号
        else:
            self.textBrowser_1.setText('')  # 文本信息
            self.textBrowser_11.setText('')  # 标签
            self.n1.setText('')  # 序号

        if display_len >= 2:
            self.textBrowser_2.setText(sentences_disply10[1])  # 文本信息
            if (len(sentences_tag_display10[1])>0) and (sentences_tag_display10[1][-1] == 't'):
                flag_color = sentences_tag_display10[1].replace('t', '')
                qc = QColor(0, 0, 255)  # 设置为蓝色
                self.textBrowser_12.setTextColor(qc)
                self.textBrowser_12.setText(flag_color)  # 标签
                qc = QColor(0, 0, 0)  # 设置为黑色
                self.textBrowser_12.setTextColor(qc)
            else:
                self.textBrowser_12.setText(sentences_tag_display10[1])  # 标签
            self.n2.setText(str(index+1))  # 序号
        else:
            self.textBrowser_2.setText('')  # 文本信息
            self.textBrowser_12.setText('')  # 标签
            self.n2.setText('')  # 序号
        if display_len >= 3:
            self.textBrowser_3.setText(sentences_disply10[2])  # 文本信息
            if (len(sentences_tag_display10[2]) > 0) and (sentences_tag_display10[2][-1] == 't'):
                flag_color = sentences_tag_display10[2].replace('t', '')
                qc = QColor(0, 0, 255)  # 设置为蓝色
                self.textBrowser_13.setTextColor(qc)
                self.textBrowser_13.setText(flag_color)  # 标签
                qc = QColor(0, 0, 0)  # 设置为黑色
                self.textBrowser_13.setTextColor(qc)
            else:
                self.textBrowser_13.setText(sentences_tag_display10[2])  # 标签
            self.n3.setText(str(index+2))  # 序号
        else:
            self.textBrowser_3.setText('')  # 文本信息
            self.textBrowser_13.setText('')  # 标签
            self.n3.setText('')  # 序号

        if display_len >=4:
            self.textBrowser_4.setText(sentences_disply10[3])  # 文本信息
            if (len(sentences_tag_display10[3]) > 0) and (sentences_tag_display10[3][-1] == 't'):
                flag_color = sentences_tag_display10[3].replace('t', '')
                qc = QColor(0, 0, 255)  # 设置为蓝色
                self.textBrowser_14.setTextColor(qc)
                self.textBrowser_14.setText(flag_color)  # 标签
                qc = QColor(0, 0, 0)  # 设置为黑色
                self.textBrowser_14.setTextColor(qc)
            else:
                self.textBrowser_14.setText(sentences_tag_display10[3])  # 标签
            self.n4.setText(str(index+3))  # 序号
        else:
            self.textBrowser_4.setText('')  # 文本信息
            self.textBrowser_14.setText('')  # 标签
            self.n4.setText('')  # 序号

        if display_len >=5:
            self.textBrowser_5.setText(sentences_disply10[4])  # 文本信息
            if (len(sentences_tag_display10[4]) > 0) and (sentences_tag_display10[4][-1] == 't'):
                flag_color = sentences_tag_display10[4].replace('t', '')
                qc = QColor(0, 0, 255)  # 设置为蓝色
                self.textBrowser_15.setTextColor(qc)
                self.textBrowser_15.setText(flag_color)  # 标签
                qc = QColor(0, 0, 0)  # 设置为黑色
                self.textBrowser_15.setTextColor(qc)
            else:
                self.textBrowser_15.setText(sentences_tag_display10[4])  # 标签
            self.n5.setText(str(index+4))  # 序号
        else:
            self.textBrowser_5.setText('')  # 文本信息
            self.textBrowser_15.setText('')  # 标签
            self.n5.setText('')  # 序号

        if display_len >=6:
            self.textBrowser_6.setText(sentences_disply10[5])  # 文本信息
            if (len(sentences_tag_display10[5]) > 0) and (sentences_tag_display10[5][-1] == 't'):
                flag_color = sentences_tag_display10[5].replace('t', '')
                qc = QColor(0, 0, 255)  # 设置为蓝色
                self.textBrowser_16.setTextColor(qc)
                self.textBrowser_16.setText(flag_color)  # 标签
                qc = QColor(0, 0, 0)  # 设置为黑色
                self.textBrowser_16.setTextColor(qc)
            else:
                self.textBrowser_16.setText(sentences_tag_display10[5])  # 标签
            self.n6.setText(str(index+5))  # 序号
        else:
            self.textBrowser_6.setText('')  # 文本信息
            self.textBrowser_16.setText('')  # 标签
            self.n6.setText('')  # 序号

        if display_len >= 7:
            self.textBrowser_7.setText(sentences_disply10[6])  # 文本信息
            if (len(sentences_tag_display10[6]) > 0) and (sentences_tag_display10[6][-1] == 't'):
                flag_color = sentences_tag_display10[6].replace('t', '')
                qc = QColor(0, 0, 255)  # 设置为蓝色
                self.textBrowser_17.setTextColor(qc)
                self.textBrowser_17.setText(flag_color)  # 标签
                qc = QColor(0, 0, 0)  # 设置为黑色
                self.textBrowser_17.setTextColor(qc)
            else:
                self.textBrowser_17.setText(sentences_tag_display10[6])  # 标签
            self.n7.setText(str(index+6))  # 序号
        else:
            self.textBrowser_7.setText('')  # 文本信息
            self.textBrowser_17.setText('')  # 标签
            self.n7.setText('')  # 序号

        if display_len >=8:
            self.textBrowser_8.setText(sentences_disply10[7])  # 文本信息
            if (len(sentences_tag_display10[7]) > 0) and (sentences_tag_display10[7][-1] == 't'):
                flag_color = sentences_tag_display10[7].replace('t', '')
                qc = QColor(0, 0, 255)  # 设置为蓝色
                self.textBrowser_18.setTextColor(qc)
                self.textBrowser_18.setText(flag_color)  # 标签
                qc = QColor(0, 0, 0)  # 设置为黑色
                self.textBrowser_18.setTextColor(qc)
            else:
                self.textBrowser_18.setText(sentences_tag_display10[7])  # 标签
            self.n8.setText(str(index+7))  # 序号
        else:
            self.textBrowser_8.setText('')  # 文本信息
            self.textBrowser_18.setText('')  # 标签
            self.n8.setText('')  # 序号

        if display_len >= 9:
            self.textBrowser_9.setText(sentences_disply10[8])  # 文本信息
            if (len(sentences_tag_display10[8]) > 0) and (sentences_tag_display10[8][-1] == 't'):
                flag_color = sentences_tag_display10[8].replace('t', '')
                qc = QColor(0, 0, 255)  # 设置为蓝色
                self.textBrowser_19.setTextColor(qc)
                self.textBrowser_19.setText(flag_color)  # 标签
                qc = QColor(0, 0, 0)  # 设置为黑色
                self.textBrowser_19.setTextColor(qc)
            else:
                self.textBrowser_19.setText(sentences_tag_display10[8])  # 标签
            self.n8.setText(str(index + 7))  # 序号
            self.n9.setText(str(index+8))  # 序号
        else:
            self.textBrowser_9.setText('')  # 文本信息
            self.textBrowser_19.setText('')  # 标签
            self.n9.setText('')  # 序号

        if display_len >= 10:
            self.textBrowser_10.setText(sentences_disply10[9])  # 文本信息
            if (len(sentences_tag_display10[9]) > 0) and (sentences_tag_display10[9][-1] == 't'):
                flag_color = sentences_tag_display10[9].replace('t', '')
                qc = QColor(0, 0, 255)  # 设置为蓝色
                self.textBrowser_20.setTextColor(qc)
                self.textBrowser_20.setText(flag_color)  # 标签
                qc = QColor(0, 0, 0)  # 设置为黑色
                self.textBrowser_20.setTextColor(qc)
            else:
                self.textBrowser_20.setText(sentences_tag_display10[9])  # 标签
            self.n8.setText(str(index + 7))  # 序号
            self.n10.setText(str(index+9))  # 序号
        else:
            self.textBrowser_10.setText('')  # 文本信息
            self.textBrowser_20.setText('')  # 标签
            self.n10.setText('')  # 序号
        # 刷新复选按钮状态
        self.checkBox_1.setChecked(False)  # 修改后就取消选中
        self.checkBox_2.setChecked(False)
        self.checkBox_3.setChecked(False)
        self.checkBox_4.setChecked(False)
        self.checkBox_5.setChecked(False)
        self.checkBox_6.setChecked(False)
        self.checkBox_7.setChecked(False)
        self.checkBox_8.setChecked(False)
        self.checkBox_9.setChecked(False)
        self.checkBox_10.setChecked(False)

    def page_before(self):
        self.index -= 10
        if self.index < 0:
            self.textBrowser_21.setText('已经到文章最前面了！\n往后看看吧。')
            self.index += 10
        else:
            self.info_display10(self.index)
        print(self.index)

    def page_next(self):
        self.index += 10
        if self.index > len(self.paper.sentences):
            self.textBrowser_21.setText('这是最后一页内容！\n别忘了保存！')
            self.index -= 10
        else:
            self.info_display10(self.index)
        print(self.index)

    def tag_t(self, tag_text, tag_number):
        """修改标签  tag_text输入标签内容文本,tag_number输入标签数字"""
        # 第一条信息
        if self.checkBox_1.isChecked():  # 必须选中才修改
            self.textBrowser_11.setText(tag_text)  # 界面更新
            self.paper.sentences[self.index][1] = self.paper.sentences[self.index][1][0] + f'{tag_number}'
        # 第二条信息
        if self.checkBox_2.isChecked():  # 必须选中才修改
            self.textBrowser_12.setText(tag_text)  # 界面更新
            self.paper.sentences[self.index+1][1] = self.paper.sentences[self.index+1][1][0] + f'{tag_number}'
        # 第三条信息
        if self.checkBox_3.isChecked():  # 必须选中才修改
            self.textBrowser_13.setText(tag_text)  # 界面更新
            self.paper.sentences[self.index+2][1] = self.paper.sentences[self.index+2][1][0] + f'{tag_number}'
        # 第四条信息
        if self.checkBox_4.isChecked():  # 必须选中才修改
            self.textBrowser_14.setText(tag_text)  # 界面更新
            self.paper.sentences[self.index+3][1] = self.paper.sentences[self.index+3][1][0] + f'{tag_number}'
        # 第五条信息
        if self.checkBox_5.isChecked():  # 必须选中才修改
            self.textBrowser_15.setText(tag_text)  # 界面更新
            self.paper.sentences[self.index + 4][1] = self.paper.sentences[self.index + 4][1][0] + f'{tag_number}'

        if self.checkBox_6.isChecked():  # 必须选中才修改
            self.textBrowser_16.setText(tag_text)  # 界面更新
            self.paper.sentences[self.index+5][1] = self.paper.sentences[self.index+5][1][0] + f'{tag_number}'

        if self.checkBox_7.isChecked():  # 必须选中才修改
            self.textBrowser_17.setText(tag_text)  # 界面更新
            self.paper.sentences[self.index+6][1] = self.paper.sentences[self.index+6][1][0] + f'{tag_number}'

        if self.checkBox_8.isChecked():  # 必须选中才修改
            self.textBrowser_18.setText(tag_text)  # 界面更新
            self.paper.sentences[self.index+7][1] = self.paper.sentences[self.index+7][1][0] + f'{tag_number}'

        if self.checkBox_9.isChecked():  # 必须选中才修改
            self.textBrowser_19.setText(tag_text)  # 界面更新
            self.paper.sentences[self.index+8][1] = self.paper.sentences[self.index+8][1][0] + f'{tag_number}'

        if self.checkBox_10.isChecked():  # 必须选中才修改
            self.textBrowser_20.setText(tag_text)  # 界面更新
            self.paper.sentences[self.index+9][1] = self.paper.sentences[self.index+9][1][0] + f'{tag_number}'

        # 刷新复选按钮状态
        self.checkBox_1.setChecked(False)
        self.checkBox_2.setChecked(False)
        self.checkBox_3.setChecked(False)
        self.checkBox_4.setChecked(False)
        self.checkBox_5.setChecked(False)
        self.checkBox_6.setChecked(False)
        self.checkBox_7.setChecked(False)
        self.checkBox_8.setChecked(False)
        self.checkBox_9.setChecked(False)
        self.checkBox_10.setChecked(False)

        # # 后台监视（最后一页会出现问题）
        # n = 0
        # while n < 10:
        #     print(self.paper.sentences[self.index + n].replace('\n', ''))
        #     n += 1

    def tag0(self):
        """案号"""
        self.tag_t('案号', 'A')
        self.textBrowser_21.setText('案号标注成功')

    def tag1(self):
        """被告人信息"""
        self.tag_t('被告人信息', 'B')
        self.textBrowser_21.setText('被告人信息标注成功')

    def tag2(self):
        """司法鉴定"""
        self.tag_t('司法鉴定', 'C')
        self.textBrowser_21.setText('司法鉴定标注成功')

    def tag3(self):
        """案由"""
        self.tag_t('案由', 'D')
        self.textBrowser_21.setText('案由标注成功')

    def tag4(self):
        """影响判决的因素"""
        self.tag_t('影响判决的因素', 'E')
        self.textBrowser_21.setText('影响判决的因素标注成功')

    def tag5(self):
        """法律依据"""
        self.tag_t('法律依据', 'F')
        self.textBrowser_21.setText('法律依据标注成功')

    def tag6(self):
        """判决结果"""
        self.tag_t('判决结果', 'G')
        self.textBrowser_21.setText('判决结果标注成功')

    def tag7(self):
        """清除标注"""
        self.tag_t(' ', 'T')
        self.textBrowser_21.setText('清除标注成功')

    def number2character(self, number):
        """修正标签转换，在tag_amend函数中使用"""
        if number == 0:
            character = 'a'
        elif number == 1:
            character = 'b'
        elif number == 2:
            character = 'c'
        elif number == 3:
            character = 'd'
        elif number == 4:
            character = 'e'
        elif number == 5:
            character = 'f'
        elif number == 6:
            character = 'g'
        else:
            pass
        return character

    def tag_amend(self):
        """Bert标注句子"""
        self.index = 0
        threshold_value = 3.8  # 修正阈值
        sentences_t = []  # 暂存所有段落
        self_sentences = self.paper.sentences.copy()
        for sentence_sq in self_sentences:  # 列表
            sentence = sentence_sq[0]  # 取句子
            outputs_t, predict_t = sentence2tag(self.config, self.model, sentence_sq[0])  # 标签预测
            if sentence_sq[1][1] == 'A':
                # 判断是否有误
                pt_index = predict_t[0]  # 向量值索引
                if pt_index == 0:  # 判断是不是预想的数字标签
                    amend_flag = 0
                else:
                    amend_flag = 1
                if amend_flag:  # 有误，满足修正条件
                    if float(outputs_t[0][pt_index]) >= threshold_value:  # 满足阈值条件
                        c_tag1 = self.number2character(pt_index)
                        sentences_t.append([sentence_sq[0], sentence_sq[1][0] + f'{c_tag1}'])  # 修改标签
                    else:
                        sentences_t.append([sentence_sq[0], sentence_sq[1]])  # 有误，但不满足阈值条件不变
                else:
                    sentences_t.append([sentence_sq[0], sentence_sq[1]])  # 无误，不变

            elif sentence_sq[1][1] == 'B':
                # 判断是否有误
                pt_index = predict_t[0]  # 向量值索引
                if pt_index == 1:  # 判断是不是预想的数字标签
                    amend_flag = 0
                else:
                    amend_flag = 1
                if amend_flag:  # 满足修正条件
                    if float(outputs_t[0][pt_index]) >= threshold_value:  # 满足阈值条件
                        c_tag1 = self.number2character(pt_index)
                        sentences_t.append([sentence_sq[0], sentence_sq[1][0] + f'{c_tag1}'])  # 修改标签
                    else:
                        sentences_t.append([sentence_sq[0], sentence_sq[1]])  # 有误，但不满足阈值条件不变
                else:
                    sentences_t.append([sentence_sq[0], sentence_sq[1]])  # 无误，不变
            elif sentence_sq[1][1] == 'C':
                # 判断是否有误
                pt_index = predict_t[0]  # 向量值索引
                if pt_index == 2:  # 判断是不是预想的数字标签
                    amend_flag = 0
                else:
                    amend_flag = 1
                if amend_flag:  # 满足修正条件
                    if float(outputs_t[0][pt_index]) >= threshold_value:  # 满足阈值条件
                        c_tag1 = self.number2character(pt_index)
                        sentences_t.append([sentence_sq[0], sentence_sq[1][0] + f'{c_tag1}'])  # 修改标签
                    else:
                        sentences_t.append([sentence_sq[0], sentence_sq[1]])  # 有误，但不满足阈值条件不变
                else:
                    sentences_t.append([sentence_sq[0], sentence_sq[1]])  # 无误，不变
            elif sentence_sq[1][1] == 'D':
                # 判断是否有误
                pt_index = predict_t[0]  # 向量值索引
                if pt_index == 3:  # 判断是不是预想的数字标签
                    amend_flag = 0
                else:
                    amend_flag = 1
                if amend_flag:  # 满足修正条件
                    if float(outputs_t[0][pt_index]) >= threshold_value:  # 满足阈值条件
                        c_tag1 = self.number2character(pt_index)
                        sentences_t.append([sentence_sq[0], sentence_sq[1][0] + f'{c_tag1}'])  # 修改标签
                    else:
                        sentences_t.append([sentence_sq[0], sentence_sq[1]])  # 有误，但不满足阈值条件不变
                else:
                    sentences_t.append([sentence_sq[0], sentence_sq[1]])  # 无误，不变
            elif sentence_sq[1][1] == 'E':
                # 判断是否有误
                pt_index = predict_t[0]  # 向量值索引
                if pt_index == 4:  # 判断是不是预想的数字标签
                    amend_flag = 0
                else:
                    amend_flag = 1
                if amend_flag:  # 满足修正条件
                    if float(outputs_t[0][pt_index]) >= threshold_value:  # 满足阈值条件
                        c_tag1 = self.number2character(pt_index)
                        sentences_t.append([sentence_sq[0], sentence_sq[1][0] + f'{c_tag1}'])  # 修改标签
                    else:
                        sentences_t.append([sentence_sq[0], sentence_sq[1]])  # 有误，但不满足阈值条件不变
                else:
                    sentences_t.append([sentence_sq[0], sentence_sq[1]])  # 无误，不变
            elif sentence_sq[1][1] == 'F':
                # 判断是否有误
                pt_index = predict_t[0]  # 向量值索引
                if pt_index == 5:  # 判断是不是预想的数字标签
                    amend_flag = 0
                else:
                    amend_flag = 1
                if amend_flag:  # 满足修正条件
                    if float(outputs_t[0][pt_index]) >= threshold_value:  # 满足阈值条件
                        c_tag1 = self.number2character(pt_index)
                        sentences_t.append([sentence_sq[0], sentence_sq[1][0] + f'{c_tag1}'])  # 修改标签
                    else:
                        sentences_t.append([sentence_sq[0], sentence_sq[1]])  # 有误，但不满足阈值条件不变
                else:
                    sentences_t.append([sentence_sq[0], sentence_sq[1]])  # 无误，不变
            elif sentence_sq[1][1] == 'G':
                # 判断是否有误
                pt_index = predict_t[0]  # 向量值索引
                if pt_index == 6:  # 判断是不是预想的数字标签
                    amend_flag = 0
                else:
                    amend_flag = 1
                if amend_flag:  # 满足修正条件
                    if float(outputs_t[0][pt_index]) >= threshold_value:  # 满足阈值条件
                        c_tag1 = self.number2character(pt_index)
                        sentences_t.append([sentence_sq[0], sentence_sq[1][0] + f'{c_tag1}'])  # 修改标签
                    else:
                        sentences_t.append([sentence_sq[0], sentence_sq[1]])  # 有误，但不满足阈值条件不变
                else:
                    sentences_t.append([sentence_sq[0], sentence_sq[1]])  # 无误，不变
            else:
                sentences_t.append([sentence_sq[0], sentence_sq[1]])  # 无误，不变
        self.paper.sentences = sentences_t.copy()
        self.textBrowser_21.setText("模型修正成功！")

        for s in sentences_t:
            print(s)
        print(self.paper.sentences)
        self.info_display10(0)

    def tag_map(self, tag0):
        """标签映射 三个变量均为字符型"""
        list_not_map = ['T']  # 不映射标签(避免不必要的运算)
        for lm in list_not_map:
            if tag0 == lm:
                return tag0

        dict_map = {'0': 'T', '1': 'T', '2': 'T', '3': '0', '4': 'T', '5': '1', '6': 'T', '7': '6', '8': 'T', '9': '5',
                    'A': '0', 'B': '1', 'C': '2', 'D': '3',  'E': '4',  'F': '5', 'G': '6',
                    'a': '0', 'b': '1', 'c': '2', 'd': '3',  'e': '4',  'f': '5', 'g': '6'}  # 映射字典
        tag1 = dict_map[tag0]  # 映射标签
        return tag1

    def save_sentences(self):
        """标签映射并保存标注文件为txt文件"""
        url = self.paper.sentences[0][0]  # 解析word文件路径
        (filter, filename) = os.path.split(url)  # 文件夹路径和文件名
        (name, ext) = os.path.splitext(filename)   # 文件名（去扩展名）和扩展名

        path = os.path.join(filter, name+'.txt')  # 生成txt文件名
        file = open(path, 'w', encoding="utf-8")
        # 句子保存（标签转换）
        for l in self.paper.sentences:
            lt = self.tag_map(l[1][1])  # 标签映射
            if lt != 'T':
                file.write(l[0]+f"\t{lt}\n")
                print(lt)
        file.close()
        self.textBrowser_21.setText(f"{path}\n文件存储成功")


if __name__ == '__main__':
    # 固定的，PyQt5程序都需要QApplication对象。sys.argv是命令行参数列表，确保程序可以双击运行
    app = QApplication(sys.argv)
    # 初始化
    myWin = MyMainForm()
    # 将窗口控件显示在屏幕上
    myWin.show()
    # 程序运行，sys.exit方法确保程序完整退出。
    sys.exit(app.exec_())
