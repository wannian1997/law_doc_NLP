# coding:utf-8
from xml.dom import minidom
import os

from Data_Access.Paper import Paper


# 写入xml文档的方法
def create_xml_test(docxPath, saveFolder):
    xml = minidom.Document()
    paper = xml.createElement('paper')
    xml.appendChild(paper)

    docx = Paper(docxPath)
    for key, value in docx.dict_label.items():
        # 添加段落块
        paras = xml.createElement('paras')
        paras.setAttribute('label', key)
        paper.appendChild(paras)
        for index in value:
            # 添加段
            para = xml.createElement('para')
            # 添加文本信息
            status_text = xml.createTextNode(docx.paras[index])
            para.appendChild(status_text)
            para.setAttribute('index', str(index))
            paras.appendChild(para)

    # 解析文件名
    saveFilename = os.path.basename(docxPath).split('.')[0]
    f = open(saveFolder + "\\" + saveFilename + ".xml", 'w', encoding='utf-8')  # 编码格式
    t = saveFolder + saveFilename + ".xml"
    f.write(xml.toprettyxml())
    f.close()


def main():
    docxPath = r'E:\docx\26被告人董连元非法采伐国家重点保护植物一审刑事判决书.docx'
    folderPath = r"D:\projects_pycharm\LawProcess\Data_Base\xml"
    create_xml_test(docxPath, folderPath)


if __name__ == '__main__':
    main()