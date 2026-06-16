# 原理：通过第三方的一个机器去发送请求

# 经验之谈：匿名度为透明的更好
import requests

# 站大爷https://www.zdaye.com/free
# 166.111.83.239:7893
proxies = {
    'http':'https://166.111.83.239:7893'
}

headers = {
    'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36'

}
resp = requests.get('https://baidu.com',headers=headers,proxies=proxies)
resp.encoding = 'utf-8'
print(resp.text)
