#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'luhui.liu'
import sys
import time
import urllib.request
#from BeautifulSoup  import BeautifulSoup 旧的版本
from bs4  import BeautifulSoup
import os
import json
mymap=['0','1','2','3','4','5','6','7']




#根据关键字获取查询网页
def baidu_search(key_words,pagenum):
    url='http://www.baidu.com/s?wd='+key_words+'&pn='+mymap[pagenum]
    html=urllib.request.urlopen(url).read()
    return html

 #处理一个要搜索的关键字
def deal_key(key_words):
    if os.path.exists('data')==False:
        os.mkdir('data')
    filename='data\\'+key_words+'.json'
    data = []
    # 打开方式用‘w'时，下边的写要str转换，而对于网页要编码转换，遇到有些不规范的空格还出错
    fp=open(filename,'w',encoding='utf-8')
    if fp:
        pass
    else:
        print('文件打失败：'+filename)
        return
    x=0
    while x<=0:
        htmlpage=baidu_search(key_words,x)
        soup=BeautifulSoup(htmlpage)
        # 这个格式应该参考百度网页布局
        for item in soup.findAll("div", {"class": "result"}):
            a_click = item.find('a')
            # 标题
            if a_click:
                title = a_click.get_text()
            # 链接
            if a_click:
                url = a_click.get("href")
            c_abstract=item.find("div", {"class": "c-abstract"})
            # 描述
            if c_abstract:
                strtmp=c_abstract.get_text()
            data_tmp = {"title":title,"abstract":strtmp,"url":url}
            print("[JSON]:",data_tmp)
            #写入json
            data.append(data_tmp)
        x=x+1
        #fp.write(b'\n')
        print("--------------------")
    json.dump(data, fp, ensure_ascii=False)
    fp.close()

#读取搜索文件内容，依次取出要搜索的关键字
def search_file():
    fp=open('searchfile.txt')
    keyword=fp.readline()
    print("[keyword]:"+keyword)
    while keyword:
        nPos=keyword.find('\n')
        if nPos>-1:
            keyword=keyword[:-1]#keyword.replace('\n','')
        deal_key(keyword)
        keyword=fp.readline()

#脚本入口
print('Start:')
search_file()
print('End！')