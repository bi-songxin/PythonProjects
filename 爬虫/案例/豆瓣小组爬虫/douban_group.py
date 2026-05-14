"""
需求：
爬取豆瓣「适老化改造促进会」小组（ID: 732378）的所有公开帖子（标题、正文、评论），存储为CSV文件。
"""


# import csv
# import requests
# import re
# import time
# import random
# import html
#


import csv
import requests
import time
import random
import html
from bs4 import BeautifulSoup

# ================== 配置 ==================
headers_list = [
    # 可以加入多个 User-Agent，随机切换
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.96 Mobile Safari/537.36",
]

cookie = 'Hm_lvt_6d4a8cfea88fa457c3127e14fb5fabc2=1778663993; HMACCOUNT=7D23520B9639B22D; bid=8T6fMoEnvpg; __utmc=30149280; __utmz=30149280.1778686036.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); dbcl2="215533639:N/s5nJZ3HyU"; ck=0HQe; push_noty_num=0; push_doumail_num=0; __utmv=30149280.21553; frodotk="b88aec6fe7e15a3329a0c54fb7a40e99"; talionusr="eyJpZCI6ICIyMTU1MzM2MzkiLCAibmFtZSI6ICJcdTk3MWNcdTRmMTEifQ=="; frodotk_db="69d57038e2aee8cb3d8050aaa80cba61"; _gid=GA1.2.674843540.1778686752; ap_v=0,6.0; __utma=30149280.1310323802.1778686036.1778690370.1778739600.3; __utmt=1; __utmb=30149280.88.4.1778742459985; Hm_lpvt_6d4a8cfea88fa457c3127e14fb5fabc2=1778742486; _ga_Y4GN1R87RG=GS2.1.s1778742487$o2$g0$t1778742487$j60$l0$h0; _ga=GA1.2.604519466.1778686752'

session = requests.Session()
session.headers.update({
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Referer": "https://www.douban.com/group/732378/discussion?start=0&type=new",
    "Cookie": cookie
})

base_url = "https://www.douban.com/group/732378/discussion"

# ================== CSV 文件 ==================
csv_file = "douban_group.csv"
with open(csv_file, "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)
    writer.writerow(["标题", "内容", "评论"])

    # ================== 分页 ==================
    for start in range(0, 25, 25):
        page_url = f"{base_url}?start={start}&type=new"
        print(f"正在抓取页面: {page_url}")

        # 随机选择一个 User-Agent
        session.headers["User-Agent"] = random.choice(headers_list)
        resp = session.get(page_url, timeout=10)
        soup = BeautifulSoup(resp.text, "html.parser")

        # ================== 获取帖子链接 ==================
        post_links = list(set([a.get("href") for a in soup.select('a[href*="/group/topic/"]') if "/group/topic/" in a.get("href")]))
        random.shuffle(post_links)  # 随机顺序，模拟真实点击

        for href in post_links:
            try:
                # 随机切换 User-Agent
                session.headers["User-Agent"] = random.choice(headers_list)
                resp2 = session.get(href, timeout=10)
                soup2 = BeautifulSoup(resp2.text, "html.parser")

                # -------- 标题 --------
                title_tag = soup2.find("title")
                title = html.unescape(title_tag.text).strip().replace(" - 豆瓣", "") if title_tag else ""

                # -------- 正文 --------
                content_tag = soup2.select_one("div.rich-content topic-richtext p")
                content = html.unescape(content_tag.get_text(separator="\n").strip()) if content_tag else ""

                # -------- 评论（一级评论） --------
                comment_tags = soup2.select("div.markdown p")
                comments = [html.unescape(c.get_text(strip=True)) for c in comment_tags]
                comments_str = " || ".join(comments)

                # -------- 写入 CSV --------
                writer.writerow([title, content, comments_str])
                print(f"抓取成功: {title}")

                # 随机延时，模拟真实浏览
                time.sleep(random.uniform(5, 15))

            except Exception as e:
                print("抓取失败:", e)
                # 失败休息久一点
                time.sleep(random.uniform(10, 20))

        # 分页休息
        time.sleep(random.uniform(10, 20))
#
# session = requests.Session()
# #  预编译正则表达式
# obj = re.compile(r'<a href="https://www.douban.com/group/topic/(?P<href>.*?)" title="',re.S)
# # 匹配标题
# obj2 = re.compile(r'<title>(?P<title>.*?)</title>',re.S)
#
# # 匹配内容
# obj3 = re.compile(r'<p data-align="left">(?P<content>.*?)</p>',re.S)
#
# # 子链接相同部分
# obj_url = 'https://www.douban.com/group/topic/'
#
# # 分页爬取
# for start in range(0,25,25):
#     url = f'https://www.douban.com/group/732378/discussion?start={start}&type=new'
#     resp = session.get(url, headers=headers,timeout=10)
#     # print(resp.text)
#     href = obj.finditer(resp.text)
#     for it in href:
#         result1 = it.group('href')
#         # 拼接子链接
#         child_url = obj_url + result1
#         # print(child_url)
#
#         # 爬取每个子链接
#         resp2 = session.get(child_url, headers=headers,timeout=10)
#         result2 = obj2.search(resp2.text)
#         result3 = obj3.search(resp2.text)
#         # if result2:
#         #     print(result2.group('title').strip().replace(' - 豆瓣',''))
#
#         if result3:
#             print(result3.group('content'))
#
#         # 爬完一个页面后休息
#         time.sleep(random.uniform(4, 8))
#     # 爬完一分页后休息
#     time.sleep(random.uniform(4,8))


"""
总结：
regex的弊端（缺点）：
在一个预编译正则表达式里面插入多个分组名字，要看两者之间的元素距离：
1.相近，直接使用
使用finditer，迭代一下

2.太远，不要在一个预编译正则表达式里面使用多个(?P<分组名字>正则)，否则在整个html里面疯狂回溯，以为程序卡死了一样
使用search匹配第一次出现的，配合if
"""