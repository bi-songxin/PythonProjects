import requests
import re
import logging
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json
from os import makedirs
from os.path import exists
import time
import pandas as pd
import matplotlib.pyplot as plt

# 解决绘图时中文显示乱码问题
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
BASE_URL = 'https://ssr1.scrape.center'
TOTAL_PAGE = 10


# 通用爬取页面方法（带重试机制）
def scrape_page(url, retries=3):
    logging.info('scraping %s...', url)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    for i in range(retries):
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                return response.text
            else:
                logging.error('get invalid status code %s while scraping %s', response.status_code, url)
                return None
        except (requests.RequestException, Exception) as e:
            logging.warning('连接失败，正在进行第 %d 次重试... 错误原因: %s', i + 1, e)
            time.sleep(1)  # 稍微等待一下再重试

    logging.error('Failed to scrape %s after %d retries', url, retries)
    return None


# 抓取列表页
def scrape_index(page):
    index_url = f'{BASE_URL}/page/{page}'
    return scrape_page(index_url)


# 获取列表页每个url
def parse_index(html):
    soup = BeautifulSoup(html, 'lxml')
    items = soup.find_all('a', class_='name')
    if not items:
        return []
    for item in items:
        href = item.get('href')
        detail_url = urljoin(BASE_URL, href)
        logging.info('get detail url: %s', detail_url)
        yield detail_url


# 抓取详情页
def scrape_detail(url):
    return scrape_page(url)


# 解析详情页
def parse_detail(html):
    soup = BeautifulSoup(html, 'lxml')
    cover = soup.find('img', class_='cover').get('src') if soup.find('img', class_='cover') else None

    name_node = soup.find('h2', class_='m-b-sm')
    name = str(name_node.string) if name_node and name_node.string else None

    categories = []
    cat_spans = soup.select('.categories span')
    if cat_spans:
        for i in cat_spans:
            if i.string:
                categories.append(str(i.string))
    categories_str = ",".join(categories) if categories else None

    publish_node = soup.find('span', string=re.compile(r'上映', re.S))
    publish_at = str(publish_node.string) if publish_node and publish_node.string else None

    score_node = soup.find('p', class_='score m-t-md m-b-n-sm')
    score = float(score_node.string) if score_node and score_node.string else None

    drama_p = soup.select('.drama p')
    drama = str(drama_p[0].string).strip() if drama_p and drama_p[0].string else None

    return {
        'cover': cover,
        'name': name,
        'categories': categories_str,
        'publish_at': publish_at,
        'score': score,
        'drama': drama
    }


# 数据分析与可视化函数
def analyze_and_visualize(df):
    print("\n" + "=" * 10 + " 数据分析结果 " + "=" * 10)

    # 1. 提取年份 (从 "2013-01-23 上映" 中提取前4位数字)
    df['year'] = df['publish_at'].str.extract(r'(\d{4})')

    # 计算各年份电影数量
    year_counts = df['year'].value_counts().sort_index()
    print("\n[各年份电影数量]:")
    print(year_counts.to_string())

    # 2. 分析 score 字段
    max_score = df['score'].max()
    min_score = df['score'].min()
    mean_score = df['score'].mean()
    print(f"\n[电影评分分析]:\n最大值: {max_score}\n最小值: {min_score}\n平均值: {mean_score:.2f}")
    print("=" * 32 + "\n")

    # 3. 使用 Matplotlib 绘制饼图
    plt.figure(figsize=(8, 8))
    plt.pie(year_counts, labels=year_counts.index, autopct='%1.1f%%', startangle=140, counterclock=False)
    plt.title('各年份电影数量占比饼图', fontsize=16)
    plt.axis('equal')
    plt.show()


# 主运行逻辑
if __name__ == '__main__':
    all_data = []  # 用于存储所有爬取到的电影数据

    # 单进程循环顺序爬取
    for page in range(1, TOTAL_PAGE + 1):
        logging.info(f'--- 开始爬取第 {page} 页 ---')
        index_html = scrape_index(page)
        if not index_html:
            continue

        detail_urls = parse_index(index_html)
        for detail_url in detail_urls:
            detail_html = scrape_detail(detail_url)
            if detail_html:
                data = parse_detail(detail_html)
                logging.info(f'成功解析电影: {data.get("name")}')
                all_data.append(data)

            # 顺序爬取时，稍微温和地停顿 0.2 秒，防止对服务器造成高频轰炸
            time.sleep(0.2)

    # 爬取完成后，统一使用 Pandas 处理
    if all_data:
        df = pd.DataFrame(all_data)

        # 创建保存目录
        RESULTS_DIR = 'results'
        if not exists(RESULTS_DIR):
            makedirs(RESULTS_DIR)

        csv_path = f'{RESULTS_DIR}/movies.csv'
        # index=False 表示不保存行索引，utf-8-sig 确保 Excel 打开不乱码
        df.to_csv(csv_path, index=False, encoding='utf-8-sig')
        logging.info(f'所有数据已成功保存至 {csv_path}')

        # 执行数据统计与可视化饼图
        analyze_and_visualize(df)
    else:
        logging.error("未爬取到任何数据，请检查网络或目标网站状态！")