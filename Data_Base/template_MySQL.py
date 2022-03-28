import pymysql

from Data_Access.Paper import Paper


def search(connection, table, caseID) -> tuple:
    """
    检查table中是否已经包含id
    :param connection: 数据库连接
    :param table: 表格名
    :param caseID: 案号
    :return: 返回一个元组
    """
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = connection.cursor()
    cursor.execute(f'select * from {table} where caseID="{caseID}"')
    values = cursor.fetchall()
    return values


def isExist(connection, table, caseID) -> bool:
    """判断该文件是否存在，返回布尔型"""
    values = search(connection, table, caseID)
    if len(values) == 0:
        return False
    else:
        return True


# 单文档标注测试
path1 = r'E:\docx\暨附带民非法采伐毁坏国家重点保护植物一审刑事判决书.docx'
paper = Paper(path1)

# 打开数据库连接
conn = pymysql.connect(host='localhost',
                       user='root',
                       password='971022',
                       database='smartlaw')

# 使用 cursor() 方法创建一个游标对象 cursor
cursor = conn.cursor()

print(isExist(conn, 'paper', 'test'))
# SQL 插入语句
sql = f"INSERT INTO paper(caseID,label00,label10, \
      label20,label30,label40,label50,label60,label70,label80,label90)\
      VALUES ('test', '', '', '', '', '', '', '', '', '', '')"

try:
    # 执行sql语句
    cursor.execute(sql)
    # 提交到数据库执行
    conn.commit()
except pymysql.err.IntegrityError as e:  # 捕捉错误
    # 如果发生错误则回滚
    conn.rollback()
    print("插入语句发生错误:\n", e)

# 关闭数据库连接
conn.close()