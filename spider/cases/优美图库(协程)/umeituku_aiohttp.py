import asyncio
import aiohttp
import random
from lxml import etree


"""
实现思路：
1.指定url专题提取第n个分页下的所有详情页url_lists
2.循环进入url_lists中的每个详情页
3.提取详情页所在的所有图片img_url_lists
4.请求下载保存img_url_lists中的img_url
5.往复上述1-4步骤
"""


# 提取专题页指定网页（纯CPU）
def parse_content1(resp_text):
    # xpath解析
    tree = etree.HTML(resp_text)
    li_lists = tree.xpath('//div[@class="list_cont Left_list_cont  Left_list_cont1"]//ul[@class="clearfix"]/li/a/@href')
    # print(li_lists)
    domain = 'https://umeituku.com'
    domain_url_list = []
    for path in li_lists:
        url = domain + path
        domain_url_list.append(url)

    return domain_url_list

# 提取详情页图片
def parse_content2(resp_text):
    tree = etree.HTML(resp_text)
    jpg_lists = tree.xpath('//div[@class="scroll-img-cont"]//img/@data-original')

    return jpg_lists

async def sleep_times():
    # 随机休息5-8s，避免请求过快给服务器造成压力
    time_sleep = random.uniform(3, 5)
    await asyncio.sleep(time_sleep)

# 异步抓取网页内容（session 由外部传入，复用连接池）
async def scrape_html(session, url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/155.0.0.0 Safari/537.36",
        "Referer": "https://umeituku.com/",
        "Cookie":"Hm_lvt_f412c1e3a9eb86a70407007197da304b=1792226506; HMACCOUNT=7D23520B9639B22D; Hm_lpvt_f412c1e3a9eb86a70407007197da304b=1792335639"
    }
    async with session.get(url, headers=headers) as resp:
        if resp.status == 200:
            resp_text = await resp.text()
            return resp_text
        else:
            return None


# 下载图片（session 由外部传入，复用连接池）
async def aio_download(session, img_url, retries=3, delay=5):

    # 图片服务器 img.7476.com 只支持 https，http 会被服务端直接断开(Server disconnected)
    if img_url.startswith('http://'):
        img_url = img_url.replace('http://', 'https://', 1)

    clean_url = img_url.split('?')[0]
    folder_path = '/Users/songxinbi/Pictures/beauty_pictures/'
    file_name = clean_url.rsplit('/', maxsplit=1)[1]
    full_save_path = folder_path + file_name

    if not full_save_path:
        print(f"无法从 URL 解析出合法文件名: {img_url}")
        return None

    # 设置超时时间，防止某个图片锁死，导致整个程序卡死
    timeout = aiohttp.ClientTimeout(total=15)

    for attempt in range(1, retries+1):
        try:
            # 核心
            headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/155.0.0.0 Safari/537.36",
                "Referer": "https://umeituku.com/",
                "Cookie": "Hm_lvt_f412c1e3a9eb86a70407007197da304b=1792226506; HMACCOUNT=7D23520B9639B22D; Hm_lpvt_f412c1e3a9eb86a70407007197da304b=1792335639"
            }
            async with session.get(img_url, headers=headers, timeout=timeout) as resp:

                # 检查 HTTP 状态码（如果是 404 或 500，直接抛出异常触发重试或报错）
                resp.raise_for_status()

                # 读二进制数据
                img_data = await resp.content.read()

                # 保存图片
                with open(full_save_path, 'wb') as f:
                    f.write(img_data)
            print(f"{file_name} is downloaded!")

            return True # 下载成功，提前退出函数

        except (aiohttp.ClientError, asyncio.TimeoutError) as net_err:
            # 捕获网络错误、超时、404/500 等客户端异常
            print(f"尝试 [ {attempt}/{retries} ] 失败: 网络或请求异常 -> {net_err}")

        except IOError as io_err:
            # 捕获本地文件读写错误（通常不需要重试，直接报错）
            print(f"文件保存失败 (IOError): {io_err}")

        except Exception as e:
            # 捕获其他未知异常
            print(f"发生未知错误: {e}")


        if attempt < retries:
            await asyncio.sleep(delay)
    print(f'经历了{retries}次尝试后，仍然失败{img_url}')
    return None


async def main():
    # 全局只建一个连接器 + 会话，让 aiohttp 走连接池(keep-alive)，
    # 避免每个请求都新建/销毁 TCP 连接，从而触发服务端 disconnect
    connector = aiohttp.TCPConnector(ssl=False)
    timeout = aiohttp.ClientTimeout(total=15)

    async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:

        # 创建一个信号量控制器，限制同时下载的图片数量最大为 5
        # sem = asyncio.Semaphore(5)

        # # 定义一个内部临时包装函数，用来给 aio_download 上锁
        # async def sem_download(url):
        #     async with sem:
        #         # 只有拿到许可证的图片，才会去调用aio_download函数
        #         return await aio_download(session, url)

        index = 1
        # 循环当前专区所有分页
        while True:
            img_class_urls = f'https://umeituku.com/zt/57/meinv/index_{index}.html'
            print(f"\n================ 正在爬取第 {index} 个分页 ================")

            # 当前分页网页内容
            resp_text = await scrape_html(session, img_class_urls)

            if resp_text:
                # print(resp_text)
                html_lists = parse_content1(resp_text)

                # 分页中的每个详情页如果不存在，直接退出
                if not html_lists:
                    print('all imgs is downloaded!')
                    break

                #循环当前分页下的各个详情页
                index2 = 1
                for img_little_class_url in html_lists:
                    print(f"\n================ 正在爬取当前第{index}分页/第 {index2} 个详情页 ================")
                    resp2_text = await scrape_html(session, img_little_class_url)

                    if resp2_text:
                        jpg_lists = parse_content2(resp2_text)

                        if jpg_lists:
                            print(f'发现有{len(jpg_lists)}张图片，开始异步下载。。。')

                            # 核心：协程爬取图片
                            # 保存详情页所有个图片
                            tasks = [aio_download(session,jpg_list) for jpg_list in jpg_lists]

                            await asyncio.gather(*tasks)
                            # 随机休眠
                            await sleep_times()
                        else:
                            print('图片列表为空，请求失败，未获取到内容')
                            continue


                    else:
                        print(f"详情页{img_little_class_url}请求失败，未获取到内容")
                        continue

                    await sleep_times()
                    index2 += 1
            else:
                print(f"第{index}分页网页{img_class_urls}请求失败，未获取到内容")
                break

            await sleep_times()

            index += 1

if __name__ == '__main__':
    asyncio.run(main())
