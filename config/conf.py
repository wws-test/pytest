import os
from selenium.webdriver.common.by import By
# 项目目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 配置文件
YAML_PATH= os.path.join(BASE_DIR, 'config', 'config.yaml')

INI_PATH =  os.path.join(BASE_DIR, 'config', 'config.ini')

# 页面元素目录
ELEMENT_PATH = os.path.join(BASE_DIR, 'page_element')

# 日志目录
LOG_PATH = os.path.join(BASE_DIR, 'logs')

# 截图目录
SCREENSHOT_DIR = os.path.join(BASE_DIR, 'screen_capture')

# 数据文件
DATA_DIR = os.path.join(BASE_DIR, 'apitest\\apiData')

WORKFLOW=os.path.join(BASE_DIR, 'apitest\\apiData\\workflow')

# 报告目录
REPORT_PATH = os.path.join(BASE_DIR, 'report', 'report.html')

# 元素定位的类型
LOCATE_MODE = {
    'css': By.CSS_SELECTOR,
    'xpath': By.XPATH,
    'name': By.NAME,
    'id': By.ID,
    'class': By.CLASS_NAME
}

# 邮件信息
EMAIL_INFO = {
    'username': '1092587222@qq.com',  # 切换成你自己的地址
    'password': 'kmpxmxunnsrhbagd',
    'smtp_host': 'smtp.qq.com',
    'smtp_port': 465
}

# 收件人
ADDRESSEE = [
    '1092587222@qq.com',
]

if __name__ == '__main__':
    print(DATA_DIR)