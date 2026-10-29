# requests.get()同步代码 ——> 异步操作aiohttp

import asyncio
import aiohttp

urls = [
    'https://img.7476.com/d/file/bigpic/2018-11-24/17/175328297.jpg',
    'https://img.7476.com/d/file/bigpic/2023-09-20/23/2306041734.jpg',
    'https://img.7476.com/d/file/bigpic/2023-08-03/21/2112022202.jpg'
]


async def iodownload(url):
    # 1.发送请求 2.得到图片内容 3.保存到文件
    # s = aiohttp.ClientSession() <==>requests.session

    name = url.rsplit('/', 1)[1]
    async with aiohttp.ClientSession() as session:  # <==>requests.session
        async with session.get(url) as resp:  # <==>requests.get
            # resp.content.read()  #等价于resp.content
            # resp.text()  #等价于resp.text
            # resp.json()  ##等价于resp.json()

            with open(name, 'wb') as f:
                f.write(await resp.content.read())  # 读取内容是异步的，需要await挂起   #<==>requests.content
    print("over!")


async def main():
    tasks = []
    for url in urls:
        task = asyncio.create_task(iodownload(url))
        tasks.append((task))

    await asyncio.wait(tasks)


if __name__ == '__main__':
    asyncio.run(main())

"""
1.async异步函数要接受返回的成功数据需要用await挂载
2.await 跟着的业务代码 （它们必须依赖 await 返回的结果才能继续）
3.当进行I/O操作时，cpu是空闲的，如果要充分利用cpu的性能需要使用异步，具体时使用协程coroutine方式
"""
