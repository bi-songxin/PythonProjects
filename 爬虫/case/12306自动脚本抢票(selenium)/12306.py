# 导入time模块，用于程序休眠
import time
# 导入datetime和timedelta模块，用于动态处理日期
from datetime import datetime, timedelta
# 导入selenium的webdriver模块，用于控制浏览器
from selenium import webdriver
# 导入By模块，用于定位页面元素（如通过ID、XPath等）
from selenium.webdriver.common.by import By
# 导入显式等待类，用于智能等待元素出现
from selenium.webdriver.support.ui import WebDriverWait
# 导入期望条件，用于定义等待的条件
from selenium.webdriver.support import expected_conditions as EC
# 导入TimeoutException，用于捕获等待超时异常
from selenium.common.exceptions import TimeoutException
# 导入Chrome浏览器的选项配置类
from selenium.webdriver.chrome.options import Options
# 导入Chrome浏览器的服务类，用于指定ChromeDriver路径
from selenium.webdriver.chrome.service import Service


# 定义火车票自动抢票机器人类
class TrainTicketBot:
    # 初始化方法，创建对象时自动执行，接收出发地、目的地、出发时间和乘客姓名四个参数
    def __init__(self, from_station, to_station, departure_time, passenger_name='毕松鑫'):
        # 将出发地参数赋值给实例变量
        self.from_st = from_station
        # 将目的地参数赋值给实例变量
        self.to_st= to_station
        # 将出发时间参数赋值给实例变量
        self.de_time = departure_time
        # 将乘客姓名参数赋值给实例变量，默认值为'毕松鑫'
        self.passenger = passenger_name
        # 创建Chrome浏览器选项配置对象
        self.options = Options()
        # 设置实验性选项：排除启用自动化的开关，避免被网站识别为自动化脚本
        self.options.add_experimental_option('excludeSwitches', ['enable-automation'])
        # 添加参数：禁用自动化控制特征，进一步伪装成真实用户
        self.options.add_argument('--disable-blink-features=AutomationControlled')
        # 添加参数：禁用浏览器信息栏（如"Chrome正在被自动化软件控制"的提示）
        self.options.add_argument('--disable-infobars')
        # 创建ChromeDriver服务对象，指定chromedriver可执行文件的路径
        service = Service(executable_path='/usr/local/bin/chromedriver/chromedriver')
        # 创建Chrome浏览器驱动对象，传入服务对象和选项配置
        self.driver = webdriver.Chrome(service=service,options=self.options)
        # 最大化浏览器窗口，确保页面元素可见
        self.driver.maximize_window()

    # 定义判断元素是否存在的方法，接收元素的XPath表达式作为参数
    def is_element_exist(self, element):
        # 使用try-except捕获异常
        try:
            # 尝试通过XPath定位元素，如果找到则返回True
            self.driver.find_element(By.XPATH, element)
            return True
        # 如果发生异常（元素未找到）
        except:
            # 返回False
            return False

    # 定义选择可购车票信息的方法，实现自动抢票的核心逻辑
    def check_ticket(self):
        # 打开12306登录页面
        self.driver.get("https://kyfw.12306.cn/otn/resources/login.html")

        # 判断是否登录成功（循环检查特定元素是否存在），最多等待5分钟
        max_wait_time = 300  # 最大等待时间300秒（5分钟）
        wait_time = 0  # 已等待时间
        while not self.is_element_exist('//a[@id="link_for_ticket"]'):
            # 每次循环休眠1秒，避免CPU占用过高（用户扫码等待，保留固定等待）
            time.sleep(1)
            wait_time += 1  # 累加等待时间
            # 如果超过最大等待时间，提示用户并退出程序
            if wait_time >= max_wait_time:
                print("登录超时！请重新运行程序扫码登录。")
                self.driver.quit()  # 关闭浏览器
                return  # 退出方法

        # 登录成功后，智能等待链接元素可点击，然后跳转到首页
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//a[@id="link_for_ticket"]'))
        ).click()

        # 使用try-except捕获抢票过程中可能出现的异常
        try:
            # 智能等待出发地输入框可交互，然后点击并输入
            from_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//input[@id="fromStationText"]'))
            )
            from_input.click()
            from_input.send_keys(self.from_st)
            # 智能等待站点选择元素出现并点击
            WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, '//div[@id="citem_0"]'))
            ).click()

            # 智能等待目的地输入框可交互，然后点击并输入
            to_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//input[@id="toStationText"]'))
            )
            to_input.click()
            to_input.send_keys(self.to_st)
            # 智能等待站点选择元素出现并点击
            WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, '//div[@id="citem_0"]'))
            ).click()

            # 智能等待日期输入框可交互，清空并输入日期
            date_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//input[@id="train_date"]'))
            )
            date_input.clear()
            date_input.send_keys(self.de_time)

            # 智能等待"查询"按钮可点击，然后点击查询
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//a[@id="query_ticket"]'))
            ).click()

            # 智能等待"预订"按钮出现并点击
            WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, '//a[text()="预订"]'))
            ).click()

            # 智能等待乘车人复选框可点击，然后选择
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, f'//label[text()="{self.passenger}"]'))
            ).click()
            # 在控制台输出选择成功的提示信息
            print("选择成功")

            # 智能等待提交订单按钮可点击，然后点击
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//a[text()="提交订单"]'))
            ).click()
            # 在控制台输出提交成功的提示信息
            print("提交成功")

            # 智能等待确认订单按钮可点击，然后点击
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, 'qr_submit_id'))
            ).click()
            # 在控制台输出确认成功的提示信息
            print("确认成功")

        # 如果在抢票过程中发生任何异常
        except Exception as e:
            # 在控制台输出重试的提示信息
            print(f"错误：{e}")
            print("=========================选票异常重试中=============================")

        # 在控制台输出支付提示信息
        print("请在15分制内支付订单")

        # 休眠60秒，保持程序运行，给用户时间支付订单（手动支付等待，保留固定等待）
        time.sleep(60)


# 判断是否为主程序运行（而非被导入为模块）
if __name__ == "__main__":
    # 定义出发地变量，设置为深圳东
    from_station = '深圳东'

    # 定义目的地变量，设置为常德
    to_station = '常德'

    # 设置出行日期变量，自动获取明天的日期（最多只能设置15天内）
    departure_time = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')

    # 实例化TrainTicketBot类，传入出发地、目的地和出发时间
    T= TrainTicketBot(from_station, to_station, departure_time)

    # 调用check_ticket方法，开始自动抢票流程
    T.check_ticket()

