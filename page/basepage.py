from selenium.common.exceptions import TimeoutException, ElementNotVisibleException, ElementNotSelectableException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config.conf import LOCATE_MODE
from tools.time import sleep
from tools.logger import log
from selenium.webdriver.support.ui import Select
from common.readelement import Element
from common.upload_file import upload
search = Element('search')


class Page(object):
    '''
    page基类，所有page都应该继承该类
    '''

    def __init__(self, driver):
        # 要引用driver，但是这里还未定义具体的浏览器，所以用self.driver代替
        self.driver = driver
        self.timeout = 30
        self.wait = WebDriverWait(self.driver, self.timeout)


    @staticmethod
    def element_locator(func, locator):
        """元素定位器"""
        name, value = locator
        return func(LOCATE_MODE[name], value)

    def find_element(self, locator):
        """寻找单个元素"""
        return Page.element_locator(lambda *args: self.wait.until(
            EC.presence_of_element_located(args)), locator)

    def find_elements(self, locator):
        """查找多个相同的元素"""
        return Page.element_locator(lambda *args: self.wait.until(
            EC.presence_of_all_elements_located(args)), locator)

    def elements_num(self, locator):
        """获取相同元素的个数"""
        number = len(self.find_elements(locator))
        log.info("相同元素：{}".format((locator, number)))
        return number

    def isclick(self, locator):
        """点击"""
        """点击"""
        self.find_element(locator).click()
        sleep()
        log.info("点击元素：{}".format(locator))

    def on_page(self, pagetitle):
        return pagetitle in self.driver.title

    def get_url(self, base_url):
        """打开网址并验证"""
        self.driver.maximize_window()
        self.driver.set_page_load_timeout(60)
        try:
            self.driver.get(base_url)
            self.driver.implicitly_wait(10)
            log.info("打开网页：%s" % base_url)
        except TimeoutException:
            raise TimeoutException("打开%s超时请检查网络或网址服务器" % base_url)

    def switch_frame(self, loc):
        return self.driver.switch_to.frame(loc)

    def script(self, src):
        self.driver.execute_script(src)

    def refresh(self):
        """刷新页面F5"""
        self.driver.refresh()
        self.driver.implicitly_wait(30)

    def element_text(self, locator):
        """获取当前的text"""
        _text = self.find_element(locator).text
        log.info("获取文本：{}".format(_text))
        return _text

    def send_key(self, locator, text):
        """输入(输入前先清空)"""
        sleep(1)
        ele = self.find_element(locator)
        ele.clear()
        ele.send_keys(text)
        log.info("输入文本：{}".format(text))

    def focus(self, locator):
        # 聚焦到某个元素
        target = self.find_element(locator)
        self.driver.execute_script("arguments[0].scrollIntoView();", target)
        sleep(0.5)

    def option(self, locator):
        # 定位下拉框
        select = self.driver.find_element(locator)
        # 定位列表
        Select(select).select_by_index(1)

    def get_text(self, locator):
        """获取当前的text"""
        _text = self.find_element(locator).text
        log.info("获取文本：{}".format(_text))
        return _text

    # def display(self, locator):
    #     self.driver.is_displayed(locator)

    def upload_file(self, filename, browser_type="chrome"):
        '''
        非input标签的文件上传
        :param filename: 文件名（绝对路径）
        :param img_doc: 截图说明
        :param browser_type: 浏览器类型
        :return:
        '''
        try:
            log.info("上传文件（{}）".format(filename))
            sleep(2)
            upload(filePath=filename, browser_type=browser_type)
        except Exception as e:
            log.error("上传文件（{}）失败！".format(filename))
            raise e
        else:
            sleep(2)

    def wait(self):
        wait = WebDriverWait(self.driver, 10, poll_frequency=1, ignored_exceptions=[
                             ElementNotVisibleException, ElementNotSelectableException])
        # ww = wait.until(EC.element_to_be_clickable((locator)))


if __name__ == '__main__':
    pass
