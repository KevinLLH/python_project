#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'luhui.liu'

import xlrd
import xlwt
import re
from elasticsearch import Elasticsearch

es = Elasticsearch()

dicts = {"怎样", "怎么", "如何", "什么", "为什么"}
dicts_sub = {"锁车":"锁车设防"}


# 向es写入数据
def write_es(filename):
    # # Open the workbook and define the worksheet
    book = xlrd.open_workbook("data/" + filename)
    sheet = book.sheet_by_name("Sheet1")
    actions = []
    # 遍历Excel中的数据
    start_num = 1 #计数用
    for r in range(1, sheet.nrows):
        type = str(sheet.cell(r, 0).value)
        if type.strip() == '':
            type = 'NULL'  # 如果类型为空则赋值NULL
        content = sheet.cell(r, 1).value
        content = re.sub('\[.*?jpg\]', '', content) #去除content开头的[image**.jpg]
        if len(content) < 10: #长度小于十不写入es中
            continue
        es.index(index="answers", doc_type="list", body={"type": type, "content": content}) #写入es
        start_num += 1
        print(type)
        print(content)

    print("[write2es.write_es]:一共加入了：", start_num)


def query_es(query_file):
    # 创建一个Workbook对象，这就相当于创建了一个Excel文件
    workbook = xlwt.Workbook(encoding='ascii')
    worksheet = workbook.add_sheet('My Worksheet')

    # 读取问题列表
    book = xlrd.open_workbook("data/" + query_file)
    sheet = book.sheet_by_name("Sheet1")
    # 遍历数据
    start_num = 0 # 记录写入行数
    for r in range(1, sheet.nrows):
        query_string = str(sheet.cell(r, 0).value)
        print("[write2es.query_es.query]:"+query_string)
        worksheet.write(start_num, 0, label=query_string)  # 其中的'0-行, 0-列'指定表中的单元，写入query
        # 去除query中的怎么，什么等词
        for temp_string in dicts:
            query_string = query_string.replace(temp_string, "")
        start_num += 1
        res = es.search(index="answers", doc_type="list",
                        body={"query": {"match": {"content": query_string}}, "from": 0, "size": 10})
        # 写入excel中
        for i in range(len(res['hits']['hits'])):
            content_string = res['hits']['hits'][i]['_source']['content']
            worksheet.write(start_num, 0, label=content_string)  # 其中的'0-行, 0-列'指定表中的单元，写入answer
            start_num += 1
            print("[write2es.query_es.content]:"+content_string)

    workbook.save('answers.xls')
    print("[write2es.query_es]:query is over!")


def check_sub(filename):
    # 修改为写入文本
    fw = open('data/car_answer_simple.txt', 'w',encoding="utf-8")
    num_total = 0 #一共问题数
    num_true = 0 # 正确的问题数
    start_num = 0
    #index_answer1 = 0 # 定位每个问题第一个答案位置


    with open('data/'+filename, 'r',encoding='utf-8') as f:
        for line in f.readlines():
            list_answers = []
            num_total+=1

            sign = True
            query_string = line.strip().split()[0]
            answer_true = line.strip().split("	")[1]
            #list_answers.append(query_string+" "+answer_true+"	1")
            # 去除query中的怎么，什么等词
            for temp_string in dicts:
                query_string_out = query_string.replace(temp_string, "")
            start_num += 2
            res = es.search(index="answers", doc_type="list",
                            body={"query":  {"multi_match":{"query": query_string_out ,"fields": ["type^2","content"]}}, "from": 0, "size": 10})
            # 写入excel中
            for i in range(len(res['hits']['hits'])):
                content_string = res['hits']['hits'][i]['_source']['content']
                if content_string==answer_true and sign:
                    print(answer_true)
                    print(content_string)
                    print("***********")
                    num_true +=1
                    sign = False
                    list_answers.append(query_string + "    " + content_string + "  1")
                    continue
                list_answers.append(query_string+"	"+content_string+"	0")
                start_num += 1
                #print("[write2es.query_es.content]:" + content_string)
            if sign:
                list_answers.append(query_string + "    " + answer_true + " 1")
            for num_i in range(len(list_answers)):
                fw.write(list_answers[num_i]+"\n")
        #计算正确率
        result = num_true/num_total
        fw.write("正确率为：" + str(result))
    fw.close()
    print("[write2es.check_sub]:check_sub is over!")




if __name__ == '__main__':
     #write_es("01瑞虎5车型电器维修手册.xlsx")
     #write_es("02奇瑞瑞虎5功能使用快速入门.xlsx")
     #write_es("03奇瑞瑞虎5使用说明书.xlsx")
    #query_es("提问.xlsx")
    check_sub("car_answer_simple")
