import requests

# 实战1
url = 'https://www.sogou.com/web?query=周杰伦'

headers = {
    'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Mobile Safari/537.36'
}
# 地址栏里面的信息都是get提交
response = requests.get(url,headers=headers) #处理一个小小反爬

print(response.text)

# 关闭resp
response.close()

# 实战2
# url ='https://fanyi.baidu.com/sug'
# s = input('请输入你要发送的单词：')
# data = {
#     'kw':s
# }
#
# # 发送post请求，发送的数据必须放在字典中，通过data参数进行传递
# resp = requests.post(url,data=data)
# print(resp.json())   #将服务器返回的内容直接返回成json格式 => python中叫字典dict
# resp.close()


# 实战3
# url = 'https://movie.douban.com/j/chart/top_list'
# header = {
#     'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Mobile Safari/537.36'
# }

# 如果get请求的的参数比较长，重新封装参数

# param = {
#     'type':24,
#     'interval_id':'100:90',
#     'action':'',
#     'start':0,
#     'limit':20
# }
# resp = requests.get(url,params=param,headers=header)
#
# # print(resp.request.url)
# print(resp.json())
# resp.close()
# print(resp.request.headers)