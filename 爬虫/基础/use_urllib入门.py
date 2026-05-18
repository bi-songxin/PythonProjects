import socket
import urllib.request
import urllib.parse
import urllib.error

# 01 urlopen模块
# response = urllib.request.urlopen('http://www.python.org')
# print(response.read().decode('utf-8'))
# print(type(response))
# print(response.status)
# print(response.getheaders())
# print(response.getheader('server'))

# 02
# 在urlopen中添加data参数
# data = bytes(urllib.parse.urlencode({'name':'germey'}), encoding='utf-8')
# response = urllib.request.urlopen('https://www.httpbin.org/post',data=data)
# print(response.read().decode('utf-8'))

"""
结果:
{
  "args": {}, 
  "data": "", 
  "files": {}, 
  "form": {
    "name": "germey"
  }, 
  "headers": {
    "Accept-Encoding": "identity", 
    "Content-Length": "11", 
    "Content-Type": "application/x-www-form-urlencoded", 
    "Host": "www.httpbin.org", 
    "User-Agent": "Python-urllib/3.12", 
    "X-Amzn-Trace-Id": "Root=1-69ee14b2-17c19a501f8c7c6d4e9362f1"
  }, 
  "json": null, 
  "origin": "111.55.210.65", 
  "url": "https://www.httpbin.org/post"
}
"""

# 03
# timeout参数
# 超过0.1秒没有响应，抛出错误
# response = urllib.request.urlopen("https://www.httpbin.org/get",timeout=0.1)
# print(response.read())


# try except等价写法
# try:
#     response = urllib.request.urlopen("https://www.httpbin.org/get",timeout=0.1)
# except urllib.error.URLError as e:
#     if isinstance(e.reason,socket.timeout):
#         print('Time out')

# 01Request模块
# request = urllib.request.Request('https://python.org')
# response = urllib.request.urlopen(request)
# print(response.read())



#02 Requst的参数
# url = 'https://www.httpbin.org/post'
# headers = {
#     'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT 5.1)',
#     'Host': 'www.httpbin.org',
# }
# dict = {'name': 'germey'}
# data = bytes(urllib.parse.urlencode(dict), encoding='utf-8')
# req = urllib.request.Request(url, data=data, headers=headers, method='POST')
# # 将req中的Request构造成request的参数
# response = urllib.request.urlopen(req)
# print(response.read())


#03 登陆基本身份认证
# https://ssr3.scrape.center/


# from urllib.request import HTTPPasswordMgrWithDefaultRealm, HTTPBasicAuthHandler,build_opener
# from urllib.error import URLError
#
# username = 'admin'
# password = 'admin'
# url = 'https://ssr3.scrape.center/'
#
# p = HTTPPasswordMgrWithDefaultRealm()
# p.add_password(None, url, username, password)
# auth_hander = HTTPBasicAuthHandler(p)
# opener = build_opener(auth_hander)
#
# try:
#     result = opener.open(url)
#     html = result.read().decode('utf-8')
#     print(html)
#
# except URLError as e:
#     print(e.reason)

# 01添加代理
# from urllib.error import URLError
# from urllib.request import ProxyHandler,build_opener
#
# # 代理链接自行填写
# proxy_handler = ProxyHandler({
#     "http": "http://127.0.0.1:8080",
#     "https": "http://127.0.0.1:8080"
# })
# opener = build_opener(proxy_handler)
# try:
#     response = opener.open('https://www.baidu.com')
#     print(response.read().decode('utf-8'))
# except URLError as e:
#     print(e.reason)

# 02 Cookie
# import http.cookiejar,urllib.request
#
# cookie = http.cookiejar.CookieJar()
# handler = urllib.request.HTTPCookieProcessor(cookie)
# opener = urllib.request.build_opener(handler)
# response = opener.open('https://www.baidu.com')
# for item in cookie:
#     print(item.name + '=' + item.value)

"""
BIDUPSID=152BDC8EC47D2FFC6E2B7686EE73DAA0
PSTM=1777284977
BAIDUID=152BDC8EC47D2FFC6E2B7686EE73DAA0:FG=1
BAIDUID_BFESS=152BDC8EC47D2FFC6E2B7686EE73DAA0:FG=1
"""

import urllib.request,http.cookiejar

# 生成Mozilla型Cookie格式
# filename = 'cookie.txt'
# cooike = http.cookiejar.MozillaCookieJar(filename)
# handler = urllib.request.HTTPCookieProcessor(cooike)
# opener = urllib.request.build_opener(handler)
# response = opener.open('http://www.baidu.com/')
# cooike.save(ignore_discard=True, ignore_expires=True)

# 生成LWP型Cookie格式
# filename = 'cookie1.txt'
# cooike = http.cookiejar.LWPCookieJar(filename)
# handler = urllib.request.HTTPCookieProcessor(cooike)
# opener = urllib.request.build_opener(handler)
# response = opener.open('http://www.baidu.com/')
# cooike.save(ignore_discard=True, ignore_expires=True)


#使用cookie请求登陆baidu获取源码
# cookie = http.cookiejar.LWPCookieJar()
# cookie.load(filename='cookie1.txt', ignore_discard=True, ignore_expires=True)
# hander = urllib.request.HTTPCookieProcessor(cookie)
# opener = urllib.request.build_opener(hander)
# response = opener.open('http://www.baidu.com')
# print(response.read())

# 01
