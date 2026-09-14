import sys
import requests
import subprocess
import os

"""
ffmpeg比moviepy2的速度更快更好
思路：b站视频是由音频和无声视频合成的

流程：
1.获取音频文件并保存在本地
2.获取无声视频文件并保存在本地
3.若获取失败抛出异常结束程序
4.使用subprocess让python调用ffmpeg工具进行音视频合成
4.保存合成的视频为mp4
5.删除音视频文件
"""
if __name__ == '__main__':

    url_30077 = 'https://cn-fjqz-cm-01-01.bilivideo.com/upgcxcode/91/22/237582291/237582291_x2-1-30077.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&nbs=1&oi=0x2409895b38c010ed79784543dadae44b&mid=435349784&deadline=1787398760&gen=playurlv3&os=bcache&og=ali&trid=00007ca9e7583c4e40d8812b057724fb216u&uipk=5&platform=pc&upsig=ba224581f7a5354a922e2e44f8154460&uparams=e,nbs,oi,mid,deadline,gen,os,og,trid,uipk,platform&cdnid=6476&bvc=vod&nettype=0&bw=1098141&lrs=2&dl=0&f=u_0_0&qn_dyeid=ef6c56aa7e33b87e0095a2f96a896e48&agrr=1&buvid=FB2371B8-3FAF-7848-5F24-C0A9EBA974E226420infoc&build=0&orderid=0,3'
    url_30280 = 'https://cn-fjqz-cm-01-02.bilivideo.com/upgcxcode/91/22/237582291/237582291_nb2-1-30280.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5&oi=0x2409895b38c010ed79784543dadae44b&mid=435349784&deadline=1787398760&platform=pc&nbs=1&trid=00007ca9e7583c4e40d8812b057724fb216u&gen=playurlv3&os=bcache&og=cos&upsig=f3d38ae81d19f9248edd3e449bf92a48&uparams=e,uipk,oi,mid,deadline,platform,nbs,trid,gen,os,og&cdnid=6477&bvc=vod&nettype=0&bw=319342&lrs=2&buvid=FB2371B8-3FAF-7848-5F24-C0A9EBA974E226420infoc&build=0&dl=0&f=u_0_0&qn_dyeid=ef6c56aa7e33b87e0095a2f96a896e48&agrr=1&orderid=0,3'
    # 设置用户代理
    headers_ = {
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36',
        'Referer':'https://www.bilibili.com/video/BV1Sz4y1Z7g9/?from=search&seid=7693898795687978846&vd_source=b62d73a9f4446a598b8107db28d1f07a'
    }
    cookies_ = {
        'cookie':'buvid3=FB2371B8-3FAF-7848-5F24-C0A9EBA974E226420infoc; b_nut=1778592626; _uuid=A19B105610-C22C-B2C7-CDD9-B2AFAC752105A32720infoc; buvid4=8A33F162-CEC1-4C05-F097-91C13378538D67950-025051216-Mq+xgIPzF9qdLf9KFeod8ojQwDrqbMtSUAzCIWTV4LwAR9M1Ldv8b9sFTHsYeQPv; buvid_fp=b2eb019471a45920ba58cb32e2e45c72; theme-tip-show=SHOWED; rpdid=0zbfAGP4av|Hh0XWOMS|2CV|3w1WmOnD; theme-avatar-tip-show=SHOWED; CURRENT_BLACKGAP=0; DedeUserID=435349784; DedeUserID__ckMd5=f8d395aa01d7300f; kfcFrom=detailspage; kfcSource=link; msource=link; deviceFingerprint=a8a4a462c251e9ba737a6ffc00e308c3; home_feed_column=5; browser_resolution=1440-778; CURRENT_QUALITY=80; CURRENT_FNVAL=4048; share_source_origin=COPY; bsource=share_source_copy_link; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3ODc1NzI2MjgsImlhdCI6MTc4NzMxMzM2OCwicGx0IjotMX0.ijqWz6zDH09fhEefIZ0mZK532hPDhp9S2UU0gnskQo8; bili_ticket_expires=1787572568; SESSDATA=6e44c602%2C1802865433%2Ccecc6%2A82CjAzkNnpfmbB-tp0Yrg9ol-CZ1kosHJ-YN3iZiDG4waZe6JsUj8b9bT_Xw1jvuPjK94SVlg3dEZuZ19CaE1vWXEtVlM3eWl6Rlg5WVFBajhXcTJocVI3amplUkRmV3psanRoZS1XUjEwVWFnbmJMWW1PZ0o1emgzcjF5T01FUWtVd3ZUOXJxSXFRIIEC; bili_jct=96de66331fa9f61b07381dfc932b990f; bp_t_offset_435349784=1239202071824039936; sid=7ochs6l9; b_lsid=A6A1AE6B_1A028D6CF08'
    }


    print("开始下载视频...")
    try:
        print('开始下载无声视频文件。。。')
        response_30077 = requests.get(url_30077, headers=headers_, cookies=cookies_,timeout=10)
        response_30077.raise_for_status()
        print('30077请求成功！')

        data_30077 = response_30077.content

        # 保存m4s
        with open('斗罗大陆_30077.m4s', 'wb') as f:
            f.write(data_30077)
            print('纯视频文件下载完毕......')


        print('开始下载音频文件。。。')
        response_30280 = requests.get(url_30280,headers=headers_,cookies=cookies_,timeout=10)
        response_30280.raise_for_status()
        print('30280请求成功！')

        data_30280 = response_30280.content

        with open('斗罗大陆_30280.m4s', 'wb') as f:
            f.write(data_30280)
            print('纯音频文件下载完毕......')

    except requests.RequestException as e:
        print('网络请求失败')
        print(e)

        # 捕捉异常，直接退出,不执行FFmpeg
        sys.exit(1)


# 利用第三方工具ffmpeg 将本地音频和无声视频合成有声视频, 使用subprocess标准库模块让python调用ffmpeg
cmd = [
    'ffmpeg',
    '-i', '斗罗大陆_30077.m4s',
    '-i', '斗罗大陆_30280.m4s',

    '-map', '0:v:0',
    '-map', '1:a:0',

    '-c', 'copy',

    '-shortest',

    '斗罗大陆_ffmpeg.mp4'
]


result = subprocess.run(cmd)

if result.returncode == 0:
    print('视频合成成功！')
else:
    print('视频合成失败！')


# 删除音频、无声视频文件
os.remove('斗罗大陆_30077.m4s')
os.remove('斗罗大陆_30280.m4s')



