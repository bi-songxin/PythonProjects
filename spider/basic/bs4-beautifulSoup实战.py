# # 安装
# # pip install bs4 -i 清华源
#
#
# # 案例1（已经变成post请求了）:北京新发地：http://www.xinfadi.com.cn/priceDetail.html

import requests
from bs4 import BeautifulSoup as bs
import csv
#
url = "https://www.douban.com/group/topic/486427751/?_spm_id=Nzg1NzM5MjY"

headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Mobile Safari/537.36',
    'cookie': 'Hm_lvt_6d4a8cfea88fa457c3127e14fb5fabc2=1778663993; HMACCOUNT=7D23520B9639B22D; bid=8T6fMoEnvpg; __utmc=30149280; __utmz=30149280.1778686036.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); dbcl2="215533639:N/s5nJZ3HyU"; ck=0HQe; push_noty_num=0; push_doumail_num=0; __utmv=30149280.21553; frodotk="b88aec6fe7e15a3329a0c54fb7a40e99"; talionusr="eyJpZCI6ICIyMTU1MzM2MzkiLCAibmFtZSI6ICJcdTk3MWNcdTRmMTEifQ=="; frodotk_db="69d57038e2aee8cb3d8050aaa80cba61"; ap_v=0,6.0; __utma=30149280.1310323802.1778686036.1778748294.1778902878.5; _gid=GA1.2.1246976284.1778903125; _ga=GA1.1.604519466.1778686752; __utmt=1; __utmb=30149280.61.0.1778904248474; Hm_lpvt_6d4a8cfea88fa457c3127e14fb5fabc2=1778904480; _ga_Y4GN1R87RG=GS2.1.s1778903125$o4$g1$t1778904481$j60$l0$h0'
}

resp = requests.get(url, headers=headers)
# print(resp.text)
# 解析数据
# 1.把页面源代码交给BeautifulSoup进行处理，生成bs对象

page = bs(resp.text, 'html.parser')  # 指定html解析器
# 2.从bs的标签（tag）对象中查找数据
# find(标签，属性=属性值) 只找第一次符合条件的，剩下符合条件的不选
# findall(标签，属性=属性值) 找全部符合条件的



title_name = page.find("title")
print(title_name)

# page_content = page.find("div",class_="rich-content topic-richtext")  #class是py的关键字，这里使用class_
# print(page_content)

with open('菜价.csv', 'wb') as f:
    csvwirter = csv.writer(f)
    page_content = page.find("div", attrs={"class": "rich-content topic-richtext"})  # 和上面等价，此时可以避免class
    print(page_content)

    # 拿到所有数据行
    trs = page_content.find_all("tr")[1:]
    for tr in trs:
        tds = tr.find_all("td")
        name = tds[0].text.strip()
        low = tds[1].text.strip()
        high = tds[2].text.strip()
        avg = tds[3].text.strip()
        guige = tds[4].text.strip()
        kind = tds[5].text.strip()
        date = tds[6].text.strip()

    csvwirter.writerow([title_name, low, high, avg, guige, kind, date])

print('over!')



import requests
from bs4 import BeautifulSoup as bs

# 案例2(被反爬了):豆瓣小组

url = "https://www.douban.com/group/topic/486427751/?_spm_id=Nzg1NzM5MjY"

headers = {
    'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Mobile Safari/537.36',
    'cookie':'Hm_lvt_6d4a8cfea88fa457c3127e14fb5fabc2=1778663993; HMACCOUNT=7D23520B9639B22D; bid=8T6fMoEnvpg; __utmc=30149280; __utmz=30149280.1778686036.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); dbcl2="215533639:N/s5nJZ3HyU"; ck=0HQe; push_noty_num=0; push_doumail_num=0; __utmv=30149280.21553; frodotk="b88aec6fe7e15a3329a0c54fb7a40e99"; talionusr="eyJpZCI6ICIyMTU1MzM2MzkiLCAibmFtZSI6ICJcdTk3MWNcdTRmMTEifQ=="; frodotk_db="69d57038e2aee8cb3d8050aaa80cba61"; ap_v=0,6.0; __utma=30149280.1310323802.1778686036.1778748294.1778902878.5; _gid=GA1.2.1246976284.1778903125; _ga=GA1.1.604519466.1778686752; __utmt=1; __utmb=30149280.61.0.1778904248474; Hm_lpvt_6d4a8cfea88fa457c3127e14fb5fabc2=1778904480; _ga_Y4GN1R87RG=GS2.1.s1778903125$o4$g1$t1778904481$j60$l0$h0'
}

resp = requests.get(url, headers=headers)
# print(resp.text)
# 解析数据
# 1.把页面源代码交给BeautifulSoup进行处理，生成bs对象

page = bs(resp.text,'html.parser') #指定html解析器
# 2.从bs的标签（tag）对象中查找数据
#find(标签，属性=属性值) 只找第一次符合条件的，剩下符合条件的不选
#findall(标签，属性=属性值) 找全部符合条件的


title_name = page.find("title")
print(title_name)

# page_content = page.find("div",class_="rich-content topic-richtext")  #class是py的关键字，这里使用class_
# print(page_content)

