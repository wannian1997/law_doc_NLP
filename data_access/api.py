import json

from information_extraction import toJson


def docx2XJ(docxPath, jsonFolderPath):
    # docx文件路径，xml文件所在文件夹路径，json文件所在文件夹路径
    # 自动生成同名文件
    toJson(docxPath, jsonFolderPath)


def main():
    # 从path.json文件中读取三个路径
    dic = json.load(open('path.json', 'r', encoding="utf-8"))
    docxPath = dic["docxPath"]
    jsonFolderPath = dic["jsonFolderPath"]
    print(dic)
    docx2XJ(docxPath, jsonFolderPath)


if __name__ == "__main__":
    main()