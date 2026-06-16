# 需求：爬取电影天堂的迅雷电影资源板块下的电影电影名称和下载链接种子

"""
思路：
1.获取迅雷电影资源板块的跳转链接
2.获取跳转链接的电影名称和种子链接
3.保存到csv中
"""

import csv
import requests
import re
import time
import random
import html

# 获取迅雷电影资源板块下到链接

url = 'https://www.dygod.vip/'

headers = {
    "User-Agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Mobile Safari/537.36",
    "Accept-Language":"zh-CN,zh;q=0.9",
    "Referer":"https://www.dygod.vip/",
    "cookie":"Hm_lvt_bbe43e7ccd3be8349687c42bc5b6c349=1778664126; HMACCOUNT=7D23520B9639B22D; Hm_lpvt_bbe43e7ccd3be8349687c42bc5b6c349=1778664896"

}
session = requests.Session()
resp = session.get(url, headers=headers)
resp.encoding='gb2312'
# print(resp.text)

obj = re.compile(r'迅雷电影资源.*?<ul>(?P<ul>.*?)</ul>',re.S)
obj2 = re.compile(r"<li><a href='(?P<href>.*?)'",re.S)
obj3 = re.compile(r'◎片　　名　(?P<movie>.*?)<br />.*?'
                  r'<td style="WORD-WRAP: break-word" bgcolor="#fdfddf"><a href="(?P<maget>.*?)">',re.S)

result1 = obj.finditer(resp.text)
# print(result1) #迭代器<callable_iterator object at 0x12b0dae60>
child_href_list =[]

for it in result1:
    # print(it)
    ul = it.group('ul')

    # 提取子页面链接：
    result2 = obj2.finditer(ul)
    for itt in result2:
        child_href = url + itt.group('href').strip('/')
        child_href_list.append(child_href)

# print(child_href_list)
# 获取跳转链接的电影名称和种子链接
with open('heaven.csv','a',encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['电影名','磁力链接'])
    for it in child_href_list:
        response = session.get(it,headers=headers,timeout=10)
        response.encoding='gb2312'
        s = obj3.finditer(response.text)
        for it in s:
            movie = html.unescape(it.group('movie'))
            maget = it.group('maget')
            print(movie,maget)
            writer.writerow([movie,maget])

        time.sleep(random.uniform(3,8))

print('over!')