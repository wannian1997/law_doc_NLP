"""基于统计的自然语言处理"""
from Paper import Paper
from process_doc import list2txt
import jieba
import os

def docx_words(file_path):
    """单篇文书"""
    paper = Paper(file_path)
    words_list = [['初始化值', 0]]
    for p in paper.sentences:
        words = jieba.cut(p[0])  # 分词
        for word in words:
            old_word_flag = 0
            for wl in words_list:  # 检索该词是否存在
                if word == wl[0]:  # 存在
                    old_word_flag = 1
                    word_index = words_list.index(wl)
                    break
                else:
                    continue

            if old_word_flag:
                words_list[word_index][1] = 1 + words_list[word_index][1]  # 计数加一
            else:
                if len(word) > 1:  # 过滤无效信息
                    words_list.append([word, 1])  # 加词
    del words_list[0]

    def takeSecond(words_list):
        return words_list[1]

    words_list.sort(key=takeSecond, reverse=True)
    for wl in words_list:
        print(wl)
    return words_list


def docxs_words(filter_path):
    """批量文书词统计"""
    words_list = [['初始化值', 0]]
    path_list = os.listdir(filter_path)
    total = len(path_list)
    n = 1
    for pl in path_list:
        # 百分比
        print(f'{(n / total) * 100}%')
        n += 1

        filename_t, type_t = os.path.splitext(pl)
        if type_t != '.docx':  # 过滤文件类型
            continue
        path_temp = os.path.join(filter_path, pl)
        paper = Paper(path_temp)
        print(pl)
        print(len(words_list))
        for p in paper.sentences:
            print(p)
            if p[1][0] != '5':
                continue
            words = jieba.cut(p[0])  # 分词
            for word in words:
                old_word_flag = 0
                for wl in words_list:  # 检索该词是否存在
                    if word == wl[0]:  # 存在
                        old_word_flag = 1
                        word_index = words_list.index(wl)
                        break
                    else:
                        continue

                if old_word_flag:
                    words_list[word_index][1] = 1 + words_list[word_index][1]  # 计数加一
                else:
                    if len(word) > 1:  # 过滤无效信息
                        words_list.append([word, 1])  # 加词
            if p[1][0] != '6':  # 提前终止条件
                break

    del words_list[0]

    # 按频率排序
    def takeSecond(words_list):
        return words_list[1]

    words_list.sort(key=takeSecond, reverse=True)
    for wl in words_list:
        print(wl)
    return words_list


if __name__ == '__main__':
    path1 = r'E:\NLP\02Database\Document\非法采伐、毁坏国家重点保护植物罪(新)\docx'
    path2 = r'C:\Users\songwannian\Desktop\新建文件夹'
    docxs_words_list = docxs_words(path2)
    print(docxs_words_list)
    for s in docxs_words_list:
        print(s)
    list2txt(docxs_words_list, r'C:\Users\songwannian\Desktop\docxs_words_list.txt')