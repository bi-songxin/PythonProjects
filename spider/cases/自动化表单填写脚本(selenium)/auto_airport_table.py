import random
import time
import logging
from datetime import datetime
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('auto_table.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# 表单配置
FORMS_CONFIG = [
    {
        "name": "应急培训考核",
        "url": "https://ks.wjx.com/vm/Q0VHnVb.aspx#",
        "user_info_id": 16,
        "answers": {
            1: [4], 2: [1], 3: [3], 4: [2], 5: [2],  # 单选
            6: [1, 3], 7: [2], 8: [1, 3, 4], 9: [1, 2, 3], 10: [1, 3, 4],  # 多选
            11: [2], 12: [2], 13: [1], 14: [2], 15: [2]  # 判断
        }
    },
    {
        "name": "开机岗位",
        "url": "https://ks.wjx.com/vm/OBNmNYV.aspx#",
        "user_info_id": 26,
        "answers": {
            1: [2], 2: [2], 3: [4], 4: [3], 5: [1], 6: [2], 7: [3], 8: [1], 9: [3], 10: [2],  # 单选
            11: [1, 2, 3], 12: [1, 3], 13: [1, 2, 3, 4], 14: [1, 2, 3], 15: [1, 3],  # 多选
            16: [1, 2], 17: [1, 2, 3, 4], 18: [1, 2, 3, 4], 19: [1, 2, 3, 4], 20: [1, 3],  # 多选
            21: [1], 22: [2], 23: [1], 24: [1], 25: [1]  # 判断
        }
    },
    {
        "name": "防爆",
        "url": "https://ks.wjx.com/vm/QibhJmV.aspx#",
        "user_info_id": 26,
        "answers": {
            1: [4], 2: [2], 3: [1], 4: [1], 5: [3], 6: [1], 7: [1], 8: [2], 9: [1], 10: [2],  # 单选
            11: [1, 2, 3, 4], 12: [2, 3], 13: [1, 3], 14: [1, 2, 3, 4], 15: [1, 2, 3, 4],  # 多选
            16: [1, 3], 17: [1, 2, 3, 4], 18: [1, 2, 3, 4], 19: [1, 2, 3, 4], 20: [1, 2, 3],  # 多选
            21: [2], 22: [1], 23: [2], 24: [1], 25: [1]  # 判断
        }
    },
    {
        "name": "证件、人身",
        "url": "https://ks.wjx.com/vm/txGRedN.aspx#",
        "user_info_id": 21,
        "answers": {
            1: [2], 2: [1], 3: [4], 4: [2], 5: [2], 6: [4], 7: [1], 8: [1],  # 单选
            9: [1, 2, 4], 10: [1, 2, 3], 11: [2, 4], 12: [1, 2, 4],  # 多选
            13: [1, 2, 3, 4], 14: [1, 2, 3, 4], 15: [1, 2, 3, 4],  # 多选
            16: [2], 17: [1], 18: [2], 19: [2], 20: [1]  # 判断
        }
    }
]


class Auto_Table_Bot:
    def __init__(self, name, squad, id, driver=None):
        self.name = name
        self.squad = squad
        self.id = id

        # 如果没有共享同一浏览器
        if driver is None:
            self.options = Options()
            self.options.add_experimental_option('excludeSwitches', ['enable-automation'])
            self.options.add_argument('--disable-blink-features=AutomationControlled')
            self.options.add_argument('--disable-infobars')

            service = Service(executable_path='/usr/local/bin/chromedriver/chromedriver')
            self.driver = webdriver.Chrome(service=service, options=self.options)
            self.driver.maximize_window()
            self.own_driver = True
        else:
            self.driver = driver
            self.own_driver = False

        logger.info(f"初始化机器人 - 员工: {self.name} ({self.squad}, {self.id})")

    # 填写表单信息
    def fill_user_info(self, user_id_xpath_number):
        logger.info("填写用户信息")
        try:
            # 名字
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, f'//*[@id="q{user_id_xpath_number}_0"]'))
            ).send_keys(self.name)
            # 中队
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, f'//*[@id="q{user_id_xpath_number}_1"]'))
            ).send_keys(self.squad)
            # 编号
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, f'//*[@id="q{user_id_xpath_number}_2"]'))
            ).send_keys(self.id)
            logger.info("用户信息填写完成")
        except Exception as e:
            logger.error(f"填写用户信息失败: {e}")
            raise

    # 通用选择方法
    def good_select(self, title_num, *indices):
        for i in indices:
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, f'//*[@id="div{title_num}"]/div[2]/div[{i}]/div'))
            ).click()

    # 提交表单
    def good_submit(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="ctlNext"]'))
        ).click()
        logger.info("表单已提交")

    # 根据配置填写单个表单
    def fill_form_by_config(self, form_config):
        form_name = form_config["name"]
        url = form_config["url"]
        user_info_id = form_config["user_info_id"]
        answers = form_config["answers"]

        logger.info(f"开始填写表单: {form_name}")

        try:
            # 打开表单
            self.driver.get(url)
            logger.info(f"打开表单页面: {url}")

            # 填写所有答案
            for question_num, answer_indices in answers.items():
                self.good_select(question_num, *answer_indices)

            # 填写用户信息
            self.fill_user_info(user_info_id)

            logger.info(f"✓ {form_name} 填写完成")

            # 提交表单（可选）
            # time.sleep(30)
            # self.good_submit()

            return True

        except Exception as e:
            logger.error(f"✗ {form_name} 填写失败: {e}")
            return False

    def start_table(self):
        logger.info("=" * 50)
        logger.info(f"开始为员工 {self.name} 填写所有表单")

        success_count = 0
        failed_forms = []

        try:
            for index, form_config in enumerate(FORMS_CONFIG, 1):
                # 表单之间随机等待
                if index > 1:
                    time.sleep(random.uniform(0.5, 1))

                success = self.fill_form_by_config(form_config)
                if success:
                    success_count += 1
                else:
                    failed_forms.append(form_config["name"])

            # 所有表单填写完成
            logger.info("=" * 50)
            logger.info(f"员工 {self.name} 表单填写汇总:")
            logger.info(f"  成功: {success_count}/{len(FORMS_CONFIG)}")
            if failed_forms:
                logger.warning(f"  失败: {', '.join(failed_forms)}")

            time.sleep(random.uniform(2, 3))

            # 关闭浏览器（只有自己创建的才关闭）
            if self.own_driver:
                self.driver.quit()
                logger.info("浏览器已关闭")

        except TimeoutException as e:
            logger.error(f"元素等待超时：{e}")
        except NoSuchElementException as e:
            logger.error(f"元素未找到：{e}")
        except Exception as e:
            logger.error(f"未知错误: {e}")


def create_driver():
    """创建并配置浏览器驱动"""
    options = Options()
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--disable-infobars')

    service = Service(executable_path='/usr/local/bin/chromedriver/chromedriver')
    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()
    return driver


if __name__ == "__main__":
    # 员工列表
    employees = [
        {"name": "张三", "squad": "一中队", "id": "001"},
        {"name": "李四", "squad": "二中队", "id": "002"}
    ]

    logger.info(f"程序开始执行 - 共 {len(employees)} 名员工，{len(FORMS_CONFIG)} 个表单")

    # 共用浏览器，节省资源
    driver = create_driver()

    try:
        for emp in employees:
            bot = Auto_Table_Bot(emp["name"], emp["squad"], emp["id"], driver)
            bot.start_table()
    finally:
        # 无论try内代码是否发生总会执行
        driver.quit()
        logger.info("程序执行完成，浏览器已关闭")
