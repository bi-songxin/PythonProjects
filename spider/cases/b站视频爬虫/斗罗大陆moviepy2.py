import requests
from moviepy import VideoFileClip,AudioFileClip
if __name__ == '__main__':
    # 1.确认url
    url_30077 = 'https://upos-sz-estgoss.bilivideo.com/upgcxcode/91/22/237582291/237582291_x2-1-30077.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&trid=3234616e538245a2ae72a3311bfd987u&mid=435349784&deadline=1787369821&os=estgoss&og=ali&oi=0x2409895b38c010ed79784543dadae44b&nbs=1&uipk=5&platform=pc&gen=playurlv3&upsig=b519850546746417c9bb67a80a405a44&uparams=e,trid,mid,deadline,os,og,oi,nbs,uipk,platform,gen&bvc=vod&nettype=0&bw=1098141&lrs=-1&build=0&dl=0&f=u_0_0&qn_dyeid=a82a4aee4449cd2a000c11626a88fd3d&agrr=1&buvid=FB2371B8-3FAF-7848-5F24-C0A9EBA974E226420infoc&orderid=0,3'
    url_30280 = 'https://upos-sz-estgcos.bilivideo.com/upgcxcode/91/22/237582291/237582291_nb2-1-30280.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&deadline=1787369821&uipk=5&platform=pc&gen=playurlv3&oi=0x2409895b38c010ed79784543dadae44b&nbs=1&os=estgcos&og=cos&trid=3234616e538245a2ae72a3311bfd987u&mid=435349784&upsig=8caf802bd0c107099f04932ff759d1c4&uparams=e,deadline,uipk,platform,gen,oi,nbs,os,og,trid,mid&bvc=vod&nettype=0&bw=319342&lrs=-1&buvid=FB2371B8-3FAF-7848-5F24-C0A9EBA974E226420infoc&build=0&dl=0&f=u_0_0&qn_dyeid=a82a4aee4449cd2a000c11626a88fd3d&agrr=1&orderid=0,3'
    # 设置用户代理
    headers_ = {
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36',
        'Referer':'https://www.bilibili.com/video/BV1Sz4y1Z7g9/?from=search&seid=7693898795687978846&vd_source=b62d73a9f4446a598b8107db28d1f07a'
    }
    cookies_ = {
        'cookie':'buvid3=FB2371B8-3FAF-7848-5F24-C0A9EBA974E226420infoc; b_nut=1778592626; _uuid=A19B105610-C22C-B2C7-CDD9-B2AFAC752105A32720infoc; buvid4=8A33F162-CEC1-4C05-F097-91C13378538D67950-025051216-Mq+xgIPzF9qdLf9KFeod8ojQwDrqbMtSUAzCIWTV4LwAR9M1Ldv8b9sFTHsYeQPv; buvid_fp=b2eb019471a45920ba58cb32e2e45c72; theme-tip-show=SHOWED; rpdid=0zbfAGP4av|Hh0XWOMS|2CV|3w1WmOnD; theme-avatar-tip-show=SHOWED; CURRENT_BLACKGAP=0; DedeUserID=435349784; DedeUserID__ckMd5=f8d395aa01d7300f; kfcFrom=detailspage; kfcSource=link; msource=link; deviceFingerprint=a8a4a462c251e9ba737a6ffc00e308c3; home_feed_column=5; browser_resolution=1440-778; CURRENT_QUALITY=80; CURRENT_FNVAL=4048; share_source_origin=COPY; bsource=share_source_copy_link; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3ODc1NzI2MjgsImlhdCI6MTc4NzMxMzM2OCwicGx0IjotMX0.ijqWz6zDH09fhEefIZ0mZK532hPDhp9S2UU0gnskQo8; bili_ticket_expires=1787572568; SESSDATA=6e44c602%2C1802865433%2Ccecc6%2A82CjAzkNnpfmbB-tp0Yrg9ol-CZ1kosHJ-YN3iZiDG4waZe6JsUj8b9bT_Xw1jvuPjK94SVlg3dEZuZ19CaE1vWXEtVlM3eWl6Rlg5WVFBajhXcTJocVI3amplUkRmV3psanRoZS1XUjEwVWFnbmJMWW1PZ0o1emgzcjF5T01FUWtVd3ZUOXJxSXFRIIEC; bili_jct=96de66331fa9f61b07381dfc932b990f; sid=q4pw33fw; bp_t_offset_435349784=1239202071824039936; b_lsid=B1B910E3_1A0271D3B72'
    }

    # 2.发送请求得到响应
    response_30077 = requests.get(url_30077,headers=headers_,cookies=cookies_)
    response_30280 = requests.get(url_30280,headers=headers_,cookies=cookies_)

    data_30077 = response_30077.content
    data_30280 = response_30280.content

    # 保存
    with open('斗罗大陆_30077.mp4', 'wb') as f:
        f.write(data_30077)

    with open('斗罗大陆_30280.mp3', 'wb') as f:
        f.write(data_30280)

    """
    在拥有了一个纯视频文件,跟一个纯音频文件的情况下......
    利用第三方库moviepy合成():速度很慢  
    """

    # 选择一个已经拥有的纯视频文件
    video_obj = VideoFileClip('斗罗大陆_30077.mp4')

    # 选一个对应已拥有的纯音频文件
    audio_obj = AudioFileClip('斗罗大陆_30280.mp3')

    # 往视频对象里面添加音频
    movie_ = video_obj.with_audio(audio_obj)

    # 保存
    movie_.write_videofile('斗罗大陆_.mp4')

