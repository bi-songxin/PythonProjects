import csv
import time
import random
from curl_cffi import requests


headers = {
    "Host": "ynheang.cn",
    "content-type": "application/json",
    "X-Access-Token": "",
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 26_5_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.75(0x18004b50) NetType/WIFI Language/zh_CN",
    "Referer": "https://servicewechat.com/wxafd2b1be21d19665/25/page-frame.html"
}
url = "https://ynheang.cn/farm-machine/newMap/PatrollingField/listAll"
params = {
    "farmerName": "杨双芝"
}
response = requests.get(url, headers=headers, params=params,impersonate="chrome120",timeout=10)

result = response.json()
result_list = result['result']
with open('xuntian.csv','w',encoding='utf-8') as f:
    # 初始化csv
    writer = csv.writer(f)
    #  写标头
    writer.writerow(['id','farmerName','phone','longitude','latitude','qx','xz','cw','address','year','filiale','tobaccoPoint'])
    for index,it in enumerate(result_list,start=1):
        print(f'正在爬取第{index}个列表元素。。。')
        id = it['id']
        farmerName = it['farmerName']
        phone = it['phone']
        longitude = it['longitude']
        latitude = it['latitude']
        qx = it['qx']
        xz = it['xz']
        cw = it['cw']
        address = it['address']
        year = it['year']
        filiale = it['filiale']
        tobaccoPoint = it['tobaccoPoint']

        # 写入csv
        writer.writerow([id,farmerName,phone,longitude,latitude,qx,xz,cw,address,year,filiale,tobaccoPoint])

        print(f'已保存第{index}个列表元素。。。')
        time.sleep(random.uniform(3, 5))

print('over!')

