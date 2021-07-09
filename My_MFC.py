# UI运行脚本文件
"""更新日期：2021年7月8日"""
import sys
import os
import time
# PyQt5中使用的基本控件都在PyQt5.QtWidgets模块中
from PyQt5.QtWidgets import QApplication, QMainWindow,QFileDialog,QMessageBox
# 导入
from data_access.TPaper import TPaper
from MFC import *


class MyMainForm(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyMainForm, self).__init__(parent)
        self.setupUi(self)

        # 成员变量
        self.index = 0  # 显示的第一条信息的索引
        self.sentences_len = 0

        # 信息栏可视化
        self.textBrowser_21.setText('程序加载成功！')

        # 添加登录按钮信号和槽。注意display函数不加小括号()
        self.pushButton.clicked.connect(self.openfile)  # 读取文件
        self.pushButton_1.clicked.connect(self.distest)  # 清空信息栏
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

    def openfile(self):
        time_start = time.time()
        openfile_name, t = QFileDialog.getOpenFileName(self, '选择文件', '', 'Word files(*.doc , *.docx, *.txt)')  # 打开文件对话框
        if os.path.exists(openfile_name):
            self.paper = TPaper(openfile_name)
            time_end = time.time()
            self.textBrowser_21.setText(f'100吴传宏非法捕捞水产品一审刑事判决书.doc\n文件处理成功!\ncost:{time_end - time_start}')
            # 后台处理数据
            self.sentences_len = len(self.paper.sentences)  # 获取句子列表的长度
            self.info_disply10(0)
        else:
            self.textBrowser_21.setText('已取消')

    # 测试函数
    def distest(self):
        self.textBrowser_21.setText('')
        print(self.checkBox_1.isChecked())

    def info_disply10(self, index):  # index为第一条数据的索引
        """显示从index开始的10条内容"""
        # 处理文本数据
        sentences_disply10 = []
        sentences_tag_display10 = []
        # 索引判断
        display_len = self.sentences_len - index  # 还要要显示的消息条数
        if display_len > 10:
            display_len = 10
        n = 0
        while n < display_len:  # 只判断display_len个句子
            tag_t = self.paper.sentences[index + n][-2]
            sentences_disply10.append(self.paper.sentences[index+n].replace(f'\t{tag_t}\n', ''))  # 删除后缀
            # 句子标签转换显示
            if tag_t == '0':
                sentences_tag_display10.append('')
            elif tag_t == '1':
                sentences_tag_display10.append('')
            elif tag_t == '2':
                sentences_tag_display10.append('')
            elif tag_t == '3':
                sentences_tag_display10.append('案号')
            elif tag_t == '4':
                sentences_tag_display10.append('')
            elif tag_t == '5':
                sentences_tag_display10.append('被告人信息')
            elif tag_t == '6':
                sentences_tag_display10.append('')
            elif tag_t == '7':
                sentences_tag_display10.append('')
            elif tag_t == '8':
                sentences_tag_display10.append('')
            elif tag_t == '9':
                sentences_tag_display10.append('法律依据')
            elif tag_t == 'T':  # 清除标记
                sentences_tag_display10.append('')
            else:
                sentences_tag_display10.append(' ')
            n += 1

        # 十条信息显示
        if display_len >= 1:
            self.textBrowser_1.setText(sentences_disply10[0])  # 文本信息
            self.textBrowser_11.setText(sentences_tag_display10[0])  # 标签
            self.n1.setText(str(index))  # 序号
        else:
            self.textBrowser_1.setText('')  # 文本信息
            self.textBrowser_11.setText('')  # 标签
            self.n1.setText('')  # 序号

        if display_len >= 2:
            self.textBrowser_2.setText(sentences_disply10[1])  # 文本信息
            self.textBrowser_12.setText(sentences_tag_display10[1])  # 标签
            self.n2.setText(str(index+1))  # 序号
        else:
            self.textBrowser_2.setText('')  # 文本信息
            self.textBrowser_12.setText('')  # 标签
            self.n2.setText('')  # 序号
        if display_len >= 3:
            self.textBrowser_3.setText(sentences_disply10[2])  # 文本信息
            self.textBrowser_13.setText(sentences_tag_display10[2])  # 标签
            self.n3.setText(str(index+2))  # 序号
        else:
            self.textBrowser_3.setText('')  # 文本信息
            self.textBrowser_13.setText('')  # 标签
            self.n3.setText('')  # 序号

        if display_len >=4:
            self.textBrowser_4.setText(sentences_disply10[3])  # 文本信息
            self.textBrowser_14.setText(sentences_tag_display10[3])  # 标签
            self.n4.setText(str(index+3))  # 序号
        else:
            self.textBrowser_4.setText('')  # 文本信息
            self.textBrowser_14.setText('')  # 标签
            self.n4.setText('')  # 序号

        if display_len >=5:
            self.textBrowser_5.setText(sentences_disply10[4])  # 文本信息
            self.textBrowser_15.setText(sentences_tag_display10[4])  # 标签
            self.n5.setText(str(index+4))  # 序号
        else:
            self.textBrowser_5.setText('')  # 文本信息
            self.textBrowser_15.setText('')  # 标签
            self.n5.setText('')  # 序号

        if display_len >=6:
            self.textBrowser_6.setText(sentences_disply10[5])  # 文本信息
            self.textBrowser_16.setText(sentences_tag_display10[5])  # 标签
            self.n6.setText(str(index+5))  # 序号
        else:
            self.textBrowser_6.setText('')  # 文本信息
            self.textBrowser_16.setText('')  # 标签
            self.n6.setText('')  # 序号

        if display_len >= 7:
            self.textBrowser_7.setText(sentences_disply10[6])  # 文本信息
            self.textBrowser_17.setText(sentences_tag_display10[6])  # 标签
            self.n7.setText(str(index+6))  # 序号
        else:
            self.textBrowser_7.setText('')  # 文本信息
            self.textBrowser_17.setText('')  # 标签
            self.n7.setText('')  # 序号

        if display_len >=8:
            self.textBrowser_8.setText(sentences_disply10[7])  # 文本信息
            self.textBrowser_18.setText(sentences_tag_display10[7])  # 标签
            self.n8.setText(str(index+7))  # 序号
        else:
            self.textBrowser_8.setText('')  # 文本信息
            self.textBrowser_18.setText('')  # 标签
            self.n8.setText('')  # 序号

        if display_len >=9:
            self.textBrowser_9.setText(sentences_disply10[8])  # 文本信息
            self.textBrowser_19.setText(sentences_tag_display10[8])  # 标签
            self.n9.setText(str(index+8))  # 序号
        else:
            self.textBrowser_9.setText('')  # 文本信息
            self.textBrowser_19.setText('')  # 标签
            self.n9.setText('')  # 序号

        if display_len >= 10:
            self.textBrowser_10.setText(sentences_disply10[9])  # 文本信息
            self.textBrowser_20.setText(sentences_tag_display10[9])  # 标签
            self.n10.setText(str(index+9))  # 序号
        else:
            self.textBrowser_10.setText('')  # 文本信息
            self.textBrowser_20.setText('')  # 标签
            self.n10.setText('')  # 序号

    def page_before(self):
        self.index -= 10
        if self.index < 0:
            self.textBrowser_21.setText('已经到文章最前面了！\n往后看看吧。')
            self.index += 10
        else:
            self.info_disply10(self.index)
        print(self.index)

    def page_next(self):
        self.index += 10
        if self.index > len(self.paper.sentences):
            self.textBrowser_21.setText('这是最后一页内容！\n别忘了保存！')
            self.index -= 10
        else:
            self.info_disply10(self.index)
        print(self.index)

    def tag_t(self, tag_text, tag_number):
        """修改标签  tag_text输入标签内容文本,tag_number输入标签数字"""
        # 第一条信息
        if self.checkBox_1.isChecked():  # 必须选中才修改
            self.textBrowser_11.setText(tag_text)  # 界面更新
            self.paper.sentences[self.index] = self.paper.sentences[self.index].replace(
                f'\t{self.paper.sentences[self.index][-2]}\n', f'\t{tag_number}\n')
        # 第二条信息
        if self.checkBox_2.isChecked():  # 必须选中才修改
            self.textBrowser_12.setText(tag_text)  # 界面更新
            self.paper.sentences[self.index + 1] = self.paper.sentences[self.index + 1].replace(
                f'\t{self.paper.sentences[self.index + 1][-2]}\n', f'\t{tag_number}\n')
        # 第三条信息
        if self.checkBox_3.isChecked():  # 必须选中才修改
            self.textBrowser_13.setText(tag_text)  # 界面更新
            self.paper.sentences[self.index + 2] = self.paper.sentences[self.index + 2].replace(
                f'\t{self.paper.sentences[self.index + 2][-2]}\n', f'\t{tag_number}\n')
        # 第四条信息
        if self.checkBox_4.isChecked():  # 必须选中才修改
            self.textBrowser_14.setText(tag_text)  # 界面更新
            self.paper.sentences[self.index + 3] = self.paper.sentences[self.index + 3].replace(
                f'\t{self.paper.sentences[self.index + 3][-2]}\n', f'\t{tag_number}\n')
        # 第五条信息
        if self.checkBox_5.isChecked():  # 必须选中才修改
            self.textBrowser_15.setText(tag_text)  # 界面更新
            self.paper.sentences[self.index + 4] = self.paper.sentences[self.index + 4].replace(
                f'\t{self.paper.sentences[self.index + 4][-2]}\n', f'\t{tag_number}\n')

        if self.checkBox_6.isChecked():  # 必须选中才修改
            self.textBrowser_16.setText(tag_text)  # 界面更新
            self.paper.sentences[self.index + 5] = self.paper.sentences[self.index + 5].replace(
                f'\t{self.paper.sentences[self.index + 5][-2]}\n', f'\t{tag_number}\n')

        if self.checkBox_7.isChecked():  # 必须选中才修改
            self.textBrowser_17.setText(tag_text)  # 界面更新
            self.paper.sentences[self.index + 6] = self.paper.sentences[self.index + 6].replace(
                f'\t{self.paper.sentences[self.index + 6][-2]}\n', f'\t{tag_number}\n')

        if self.checkBox_8.isChecked():  # 必须选中才修改
            self.textBrowser_18.setText(tag_text)  # 界面更新
            self.paper.sentences[self.index + 7] = self.paper.sentences[self.index + 7].replace(
                f'\t{self.paper.sentences[self.index + 7][-2]}\n', f'\t{tag_number}\n')

        if self.checkBox_9.isChecked():  # 必须选中才修改
            self.textBrowser_19.setText(tag_text)  # 界面更新
            self.paper.sentences[self.index + 8] = self.paper.sentences[self.index + 8].replace(
                f'\t{self.paper.sentences[self.index + 8][-2]}\n', f'\t{tag_number}\n')

        if self.checkBox_10.isChecked():  # 必须选中才修改
            self.textBrowser_20.setText(tag_text)  # 界面更新
            self.paper.sentences[self.index + 9] = self.paper.sentences[self.index + 9].replace(
                f'\t{self.paper.sentences[self.index + 9][-2]}\n', f'\t{tag_number}\n')

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
        # 后台监视
        n = 0
        while n < 10:
            print(self.paper.sentences[self.index + n].replace('\n', ''))
            n += 1

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

    def tag_map(self, sentence):
        """标签映射 三个变量均为字符型"""
        sentence_t = ''  # 初始化
        list_not_map = ['T']  # 不映射标签(避免不必要的运算)
        for lm in list_not_map:
            if sentence[-2] == lm:
                return sentence

        dict_map = {'0': 'T', '1': 'T', '2': 'T', '4': 'T', '6': 'T', '7': 'T', '8': 'T',
            '3': '0', '5': '1', '9': '5',
                    'A': '0', 'B': '1', 'C': '2', 'D': '3',  'E': '4',  'F': '5', 'G': '6'}  # 映射字典
        tag0 = sentence[-2]  # 原始标签
        tag1 = dict_map[tag0]  # 映射标签
        if sentence[-2] == tag0:
            sentence_t = sentence.replace(f'\t{tag0}\n', f'\t{tag1}\n')
        return sentence_t

    def save_sentences(self):
        """保存标注文件为txt文件"""
        url = self.paper.sentences[0].replace('\t0\n', '')  # 解析word文件路径
        (filter, filename) = os.path.split(url)  # 文件夹路径和文件名
        (name, ext) = os.path.splitext(filename)   # 文件名（去扩展名）和扩展名

        path = os.path.join(filter, name+'.txt')  # 生成txt文件名
        file = open(path, 'w', encoding="utf-8")
        # 句子保存（标签转换）
        for l in self.paper.sentences:
            lt = self.tag_map(l)  # 标签映射
            if lt[-2] != 'T':
                file.write(lt)
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
