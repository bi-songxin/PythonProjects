import requests
import re
import logging
import json

# urljoin坐URL链接
from urllib.parse import urljoin

logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(levelname)s - %(message)s')
BASE_URL = 'https://ssr1.scrape.center'
TOTAL_PAGE = 10

# 通用爬取页面方法
def scrape_page(url):
    logging.info('scraping %s...',url)
    try:
        response = requests.get(url)
        if requests.status_codes == 200:
            return response.text
        else:
            logging.error('get invalid staus code %s while scraping %s',response.status_code,url)

    except requests.RequestException as e:
        logging.error('error occurred while scraping %s',url,exc_info=True)


def scrape_index(page):
    index_url = f'{BASE_URL}/page/{page}}'
    return scrape_page(index_url)


