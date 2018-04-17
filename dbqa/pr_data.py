#!/usr/bin/python
# -*- coding:utf-8 -*-


__author__ = 'luhui.liu'


from collections import Counter
import jieba
import codecs
from tqdm import tqdm
import re


filepath = "../train_data/nlpcc-iccpol-2016.dbqa.training-data"
targetFile = "../train_data/nlpcc-iccpol-2016.dbqa.training-data_split_stop"


# @see 读取文件内容
def readFile(filename):
    content = ""
    try:
        fo = codecs.open(filename, 'r', "utf-8")
        print("读取文件名：", filename)

        for line in fo.readlines():
            content += line
        print("字数：", len(content))

    except IOError as e:
        print("文件不存在或者文件读取失败")

        return ""
    else:
        fo.close()
        # re_han.split(sentence)
        return content


# @see 写入文件内容（数组会使用writelines进行写入）codec.open实现
# @param toFile 文件名
#        content 内容
def writeFile(toFile, content):
    try:
        fo = codecs.open(toFile, 'wb', "utf-8")
        print("文件名：", toFile)

        if type(content) == type([]):
            fo.writelines(content)
        else:
            fo.write(content)
    except IOError:
        print("没有找到文件或文件读取失败")

    else:
        print("文件写入成功")
        fo.close()

def jieba_cut(rawContent):
    """
    结巴分词，默认不用停用词
    :param rawContent: 原内容
    :return: 目标内容
    """

    data_temp = ''.join(re.findall(u'[\u4e00-\u9fff]+', rawContent))  # 必须为unicode类型，取出所有中文字符
    # sts = data.translate(None, string.punctuation)            # 删除英文的标点符号，中文标点不支持。
    jieba.enable_parallel(4)  # 开启并行分词模式，参数为并行进程数
    #jieba.disable_parallel()  # 关闭并行分词模式

    #自定义停用词库
    #jieba.analyse.set_stop_words("../")

    seg_list = jieba.cut(data_temp, cut_all=False)
    # 把分词结果写到目标文件（targetFile）中，这里是用空格分割，也可以改成其他符号
    output = " ".join(seg_list)
    return output


def count_tf(rawContent):


    fileout_path=""
    wlist = rawContent.split()      # 将分词结果按空格切割为列表（字符串的切割）
    num_dict = Counter(wlist)  # 统计词频

    # 统计结果写入result.txt(字典的遍历)
    for (k, v) in num_dict.items():
        codecs.open('data/result.txt', 'a+', "utf-8").write(str(k) + ' ' + str(v) + '\n')   # 将k，v转换为str类型


if __name__ == '__main__':
    #结巴分词
    output_content = readFile(filepath)
    writeFile(targetFile,output_content)
