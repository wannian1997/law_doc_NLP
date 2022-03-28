import pymysql

from Data_Access.Paper import Paper


# 单文档标注测试
path1 = r'E:\docx\暨附带民非法采伐毁坏国家重点保护植物一审刑事判决书.docx'
paper = Paper(path1)

# 打开数据库连接
db = pymysql.connect(host='localhost',
                     user='root',
                     password='971022',
                     database='smartlaw')

# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()
# SQL 插入语句
sql = f"INSERT INTO paper(caseID,label00,label10, \
      label20,label30,label40,label50,label60,label70,label80,label90)\
      VALUES ('test', '', '', '', '', '', '', '', '', '', '')"

try:
    # 执行sql语句
    cursor.execute(sql)
    # 提交到数据库执行
    db.commit()
except pymysql.err.IntegrityError as e:  # 捕捉错误
    # 如果发生错误则回滚
    db.rollback()
    print("插入语句发生错误:\n", e)

# 关闭数据库连接
db.close()