# UI运行脚本文件
import sys
import win32com.client as wc
# PyQt5中使用的基本控件都在PyQt5.QtWidgets模块中
from PyQt5.QtWidgets import QApplication, QMainWindow,QFileDialog,QMessageBox
from PyQt5.QtCore import QDir
# 导入
from data_access.process_doc import read_docx
from data_access.TPaper import TPaper
from MFC import *

import os
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"


class MyMainForm(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyMainForm, self).__init__(parent)
        self.setupUi(self)

        self.index = 0  # 显示的第一条信息的索引
        # 信息栏可视化
        self.textBrowser_21.setText('程序加载成功！')
        # 添加登录按钮信号和槽。注意display函数不加小括号()
        self.pushButton.clicked.connect(self.openfile)  # 读取文件
        self.pushButton_1.clicked.connect(self.distest)  # 读取文件

    def openfile(self):
        # 单文档标注测试
        path1 = 'E:\\NLP\\02 Database\\Document\\非法采伐、毁坏国家重点保护植物罪(新)\\陈传福非法采伐国家重点保护植物罪一审刑事判决书.doc'
        self.paper = TPaper(path1)
        dic = self.paper.dict_label
        self.textBrowser_21.setText('100吴传宏非法捕捞水产品一审刑事判决书.doc\n文件读取成功!')
        self.info_disply10(0)

    def distest(self):
        self.textBrowser_21.setText('')

    def info_disply10(self, index):  # index为第一条数据的索引
        """显示从index开始的10条内容"""
        # 处理文本数据
        sentences_disply10 = []
        sentences_tag_display10 = []
        n = 0
        while n < 10:
            tag_t = self.paper.sentences[index + n][-2]
            sentences_disply10.append(self.paper.sentences[index+n].replace(f'\t{tag_t}\n', ''))  # 删除后缀
            sentences_tag_display10.append(tag_t)  # 获取句子标签
            n += 1
        # 显示
        self.textBrowser_1.setText(sentences_disply10[0])  # 文本信息
        self.textBrowser_2.setText(sentences_disply10[1])
        self.textBrowser_3.setText(sentences_disply10[2])
        self.textBrowser_4.setText(sentences_disply10[3])
        self.textBrowser_5.setText(sentences_disply10[4])
        self.textBrowser_6.setText(sentences_disply10[5])
        self.textBrowser_7.setText(sentences_disply10[6])
        self.textBrowser_8.setText(sentences_disply10[7])
        self.textBrowser_9.setText(sentences_disply10[8])
        self.textBrowser_10.setText(sentences_disply10[9])

        self.textBrowser_11.setText(sentences_tag_display10[0])  # 标签
        self.textBrowser_12.setText(sentences_tag_display10[1])
        self.textBrowser_13.setText(sentences_tag_display10[2])
        self.textBrowser_14.setText(sentences_tag_display10[3])
        self.textBrowser_15.setText(sentences_tag_display10[4])
        self.textBrowser_16.setText(sentences_tag_display10[5])
        self.textBrowser_17.setText(sentences_tag_display10[6])
        self.textBrowser_18.setText(sentences_tag_display10[7])
        self.textBrowser_19.setText(sentences_tag_display10[8])
        self.textBrowser_20.setText(sentences_tag_display10[9])

        self.n1.setText(str(index))  # 序号
        self.n2.setText(str(index+1))
        self.n3.setText(str(index+2))
        self.n4.setText(str(index+3))
        self.n5.setText(str(index+4))
        self.n6.setText(str(index+5))
        self.n7.setText(str(index+6))
        self.n8.setText(str(index+7))
        self.n9.setText(str(index+8))
        self.n10.setText(str(index+9))


if __name__ == '__main__':
    # 固定的，PyQt5程序都需要QApplication对象。sys.argv是命令行参数列表，确保程序可以双击运行
    app = QApplication(sys.argv)
    # 初始化
    myWin = MyMainForm()
    # 将窗口控件显示在屏幕上
    myWin.show()
    # 程序运行，sys.exit方法确保程序完整退出。
    sys.exit(app.exec_())
