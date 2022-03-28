from Data_Access.Paper import Paper


class PaperInfo(Paper):
    """对裁判文书进行信息抽取"""
    # 状态信息

    # paper_info 表格信息
    case_ID = ''
    cause_of_action = ''
    paper_number = ''
    court = ''
    paper_type = ''
    prosecution = ''
    indictment_ID = ''
    time_of_case = ''
    date = ''

    def __init__(self, docx_path):
        super().__init__(docx_path)  # 调用父类的构造函数
        self.extract_paper_info()

    def extract_paper_info(self):
        # self.case_ID = self.paras[self.dict_label['label30']]
        pass

def temp(path):
    # 单文档标注测试
    paper = PaperInfo(path)
    for key, value in paper.dict_label.items():
        print(key, value)

    for p in paper.paras:
        print(p)

    for s in paper.sentences:
        print(s)


if __name__ == '__main__':
    path = r'E:\docx\暨附带民非法采伐毁坏国家重点保护植物一审刑事判决书.docx'
    paper_info = PaperInfo(path)
    temp(path)