import requests

url = 'https://b-s-x.com'

proxies = {
    'https':'59.66.133.42:6518'
}
resp = requests.get(url,proxies=proxies)
resp.encoding = 'utf-8'
print(resp.text)