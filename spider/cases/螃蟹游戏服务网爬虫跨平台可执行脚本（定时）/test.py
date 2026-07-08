import os
import sqlite3
import requests
import json
import datetime




# 1. 初始化本地数据库（去重与监控的核心）
def init_db():
    conn = sqlite3.connect('2026_6_18_data.db')
    print('数据库连接成功！')
    cursor = conn.cursor()
    # 创建商品表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id TEXT PRIMARY KEY,
            title TEXT,
            price REAL,
            status TEXT, -- 'active' 在售, 'sold' 已卖出
            updated_at TEXT
        )
    ''')
    print('数据表创建成功！')
    conn.commit()
    return conn


# 2. 爬取一页数据
def fetch_page(url,headers,data,cookies):
    try:
        response = requests.post(url, headers=headers, json=data, cookies= cookies,timeout=10)
        if response.status_code == 200:
            print('成功请求到数据！')
            return response.json()
    except Exception as e:
        print(f"抓取失败: {e}")
    return None


# 3. 跑“点收藏”的接口（需求3）
def collect_product(product_id):
    print(f"正在自动收藏商品: {product_id}")
    # 这里写你抓到的点收藏接口的 requests.post(...)
    pass


# 4. 核心处理逻辑
def main():
    page = 1

    headers = {
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Origin": "https://www.pxb7.com",
        "Pragma": "no-cache",
        "Referer": "https://www.pxb7.com/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36",
        "accept": "application/json",
        "client_type": "0",
        "content-type": "application/json",
        "device_id": "6f99ed7e-40c1-46bb-b68d-bdd8eaf55aac",
        "gio_device": "2866e9ca-c7d4-4acb-87fa-432d21c895b5",
        "os_type": "6",
        "px-authorization-merchant;": "",
        "px-authorization-user;": "",
        "sec-ch-ua": "\"Chromium\";v=\"148\", \"Google Chrome\";v=\"148\", \"Not/A)Brand\";v=\"99\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"macOS\"",
        "user_id;": ""
    }
    cookies = {
        "JSESSIONID": "788FA8C8B55A34F9E30588C7BE3B1F26",
        "deviceId": "6f99ed7e-40c1-46bb-b68d-bdd8eaf55aac",
        "_c_WBKFRo": "tP60MMkscaiC4Hf5ltHjo37pTcbG1ptLKUsVCt6J",
        "_nb_ioWEgULi": "",
        "Hm_lvt_6d8ffc7e04e74b3866a454a4477796ce": "1781658344",
        "HMACCOUNT": "7D23520B9639B22D",
        "a6990010a0b40f79_gdp_session_id": "2f4b0fd6-cf22-41f9-bc53-6c13aa13921a",
        "gdp_user_id": "gioenc-3977d8ba%2Cb6e5%2C5abc%2C96ga%2C523e30b984c4",
        "a6990010a0b40f79_gdp_session_id_sent": "2f4b0fd6-cf22-41f9-bc53-6c13aa13921a",
        "aliyungf_tc": "f7ef18f968b3737738b904e24fa5cd14722f021912e4f3fd6247883aba870421",
        "acw_tc": "0a15e15e17816583455383174e65fcc20f9f7d7594f19178445013d7e235cd",
        "Hm_lpvt_6d8ffc7e04e74b3866a454a4477796ce": "1781658734",
        "a6990010a0b40f79_gdp_sequence_ids": "{%22globalKey%22:82}",
        "ssxmod_itna": "1-Gq_xuDci0=GQe0Ki7eitGRDmOYG2RiOD0DBP01HD_xQHK08D6nDB_2Q2iKoTxeRGxDn0EroedYjqDseii4GzDiqKGhDBeo7x5W3R4r3W0j2_3ooeQAYpae6z2Gx3HDsQxpLrLI6kIEsHKz3cDidibqmDiTbnxDoxGkDiyPD09hmDiiFx0rD0eDPxDYDG4mTboDjefIz38_HeEeWK3Db12wOCxDR6dDSefEat36Dm40S4i8LQ3DWpA2DDPpDWy3hUEUbDDCrhC5Fqh8f4iaNU_9HnxRD7KR8e3DF6M3Yq0kNbjbkFsZDCKpHD7NfquGWxwbeMixOixhepGimDxQhqqA4f2DhwexgxYhDmow=YYYAxmODND4MBiY3opD8MievooPrwrGeMusDWGemeq75KiiLoAm0DtD4Gx4qAQXjhlY4YA=KDwxE4rj4aYCt7mtliW15dD4q44d0Dq7drA4Qo_EjeWPKjnh4D",
        "ssxmod_itna2": "1-Gq_xuDci0=GQe0Ki7eitGRDmOYG2RiOD0DBP01HD_xQHK08D6nDB_2Q2iKoTxeRGxDn0EroedYi4DWmQj7rTY=Dj4hGiFQ=YxriC4GNOWo71fxYhqtPKO4I5nYQyEW=7YCPuIXqq_zhhrp8DRFaIPvYSahY_lp857Fis=ia=mH4sg5k_7GOelPac1vIUP24t_08mPOIE4qpKeyiLp3Gi9yzscOf=QD8uriXz/azQmL80zvk1_O_ddEu5KFvUx2vRnO1=4q4g6EFHk2803oQzuQsW2KmKWhUTpBO2rGLqfQc_WMEUbFFKj6SiH7ii_GhDhriRbl3HqWTlBq0Qqxpqu7cLAwPEbli0HCKMmWvFv9/449aUt_hDWjApnFP4Eqt/_BeBqIbRIn8A4btaqWyCDn437qlTjCepFHUbWAji8f_V_qkRRxAe4B7xoqu80EQ0rvPIFn8GGZmOit8PY3YaHNEqimEIjWUKixHD8o9CPPocmcbS8RKqmOvfDuB74WczVvCAka4_880NfiP4y7AWqNcLAeHWw44W9GP5vwbNGQkiYc3L0h87T6KaF7umO7EGL1bquF784cGG3HXfYR44SOwU8aB0HWBWGiwnAOtcaqK17n6uE=q45ayjjbrrA8U_ni7FBz9qb_30WF0D/CfwDLbY6_HwBitXehEbyFQh3MWfi1C5kAQrXKIp=Oyihre54=KQq8CrN08OoHxo7zFibj3vrfAsYTwlTap=xx/2ieQs4PUh/4r1KRWl78/bfADuuRm_/iaeTur4roqDbWzqcEj3nA=1w1Bob505OWxcAwabRmki8p_PGOqDiRPpbogrkxFGmahYepVu_6q5DqiCxTHGmaoOWawIYnFmxeBtEOYKxVR4mDSAFhz9h6AaLgDQDb_EAwIYk_m5oZCFwFGFepGBr4piomOMieSqd_1YFai_bExutnDofDD"
    }
    data = {
        "query": "",
        "gameId": "10161",
        "pageIndex": page,
        "pageSize": 16,
        "bizProd": 1,
        "type": "1",
        "posType": 1,
        "filterDTOList": [
            {
                "attrId": "101611",
                "attrType": 1,
                "attrValList": [
                    "101611"
                ],
                "optionType": 1
            },
            {
                "attrId": "1016118",
                "attrType": 1,
                "attrValList": [
                    "10161171"
                ],
                "optionType": 1
            },
            {
                "attrId": "1016120",
                "attrType": 1,
                "attrValList": [
                    "10161232"
                ],
                "optionType": 1
            },
            {
                "attrId": "1016123",
                "attrType": 1,
                "attrValList": [
                    "10161230"
                ],
                "optionType": 1
            },
            {
                "attrId": "price",
                "attrType": 3,
                "attrValList": [
                    1000,
                    8000
                ]
            },
            {
                "attrId": "10161512",
                "attrType": 2,
                "attrValList": [
                    70,
                    -1
                ]
            }
        ],
        "sortAttrId": "",
        "mineFav": False,
        "sortType": 2,
        "combineFilterList": [],
        "pageToken": "7qKx8DEMIJxPtHrCc1mEgQ"
    }


    conn = init_db()
    cursor = conn.cursor()

    # 记录本次抓取到的所有商品ID，用于比对“谁卖掉了”
    current_active_ids = []

    token = "7qKx8DEMIJxPtHrCc1mEgQ"  # 初始token，注意是否会过期

    print(f"--- 开始每日定时任务: {datetime.datetime.now()} ---")

    # 翻页抓取
    while True:
        url = "https://api-pc.pxb7.com/api/search/product/v2/selectSearchPageList"
        res_json = fetch_page(url,headers,data,cookies)

        if 'list' not in res_json:
            print('没有请求到数据！')
            break

        products = res_json.get('data', {}).get('list', [])

        for prod in products:
            prod_id = prod.get('productId')
            current_active_ids.append(prod_id)

            # 查重 (需求4)
            cursor.execute("SELECT status FROM products WHERE id = ?", (prod_id,))
            row = cursor.fetchone()

            if not row:
                # 新商品！插入数据库并去跑“点收藏”接口 (需求3)
                cursor.execute(
                    "INSERT INTO products VALUES (?, ?, ?, ?, ?)",
                    (prod_id, prod.get('title'), prod.get('price'), 'active', str(datetime.date.today()))
                )
                collect_product(prod_id)
            else:
                # 已存在商品，更新状态为活跃
                cursor.execute("UPDATE products SET status = 'active' WHERE id = ?", (prod_id,))

        # 更新分页参数（如果接口返回了新的pageToken，记得在这里替换）
        page += 1

    conn.commit()

    # 5. 监控哪些卖掉了 (需求2)
    # 昨天是 'active'，但今天抓取的所有商品里没有它，说明被卖掉了
    cursor.execute("SELECT id FROM products WHERE status = 'active'")
    all_stored_active = [r[0] for r in cursor.fetchall()]

    sold_items = list(set(all_stored_active) - set(current_active_ids))

    if sold_items:
        print(f"发现有 {len(sold_items)} 个商品已卖掉！")
        for s_id in sold_items:
            cursor.execute("UPDATE products SET status = 'sold' WHERE id = ?", (s_id,))
            # 这里可以写日志或者弹窗告诉客户哪些ID卖掉了
            print(f"商品ID: {s_id} 已下架/卖掉")
        conn.commit()

    conn.close()
    print("--- 任务运行结束 ---")


if __name__ == "__main__":
    main()

