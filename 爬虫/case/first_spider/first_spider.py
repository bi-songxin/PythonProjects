# 爬虫:通过编写程序来获取到互联网上的资源
# 百度
# 需求:用程序模拟浏览器输入一个网址，从该网址中获取到资源或者内容

from urllib.request import urlopen

url = 'https://www.baidu.com/'
response = urlopen(url)


with open('mybaidu.html', 'w') as f:
    f.write(response.read().decode('utf-8'))

print('over!')