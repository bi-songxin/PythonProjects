# tls指纹检查网址
# import requests
from curl_cffi import requests
from fake_useragent import UserAgent
url2 = 'https://tls.browserleaks.com/json'
#
ua = UserAgent()
headers = {
    'User-Agent': ua.random,
}
resp = requests.get(url2,headers=headers,impersonate='chrome120')
print(resp.text)