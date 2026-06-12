# 梨视频 https://www.pearvideo.com/
"""
目的：
抓取目标页的视频
1.获取目标页的的conId
2.目标页抓包获取到视频的接口，提取出视频链接
3.替换视频链接
4.下载到本地

"""

import requests

url = 'https://www.pearvideo.com/video_1806353'
conId = url.split('_')[1]
# print(conId)

headers = {
    'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36',
    'cookie':'PEAR_UUID=a335b1c5-5e6c-4b55-8132-c5f0cb066e69; Hm_lvt_9707bc8d5f6bba210e7218b8496f076a=1779893001; HMACCOUNT=7D23520B9639B22D; _c_WBKFRo=IIcPSGl8i7lHiqEi8ro60dsl4YjGcnf0F3JIsy2Y; _nb_ioWEgULi=; p_h5_u=D65A1894-D2CD-4DE2-99E0-7184024744F2; JSESSIONID=8ED8D78D194050C2BBB05A43F48AAC06; Hm_lpvt_9707bc8d5f6bba210e7218b8496f076a=1779952646; tgw_l7_route=92611af627df0b9b1cd8a442f9668c80',
    'referer':'https://www.pearvideo.com/video_1806353'

}
mp4_url = f'https://www.pearvideo.com/videoStatus.jsp?contId={conId}'

resp = requests.get(mp4_url,headers=headers)
# print(resp.json())
systemTime = resp.json()["systemTime"]
srcUrl = resp.json()["videoInfo"]["videos"]["srcUrl"]
new_srcUrl = srcUrl.replace(systemTime,f'cont-{conId}')
# print(new_srcUrl)


# 下载到本地
with open('a.mp4','wb') as f:
    f.write(requests.get(new_srcUrl).content)