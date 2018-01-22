import urllib.request
from bs4 import BeautifulSoup
keywords = '小米'
wd = urllib.request.quote(keywords)
url = 'http://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=0&rsv_idx=1&ch=12&tn=56060048_4_pg&wd='+wd
#url = url+'&rsv_pq=ff64d901000031d4&rsv_t=1b7cB%2FKAQLLDfettJz2WrartM10yMWFSwzgBoHAmYV2X6Dv3mqbDMJyJyfplrLpO%2BP8XKA&rsv_enter=1&rsv_sug3=5&rsv_sug1=4&rsv_sug2=0&inputT=6285&rsv_sug4=11467'
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
           'Accept':'text/html;q=0.9,*/*;q=0.8',
           'Accept-Charset':'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
           'Accept-Encoding':'gzip',
           'Connection':'close',
           'Referer':None #注意如果依然不能抓取的话，这里可以设置抓取网站的host
}
opener = urllib.request.build_opener()
opener.addheaders = [headers]

page = urllib.request.urlopen(url).read().decode('utf-8')


html = BeautifulSoup(page)
for i in range(1,11):
    res = html.find(id=i)
    print('第',i,'条结果：')
    if res.h3 != None:
        print(res.h3.get_text(strip=True))
    elif res.h4 != None:
        print(res.h4.get_text(strip=True))
    else:
        print('无法提取标题')
    if res.find('div',class_='c-abstract') !=None:
        print(res.find('div',class_='c-abstract').get_text(strip=True))
    elif res.find('div',class_='c-span18') !=None:
        if res.find('div',class_='c-span18').p !=None:
            print(res.find('div',class_='c-span18').p.get_text(strip=True))
        else:
            print(res.find('div',class_='c-span18').get_text(strip=True))
    else:
        print('无法提取描述')
    if res.find('span',class_='g') != None:
        print('网站：',res.find('span',class_='g').get_text(strip=True).split('/')[0])
    elif res.find('p',class_='op-bk-polysemy-move') !=None:
        print('网站：',res.find('p',class_='op-bk-polysemy-move').get_text(strip=True).split('/')[0])
    else:
        print('无法提取网址')
    print('\n')
