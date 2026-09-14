import requests
import csv
import os
from datetime import datetime

#通过datetime获取当前时间并转为毫秒时间戳
def nowadays_to_timestamp():
    return int(datetime.now().timestamp()*1000)

# 13位时间戳转换为年月日
def project_timestamp(financing):
    data_timestamp = financing / 1000
    # 将时间戳转换为datetime对象,获取年月日信息格式化输出
    return datetime.fromtimestamp(data_timestamp).date().strftime('%Y-%m-%d')

# 流式保存到csv文件
def save_items_stream(items):
    FILE_NAME= '36kr_financingList.csv'

    # 判断文件是否存在
    file_exists = os.path.exists(FILE_NAME)

    with open(FILE_NAME, 'a', encoding='utf-8-sig', newline='') as f:
        # 使用 'utf-8-sig' 可以防止 Excel 打开 CSV 时中文乱码
        csvwriter = csv.writer(f)

        # 第一次创建文件时才写表头
        if not file_exists:
           csvwriter.writerow(['融资时间', '项目名称', '项目简介', '所属行业', '融资轮次', '融资金额', '投资方', '详情页网址'])

        for item in items:
            financingDate = project_timestamp(item['financingDate'])
            projectName = item['projectName']
            projectBrief = item['projectBrief']
            industryList = item['industryList']
            financingRoundRemark = item['financingRoundRemark']
            financingMoney = item['financingMoney']
            investor = item['investor']
            projectUrlRoute = item['projectUrlRoute']

            # 写入一条项目信息
            csvwriter.writerow(
                [financingDate, projectName, projectBrief, industryList, financingRoundRemark, financingMoney, investor,projectUrlRoute])

headers = {
    "Accept": "*/*",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "keep-alive",
    "Content-Type": "application/json",
    "Origin": "https://pitchhub.36kr.com",
    "Referer": "https://pitchhub.36kr.com/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36",
    "sec-ch-ua": "\"Chromium\";v=\"148\", \"Google Chrome\";v=\"148\", \"Not/A)Brand\";v=\"99\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\""
}

url = 'https://gateway.36kr.com/api/pms/project/financing/list'
data = f'{{"partner_id":"web","timestamp":{nowadays_to_timestamp()},"partner_version":"1.0.0","param":{{"pageNo":1,"pageSize":20,"siteId":1,"platformId":2}}}}'.encode('utf-8', 'surrogateescape')
response = requests.post(url, headers=headers, data=data)

# 解析并提取页面信息
financingList = response.json()['data']['financingList']


