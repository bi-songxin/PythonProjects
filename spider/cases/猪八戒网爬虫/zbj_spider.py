

import requests

url = 'https://supei.zbj.com/api/ftServiceDomainService/search'

# 1. 保持纯粹的 Python 数据结构，不需要自己手动去给内部拼 JSON 字符串了
json = {
    'sortType': 7,
    'sign': 'P20220704001',
    'extensions[]': [2, 22],  # json= 模式下，列表能被后端完美识别
    'localCityId': '3510',
    'query': {                # 同样，直接写成字典结构
        "query": "saas",
        "size": 30,
        "start": 0
    }
}

headers = {
    "user-agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36',
    # 你的 Cookie 时效性通常比较短，如果在浏览器里退出了，记得去 F12 里换成最新的
    "cookie": "_uq=8331b49f36274a7f92cd1b092cd6a215; uniqid=d01cjd5kt12jos; _suq=3496f593-f644-45da-8731-98b06f891701; nsid=s%3Aeg7RjwONf4xAjgzCzDzkmZ7mVEv-mZ8S.y8%2F873JUuQ%2Fe%2BztOLxMogaQoCSmCyP7VxoOoUKHnXmg; unionJsonOcpc=eyJvdXRyZWZlcmVyIjoiaHR0cHM6Ly93d3cuZ29vZ2xlLmNvbS8iLCJwbWNvZGUiOiIifQ==; Hm_lvt_a360b5a82a7c884376730fbdb8f73be2=1779784956; HMACCOUNT=7D23520B9639B22D; local_city_path=shenzhen; local_city_name=%E6%B7%B1%E5%9C%B3; local_city_id=3510; pc_no_login_modal_last_show=1; newUserRegister=0; vidSended=1; zmId_1=%7B%22id%22%3A%22YkY5xfUz0ZSDosr4UVeU4cDOUeJyGaOuNXJgeOgi0iu%2B0QT47h0X4WiOI8yD8FxwK6XW%2FnrziZ%2BfUHNBEQzohwXTrwzEdKsBNoZ2rnPr6pCvxsAfzJAEPmeYwtVOKUrEl9DhACzeDtJ341Gcthuqw7R9QKl9rPi0fyBSWgGiKsiFIoR%2BtGGoMcbLy6D01QfrcMtS%2FZhj%2BXKx03I2zxlsFaJCmkDevFdF8NwKMSjRfoMBkxI8sLBn%2Bg%3D%3D%22%2C%22productId%22%3A1%2C%22clickTime%22%3A1779845095315%7D; authtoken=52e22d1deb724e5ca6794221b1be5408LYLg1pcMelF3nHhNzTPmiRYEZ6AS1TM7mutcX84eDiNL5g8pHE3Bf7uhxiPeB9B2; localCityInfo={%22handleInfo%22:{%22cityId%22:3510%2C%22cityName%22:%22%E6%B7%B1%E5%9C%B3%22%2C%22cityEname%22:%22shenzhen%22%2C%22provinceId%22:3492%2C%22provinceName%22:%22%E5%B9%BF%E4%B8%9C%22%2C%22adminCode%22:%22440300%22%2C%22zmnCode%22:%22440300%22%2C%22towns%22:%22%22}%2C%22localInfo%22:{%22cityId%22:3510%2C%22cityName%22:%22%E6%B7%B1%E5%9C%B3%22%2C%22cityEname%22:%22shenzhen%22%2C%22provinceId%22:3492%2C%22provinceName%22:%22%E5%B9%BF%E4%B8%9C%22%2C%22adminCode%22:%22440300%22%2C%22zmnCode%22:%22440300%22}}; _union_uid=7223946; _union_itemid=1734461; fromurl=4a63079ce307e07cf30a9cffab7753a9c209994dd5357da4aae10e405c3585eb; nickname=t_2376_Cskb7h; brandname=t_2376_Cskb7h; userid=30399083; userkey=n812LRBABUg7GA%2F%2FQyEKy68cX%2FVSdADoOlhXOwj1iXgyCNck1zR3mIL1qbz066UzmpN8ZAU3uTlAqPN03PtQ4Pr%2BluQ5nSadxz%2FhfnHEjtPmoihqAXvrYWmmRKUEtsEj7nZx%2B67Z0E618pTkQRvqOSKVG5FuSkWvNHsH0ElSUOwjD%2F36KNmbGI9iRt0mfjZN6nvGJhd33u38%2B72at0dEcVcpyGgdGJ5Mbiy4D31oga5y0W2QMq591KUdzIIc3o7n9xO%2BZQ4KGk1r1cuEmHuJLNCwvfHytneRXzGvM2fbzbBUEZNsbMAbVfwfq3Jfg5QGcKVjCpXWzDGKckhQAIYH61pMXVQn; organizeId=839862; orgMaster=1; osip=1779846350646; oldvid=aef413428089222d62c2a81ef49a02fa; vid=b1b279e304c4972e2fa051c1846361fc; s_s_c=xhA3dh7QsA2lgP8ro4tGR%2Blq2AGYDCVDewtPGKp3OtGeExy%2F2kf2IcD2%2BLVc%2FQysJx8PMCmW6XmCqDifJ%2F4OUQ%3D%3D; Hm_lpvt_a360b5a82a7c884376730fbdb8f73be2=1779848438",
    "referer": 'https://www.zbj.com/fw/?k=saas'
}

# 2. 【核心修改】将 data=data 改为 json=payload
response = requests.post(url, json=json, headers=headers)

# 3. 既然返回的是标准的接口数据，直接用 .json() 打印出完美的字典
try:
    response_data = response.json()
    response_list = response_data['data']['list']

    for item in response_list:
        shopName = item['shopName']
        price = item['price']['format']
        saleCount = item['cumulativeSaleCount']['origin']
        goodCommentCount = item['goodCommentCount']['origin']

        print(shopName, price, saleCount, goodCommentCount)
except Exception as e:
    print("依然未能成功解析为JSON，返回的前1000个字符为：")
    print(response.text[:1000])