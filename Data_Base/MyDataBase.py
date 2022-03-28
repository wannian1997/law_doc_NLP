# -*- coding: utf-8 -*-
from sqlalchemy import Column, String, create_engine, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy

from Data_Access.Paper import Paper


# 创建对象的基类:
Base = declarative_base()


class PaperInfo(Base):
    """PaperInfo对象"""
    __tablename__ = 'paperinfo'

    # 表的结构
    caseID = Column(String(50), primary_key=True)
    cause_of_action = Column(String(45))
    paperName = Column(String(45))
    court = Column(String(45))
    paperType = Column(String(45))
    prosecution = Column(String(45))
    indictmentID = Column(String(45))
    time_of_case = Column(DateTime)
    date = Column(DateTime)


def insert_paper_info():
    # 初始化数据库连接:
    engine = create_engine('mysql+mysqlconnector://root:971022@localhost:3306/smartlaw')
    # 创建DBSession类型:
    DBSession = sessionmaker(bind=engine)

    # 创建session对象:
    session = DBSession()
    # 创建新paperinfo对象:
    new_paperinfo = PaperInfo(caseID='案号', cause_of_action='案由', paperName="文件名", court="fayuan", paperType="wenshuleixing",
                              prosecution="sdfsd", indictmentID="sdf", time_of_case="2020-01-01", date="2020-01-01")
    # 添加到session:
    session.add(new_paperinfo)
    try:
        # 提交即保存到数据库:
        session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        print("插入语句发生错误:\n",e)
    # 关闭session:
    session.close()
    """查询"""
    # 创建Session:
    session = DBSession()
    # 创建Query查询，filter是where条件，最后调用one()返回唯一行，如果调用all()则返回所有行:
    info = session.query(PaperInfo).filter(PaperInfo.caseID == '案号').one()
    # 打印类型和对象的name属性:
    print('type:', type(info))
    print('name:', info.caseID)
    # 关闭Session:
    session.close()


insert_paper_info()
# 单文档标注测试
path1 = r'E:\docx\暨附带民非法采伐毁坏国家重点保护植物一审刑事判决书.docx'
paper = Paper(path1)
