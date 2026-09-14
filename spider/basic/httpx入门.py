# 详细介绍：https://www.python-httpx.org/

# httpx和requests有很多相似之处
import httpx
import asyncio
from fake_useragent import UserAgent


# httpx默认不开启http/2.0，默认使用http/1.1

# 开启http/2.0
# with httpx.Client(http2=True) as client:
#     response = client.get('https://spa16.scrape.center/')
#     print(response.text) #使用http/1.1会报错：httpx.RemoteProtocolError: Server disconnected without sending a response.
#     print(response.http_version) #HTTP/2



# get方法
# headers = {
#     'User-Agent':f'{UserAgent().random}',
# }
# response = httpx.get('https://httpbin.org/get', headers=headers)
# print(response.status_code)
# print(response.headers)
# print(response.text)
# print(response.http_version)


# post、put、delete、patch方法(和request用法一样)

# r2 = httpx.post('https://www.httpbin.org/post',data={'name':'germey'})
# print(r2.text)
#
# r3 = httpx.put('https://www.httpbin.org/put')
# print(r3.text)
#
# r4 = httpx.delete('https://www.httpbin.org/delete')
# print(r4.text)
#
# r5 = httpx.patch('https://www.httpbin.org/patch')
# print(r5.text)

# response属性和方法
"""
status_code
text
content
headers
json
"""


# httpx特有-Client对象
# Client对象，可以和requests中的Session对象类比进行学习
# with httpx.Client() as client:
#     resp = client.get('https://www.httpbin.org/get')
#     print(resp.text)
#
# # 等价下面式子
# print('-'*30)
#
# client = httpx.Client()
#
# try:
#     resp = client.get('https://www.httpbin.org/get')
#     print(resp.text)
# finally:
#     client.close() #显式调用close方法关闭Client对象
#

# 给client对象传参headers
# url = 'https://httpbin.org/headers'
# headers = {'User-Agent': UserAgent().random}
# with httpx.Client(headers=headers) as client:
#     r = client.get(url)
#     print(r.json()['headers']['User-Agent'])


# 异步请求
async def fetch(url):
    async with httpx.AsyncClient() as client:
        response1 = await client.get(url)
        print(response1.text)

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(fetch('https://www.httpbin.org/get'))