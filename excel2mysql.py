# -*- coding: utf-8 -*-
__author__ = 'luhui.liu'

import xlrd
import pymysql

# Open the workbook and define the worksheet
book = xlrd.open_workbook("xszxcjd_xy.xls")
sheet = book.sheet_by_name("Page1")

# 建立一个MySQL连接
conn = pymysql.connect(host="115.159.203.174", user="root", passwd="***", db="scrapyspider")
conn.set_charset('utf8')


# 获得游标对象, 用于逐行遍历数据库数据
cursor = conn.cursor()
cursor.execute('SET NAMES utf8;') 
cursor.execute('SET CHARACTER SET utf8;')
cursor.execute('SET character_set_connection=utf8;')
# 创建插入SQL语句
insert_sql = """
  INSERT INTO report_of_6080 (id, name ,sltj, mzt, zrbzf, zhyy ,rjgcgl, rjtxjg, yyxz, bxjs, ydyjsfwd, fbsjs, sjwj, mddxffjc,dsjjs,sjkxt,ydyjsdl,qyydyyykf,xnhyyjs,qyjg,ydkfjs) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
 """

# 定义一个成绩名字的字典
report_6080 = {"数理统计*": "**",
               "中国特色社会主义理论与实践研究*": "**",
               "自然辩证法概论*": "**",
               "综合英语（2）*": "**",
               "软件过程与管理*": "**",
               "软件体系结构理论与应用*": "**",
               "英语写作*": "**",
               "并行计算架构与模式*": "**",
               "移动云计算服务端技术": "**",
               "分布式计算": "**",
               "数据挖掘": "**",
               "面向对象方法精粹": "**",
               "大数据技术": "**",
               "数据库系统原理与应用": "**",
               "移动云计算导论": "**",
               "企业移动云应用开发": "**",
               "虚拟化与云计算": "**",
               "企业架构与系统分析设计": "**",
               "移动开发技术": "**",
               }
# 读取id和name
number = 0
id = sheet.cell(2, 1).value
name = sheet.cell(2, 3).value
# 遍历６到25行有效成绩行
for r in range(6, 25):
    temp_name = sheet.cell(r, 0).value
    temp_score = sheet.cell(r, 4).value
    if (temp_score != '/'):
        report_6080[temp_name] = temp_score
    else:
        report_6080[temp_name] = sheet.cell(r, 5).value


# 执行sql语句
cursor.execute(insert_sql, (id,name,report_6080["数理统计*"],report_6080["中国特色社会主义理论与实践研究*"],report_6080["自然辩证法概论*"],
               report_6080["综合英语（2）*"],report_6080["软件过程与管理*"],report_6080["软件体系结构理论与应用*"],report_6080["英语写作*"],
               report_6080["并行计算架构与模式*"],report_6080["移动云计算服务端技术"],report_6080["分布式计算"],report_6080["数据挖掘"],
               report_6080["面向对象方法精粹"],report_6080["大数据技术"],report_6080["数据库系统原理与应用"],report_6080["移动云计算导论"],
               report_6080["企业移动云应用开发"],report_6080["虚拟化与云计算"],report_6080["企业架构与系统分析设计"],report_6080["移动开发技术"]))
number=number+1
# 关闭游标
cursor.close()

# 提交
conn.commit()

# 关闭数据库连接
conn.close()

# 打印结果
print("")
print("Done! ")
print("")
#columns = str(sheet.ncols)
#rows = str(sheet.nrows)
print("一共",number,"条数据到MySQL!")
