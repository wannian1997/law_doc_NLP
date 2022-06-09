from elasticsearch import Elasticsearch
import uuid

from Data_Access.information_extraction import toJsonES


es = Elasticsearch(
    ["http://127.0.0.1:9200/"],  # 连接集群，以列表的形式存放各节点的IP地址
    # 在做任何操作之前，先进行嗅探
    # sniff_on_start=True,
    # 节点没有响应时，进行刷新，重新连接
    # sniff_on_connection_fail=True,
    # # 每 60 秒刷新一次
    # sniffer_timeout=60
)


def saveES(es, index_name, jsonES):
    """
        增，插入一个文档
    :param es: elasticsearch连接
    :param index_name: elasticsearch索引
    :param jsonES: 需要存储的json格式
    :return:
    """
    # 判断索引是否存在
    if not es.indices.exists(index=index_name):
        print(f"{index_name}索引不存在，终止操作，请检查原因。")
        return False

    # 先查询(根据案号，精确查找)
    search_body = {
        "query": {
            "term": {
                "case_ID": jsonES["case_ID"]
            }
        }
    }
    search_res = es.search(index=index_name, body=search_body)
    # 查询到的数目
    if search_res.body['hits']['total']['value'] > 0:
        print(jsonES["case_ID"] + "：案号已存在，终止操作。")
        return False

    # 执行插入操作
    timestamp_uuid = uuid.uuid1()  # 生成UUID
    insert_res = es.create(index=index_name, body=jsonES, id=timestamp_uuid)
    print(insert_res)
    return True


def deleteES(es, index_name, case_ID):
    """
        删，通过案号删除
    :param es:
    :param index_name:
    :param case_ID:
    :return:成功与否
    """
    # 查询
    search_body = {
        "query": {
            "term": {
                "case_ID": case_ID
            }
        }
    }
    search_res = es.search(index=index_name, body=search_body)
    if search_res.body['hits']['total']['value'] == 0:
        print("案号不存在，终止删除操作")
        return False
    uuid = search_res.body["hits"]["hits"][0]["_id"]
    print(uuid)
    delete_res = es.delete(index=index_name, id=uuid)   # 删除指定案号
    print(delete_res)
    return True


def searchES(es, index_name, item, words):
    """
        查
    :param es:
    :param index_name:
    :param item:
    :param words:
    :return:
    """
    # 精确查找部分
    items1 = ("case_ID", "paper_type", "indictment_ID", "date")
    if item in items1:
        search_body = {
            "query": {
                "term": {
                    item: words
                }
            }
        }
        search_res = es.search(index=index_name, body=search_body)
        print(search_res)
        return search_res.body

    # 模糊查找部分
    items2 = ("cause_of_action","paper_name","court","prosecution","defendants","fulltext")
    if item in items2:
        search_body = {
            "query": {
                "match": {
                    item: words
                }
            }
        }
        search_res = es.search(index=index_name, body=search_body)
        print(search_res)
        return search_res.body
    else:
        print("没有该项item内容，请检查item输入")
        return None


def updateES(es, index_name):
    # 更新数据(指定id更新数据，在es7之后要更新的数据需要用一个大字典包裹着，并且，key为doc )
    body = {'doc': {"defendants": [
        "曾林锋",
        "饶立明",
        "李某"
    ]}}  # 这个更新操作是在原来的基础上增加一个字段，而如果字段原来存在就会进行替换
    res = es.update(index='smartlaw', id='ae178531-e575-11ec-81c6-803049434c3a', body=body)
    print(res)



def main():
    docxPath = r'E:\docx\曾林锋饶立明非法采伐毁坏国家重点保护植物罪一案刑事一审判决书.docx'
    jsonFileFolder = r'D:\projects_pycharm\LawProcess\Data_Access'  # json文件所在文件夹,
    jsonES = toJsonES(docxPath, jsonFileFolder)
    # saveES(es, 'smartlaw', jsonES)
    # deleteES(es, 'smartlaw', jsonES["case_ID"])
    searchES(es, 'smartlaw','paper_name','曾林锋非法采伐毁坏国家重点保护植一案刑事一审')


if __name__ == '__main__':
    main()

    # body = {'query': {'match_all': {}}}
    # res = es.search(index='smartlaw', body=body)
    # print(res)

    # res=es.delete(index='smartlaw',id=1)   # 删除指定id
    # print(res)