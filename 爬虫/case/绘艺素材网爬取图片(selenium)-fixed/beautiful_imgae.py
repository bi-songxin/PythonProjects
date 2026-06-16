# 1.拿到主页面的源代码，然后提取到子页面的链接地址，href
# 2.通过href拿到子页面的内容。从子页面中找到图片的下载地址 img -> src
# 3.下载图片


import requests
from bs4 import BeautifulSoup as bs

headers = {
    'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Mobile Safari/537.36',
    'accept-language':'zh-CN,zh;q=0.9',
    'referer':'https://m.huiyi8.com/',
    'cookie':'Hm_lvt_4c65a21638f96d83db9e42a8df2772a9=1778978504; HMACCOUNT=7D23520B9639B22D; Hm_lpvt_4c65a21638f96d83db9e42a8df2772a9=1778980536; t=1010671f87f4519c52a828003ebb0acb; r=7723'
}
url ="https://m.huiyi8.com/"
resp = requests.get(url,headers=headers)
# resp.encoding ='utf-8' # 处理乱码
print(resp.text)
# 把源代码交给bs

# main_page = bs(resp.text,"html.parser")
# alist = main_page.find("div",class_= "TypeList").find_all("a")
# # print(alist)
#
# for a in alist:
#     href = a.get('href')# 直接通过qet就可以拿到属性的值
#     # 拿到子页面的源代码
#     child_page_resp= requests.get(href)
#     child_page_resp.encoding ='utf-8'
#     child_page_text = child_page_resp.text
#
#     # 从子页面中拿到图片的下载路径
#     child_page = bs(child_page_text, "html.parser")
#     p = child_page.find("p", align="center")
#     img = p.find("img")
#     src = img.get("src")
#
#     # 下载图片
#     img_resp = requests.get(src)
#     # img_resp.content # 这里拿到的是字节
#     img_name = src.split("/")[-1] # 拿到url中的最后一个/以后的内容
#     with open("img/"+img_name, mode="'wb") as f:
#         f.write(img_resp.content)  # 图片内容写入文件