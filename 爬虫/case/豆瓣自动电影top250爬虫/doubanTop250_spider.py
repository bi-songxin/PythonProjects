import random  # 思路：
 # 1.拿到页面源代码 requests
 # 2.通过re来提取想要的有效信息 re

import requests
import re
import csv
import time
import random

# 自动复用 Cookie，更像真实用户连续浏览
session = requests.Session()

headers = {
    "user-agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Mobile Safari/537.36", # 告诉服务器我是浏览器访问的
    "Cookie":'bid=7EJEuIp8twk; _vwo_uuid_v2=DF453F4BAEABA4F64B3CEED8DDFA897AA|8455dd4574373604cf74cb25060324e9; ll="118282"; viewed="30329536_30486354_37143075_35799211"; __utmc=30149280; dbcl2="215533639:yMjX2jtcBgM"; ck=r8RB; push_noty_num=0; push_doumail_num=0; __utmv=30149280.21553; ct=y; _pk_id.100001.4cf6=ce913a29b82df31c.1777453229.; __utmz=30149280.1777453229.5.3.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __utmc=223695111; __utmz=223695111.1777453229.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __yadk_uid=OsAHTO0qphHZJWOloDfNt9BwsmNA07fY; _gid=GA1.2.1902143005.1777454309; _ga=GA1.1.253874942.1751468938; _ga_Y4GN1R87RG=GS2.1.s1777454309$o2$g1$t1777454429$j9$l0$h0; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1777461601%2C%22https%3A%2F%2Fwww.google.com.hk%2F%22%5D; ap_v=0,6.0; __utma=30149280.253874942.1751468938.1777456596.1777461601.7; __utma=223695111.253874942.1751468938.1777456596.1777461601.3',
    "Accept-Language":"zh-CN,zh;q=0.9", #像中国用户
    "Referer":"https://movie.douban.com/" #告诉服务器你是“从豆瓣内部点进来的”
}

# 解析数据
obj = re.compile(r'<li>.*?<div class="item">.*?<span class="title">(?P<name>.*?)'
                 r'</span>.*?<p>.*?<br>(?P<year>.*?)&nbsp.*?<span class="rating_num" property="v:average">(?P<score>.*?)</span>'
                 r'.*?<span>(?P<num_talk>.*?)</span>',re.S)



with open('top250.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    for start in range(0,250,25):
        url = f'https://movie.douban.com/top250?start={start}&filter='

        response = session.get(url, headers=headers)
        page_content = response.text
        # 开始匹配
        result = obj.finditer(page_content)
        for item in result:
            # print(item.group('name'))
            # print(item.group('year').strip())
            # print(item.group('score')
            # print(item.group('num_talk')
            dic = item.groupdict()
            dic['year'] = dic['year'].strip()
            writer.writerow(dic.values())

        # 随机等待3-6秒之间（含小数）
        time.sleep(random.uniform(3,6))

print('over!')


