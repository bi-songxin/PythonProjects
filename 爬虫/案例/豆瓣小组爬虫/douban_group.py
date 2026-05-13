"""
需求：
爬取豆瓣「适老化改造促进会」小组（ID: 732378）的所有公开帖子（标题、正文、评论），存储为CSV文件。
"""


import csv
import requests
import re
import time
import random
import html




headers = {
    "User-Agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Mobile Safari/537.36",
    "Accept-Language":"zh-CN,zh;q=0.9",
    "Referer":"https://www.douban.com/group/732378/discussion",
    "Cookie":'_pk_id.100001.8cb4=44d8ae034b95eec6.1778685950.; _pk_ses.100001.8cb4=1; bid=8T6fMoEnvpg; ap_v=0,6.0; __utma=30149280.1310323802.1778686036.1778686036.1778686036.1; __utmc=30149280; __utmz=30149280.1778686036.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmt=1; __yadk_uid=12J8ar8pCn4J5lVtoFZm5MuSUHdJbO1R; dbcl2="215533639:N/s5nJZ3HyU"; ck=0HQe; push_noty_num=0; push_doumail_num=0; __utmv=30149280.21553; __utmb=30149280.135.0.1778686573035',
    "connection":"keep-alive"

}

session = requests.Session()
#  预编译正则表达式
obj = re.compile(r'<a href="(?P<href>.*?)" title="',re.S)
# 匹配标题、正文
obj2 = re.compile(r'"text": "(?P<text>.*?)",.*?"name": "(?P<title>.*?)",.*?<div class="markdown">.*?'
                  r'<p>(?P<talk>.*?)</p>',re.S)

# 分页爬取
for start in range(0,25,25):
    url = f'https://www.douban.com/group/732378/discussion?start={start}&type=new'
    resp = session.get(url, headers=headers,timeout=10)
    # print(resp.text)
    href = obj.finditer(resp.text)
    for it in href:
        result1 = it.group('href')
        print(result1)
    #
    #     # 爬取每个子链接
    #     resp2 = session.get(result1, headers=headers,timeout=10)
    #     result2 = obj2.finditer(resp2.text)
    #     for it in result2:
    #         print(it.group('title'))
    #         print(it.group('text'))
    #         print(it.group('talk'))
    #     # 爬完一个页面后休息
    #     time.sleep(random.uniform(3, 8))
    # # 爬完一分页后休息
    # time.sleep(random.uniform(3,8))


