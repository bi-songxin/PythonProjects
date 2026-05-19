import requests
import re
import logging
from bs4 import BeautifulSoup
# urljoin坐URL链接
from urllib.parse import urljoin
import json
from os import makedirs
from os.path import exists
import multiprocessing

logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(levelname)s - %(message)s')
BASE_URL = 'https://ssr1.scrape.center'
TOTAL_PAGE = 10

# 通用爬取页面方法
def scrape_page(url):
    logging.info('scraping %s...',url)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            logging.error('get invalid staus code %s while scraping %s',response.status_code,url)

    except requests.RequestException as e:
        logging.error('error occurred while scraping %s',url,exc_info=True)


# 抓取列表页
def scrape_index(page):
    index_url = f'{BASE_URL}/page/{page}'
    return scrape_page(index_url)

# 获取列表页每个url
def parse_index(html):
    soup = BeautifulSoup(html,'lxml')
    items = soup.find_all('a',class_='name')
    if not items:
        return []
    for item in items:
        href = item.get('href')
        detail_url = urljoin(BASE_URL,href)
        logging.info('get detail url: %s',detail_url)
        yield detail_url

# 抓取详情页
def scrape_detail(url):
    return scrape_page(url)

# 解析详情页
def parse_detail(html):
    soup = BeautifulSoup(html,'lxml')
    cover = soup.find('img',class_='cover').get('src') if soup.find('img',class_='cover').get('src') else None
    name = soup.find('h2',class_='m-b-sm').string if soup.find('h2',class_='m-b-sm').string else None
    categories = []
    for i in soup.select('.categories span') if soup.select('.categories span') else None:
        categories.append(i.string)
    publish_at = soup.find('span',string=re.compile(r'上映',re.S)).string if soup.find('span',string=re.compile(r'上映',re.S)) else None
    score = float(soup.find('p',class_='score m-t-md m-b-n-sm').string) if soup.find('p',class_='score m-t-md m-b-n-sm') else None
    drama = soup.select('.drama p')[0].string.strip() if soup.select('.drama p') else None

    return {
        'cover': cover,
        'name': name,
        'categories': categories,
        'publish_at': publish_at,
        'score': score,
        'drama': drama
    }

# 保存数据
RESULTS_DIR = 'results'
exists(RESULTS_DIR) or makedirs(RESULTS_DIR)

def save_data(data):
    name = data.get('name')
    data_path = f'{RESULTS_DIR}/{name}.json'
    json.dump(data, open(data_path,'w',encoding='utf-8'), ensure_ascii=False,indent=2)

# 主程序
def main(page):
    index_html = scrape_index(page)
    detail_urls = parse_index(index_html)
    for detail_url in detail_urls:
        detail_html = scrape_detail(detail_url)
        data = parse_detail(detail_html)
        logging.info(f'get detail data{data}')
        logging.info(f'save data to json file')
        save_data(data)
        logging.info(f'data saved successfully!!!!')


if __name__ == '__main__':
    pool = multiprocessing.Pool()
    pages = range(1,TOTAL_PAGE+1)
    pool.map(main, pages)
    pool.close()
    pool.join()


"""
总结：
BeautifulSoup
单个关键词提取：
如果要找的标签没有属性，上级标签也没有：使用select函数，找到更上层的父标签，传入css选择器
如果要找的标签没有属性，上级标签有：使用select函数，传入css选择器
如果要找的标签有属性：使用find函数，传入标签名和属性名和值

多个关键词中全部提取：（前提是标签、属性名和值相同）
如果要找的标签们没有属性，上级标签们也没有：新建一个空列表，使用select函数，找到更上层的父标签，传入css选择器，依次放进空列表中
如果要找的标签们没有属性，上级标签们有：新建一个空列表，使用select函数，找到更上层的父标签，传入css选择器，依次放进空列表中
如果要找的标签们有属性，上级标签们有：新建一个空列表，使用select函数或者find_all函数，传入css选择器或传入标签名和属性名和值，依次放进空列表中

多个关键词中部分提取：（前提是标签、属性名和值相同）
如果要找的标签们没有属性，上级标签们也没有：使用select函数，找到更上层的父标签，传入css选择器，使用[]选择对应关键词
如果要找的标签们没有属性，上级标签们有：使用select函数，找到更上层的父标签，传入css选择器，使用[]选择对应关键词
如果要找的标签们有属性，上级标签们有：使用select函数或者find_all函数，传入css选择器或传入标签名和属性名和值，使用[]选择对应关键词
"""