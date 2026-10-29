import asyncio
import random
import aiohttp
from lxml import etree


"""
相对原版的三处核心改动，v2目的是把协程用满：
1. 一个分页下的所有详情页，改为 asyncio.gather 并发抓取（原版是 for + await 串行）
2. 所有详情页的图片链接汇总后，统一批量并发下载（原版只并发单个详情页内部的图片）
3. 落盘改用 asyncio.to_thread 丢进线程池，避免同步 open/write 阻塞事件循环
"""


# ============ 配置 ============
SAVE_DIR = '/Users/songxinbi/Pictures/beauty_pictures/'
DETAIL_PAGE_CONCURRENCY = 5    # 同时请求的详情页数量上限
DOWNLOAD_CONCURRENCY = 10       # 同时下载的图片数量上限
REQUEST_TIMEOUT = 15

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/155.0.0.0 Safari/537.36",
    "Referer": "https://umeituku.com/",
    "Cookie": "Hm_lvt_f412c1e3a9eb86a70407007197da304b=1792226506; HMACCOUNT=7D23520B9639B22D; Hm_lpvt_f412c1e3a9eb86a70407007197da304b=1792335639"
}


# 提取专题页指定网页的所有详情页链接（纯 CPU）
def parse_content1(resp_text):
    tree = etree.HTML(resp_text)
    li_lists = tree.xpath(
        '//div[@class="list_cont Left_list_cont  Left_list_cont1"]//ul[@class="clearfix"]/li/a/@href'
    )
    return ['https://umeituku.com' + path for path in li_lists]


# 提取详情页所有图片链接（纯 CPU）
def parse_content2(resp_text):
    tree = etree.HTML(resp_text)
    return tree.xpath('//div[@class="scroll-img-cont"]//img/@data-original')


async def sleep_times():
    # 随机休息 3-5s，避免请求过快给服务器造成压力
    await asyncio.sleep(random.uniform(3, 5))


# 抓取网页文本；sem 传入时用信号量限流（用于并发的详情页请求）
async def scrape_html(session, url, sem=None):
    if sem is not None:
        async with sem:
            return await _scrape_html(session, url)
    return await _scrape_html(session, url)


async def _scrape_html(session, url):
    try:
        async with session.get(url, headers=HEADERS) as resp:
            if resp.status == 200:
                return await resp.text()
            return None
    except (aiohttp.ClientError, asyncio.TimeoutError):
        return None


# 落盘（同步函数，交给 asyncio.to_thread 在线程池里执行）
def _save_bytes(path, data):
    with open(path, 'wb') as f:
        f.write(data)


# 下载单张图片（带重试；sem 只锁网络部分，落盘走线程池不占连接名额）
async def aio_download(session, sem, img_url, retries=3, delay=5):
    # 图片服务器只支持 https，http 会被服务端直接断开
    if img_url.startswith('http://'):
        img_url = img_url.replace('http://', 'https://', 1)

    clean_url = img_url.split('?')[0]
    file_name = clean_url.rsplit('/', maxsplit=1)[-1]
    full_save_path = SAVE_DIR + file_name

    timeout = aiohttp.ClientTimeout(total=REQUEST_TIMEOUT)

    for attempt in range(1, retries + 1):
        try:
            async with sem:
                async with session.get(img_url, headers=HEADERS, timeout=timeout) as resp:
                    resp.raise_for_status()
                    img_data = await resp.content.read()

            # 核心改动 3：线程池落盘，不再阻塞事件循环
            await asyncio.to_thread(_save_bytes, full_save_path, img_data)
            print(f"{file_name} is downloaded!")
            return True

        except (aiohttp.ClientError, asyncio.TimeoutError) as net_err:
            print(f"尝试 [ {attempt}/{retries} ] 失败: 网络或请求异常 -> {net_err}")

        except IOError as io_err:
            print(f"文件保存失败 (IOError): {io_err}")
            return None

        except Exception as e:
            print(f"发生未知错误: {e}")

        if attempt < retries:
            await asyncio.sleep(delay)

    print(f'经历了{retries}次尝试后，仍然失败 {img_url}')
    return None


async def main():
    connector = aiohttp.TCPConnector(ssl=False)
    timeout = aiohttp.ClientTimeout(total=REQUEST_TIMEOUT)

    detail_sem = asyncio.Semaphore(DETAIL_PAGE_CONCURRENCY)
    download_sem = asyncio.Semaphore(DOWNLOAD_CONCURRENCY)

    async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:

        index = 1
        # 翻页仍保持串行：下一页是否存在，依赖当前页的解析结果
        while True:
            img_class_url = f'https://umeituku.com/zt/57/meinv/index_{index}.html'
            print(f"\n================ 正在爬取第 {index} 个分页 ================")

            resp_text = await scrape_html(session, img_class_url)
            if not resp_text:
                print(f"第{index}分页网页 {img_class_url} 请求失败，未获取到内容")
                break

            html_lists = parse_content1(resp_text)
            if not html_lists:
                print('all imgs is downloaded!')
                break

            # 核心改动 1：本分页下的所有详情页并发抓取
            detail_tasks = [scrape_html(session, url, detail_sem) for url in html_lists]
            detail_resps = await asyncio.gather(*detail_tasks)

            # 核心改动 2：汇总所有详情页的图片链接
            all_jpg_urls = []
            for url, resp2_text in zip(html_lists, detail_resps):
                if not resp2_text:
                    print(f"详情页 {url} 请求失败，已跳过")
                    continue
                all_jpg_urls.extend(parse_content2(resp2_text))

            if all_jpg_urls:
                print(f'本分页共发现 {len(all_jpg_urls)} 张图片，开始异步下载。。。')
                download_tasks = [aio_download(session, download_sem, u) for u in all_jpg_urls]
                await asyncio.gather(*download_tasks)
            else:
                print('本分页未解析到任何图片')

            await sleep_times()
            index += 1


if __name__ == '__main__':
    asyncio.run(main())
