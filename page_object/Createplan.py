# coding=utf-8
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys

from common.readconfig import ini
from page.basepage import Page, sleep
from common.readelement import Element
from common import readconfig
from faker import Faker

from tools.logger import Log

fake = Faker(locale='zh_CN')
name = fake.company()
ad = fake.address()
post = fake.postcode()
url = fake.url()
search = Element('search')
log = Log().logger


class Createpl(Page):
    """创建计划"""
    # def clear(self):
    #     self.driver.isclick(search['清除数据'])
    #     self.driver.isclick(search['确认'])

    def login(self):
        self.refresh()
        self.send_key(search['账号'], ini.account)
        self.send_key(search['密码'], ini.passwd)
        self.isclick(search['登录'])
        sleep(1)

    def pelogin(self):
        self.send_key(search['账号'], ini.peaccount)
        self.send_key(search['密码'], ini.pepasswd)
        self.isclick(search['登录'])
        sleep(1)

    def clickprecision(self):
        # 点击第一个
        self.isclick(search['营销标签'])
        sleep(1)
        self.isclick(search['创建'])
    def Selectcrowd(self):
        # 选择人群包 这边直接选了第一个
        self.isclick(search['第一个人群包'])
    def Fillplan(self):
        # 填写内容
        sleep(1)
        self.focus(search['提交'])
        self.send_key(search['计划名称'], post)
        self.send_key(search['内容'], "【短信签名】%s" % ad)
        self.isclick(search['置入动态短链'])
        self.send_key(search['短链'], url)
        self.isclick(search['提交'])

        sleep(1)

    def get_result(self):
        a = self.get_text(search['待审核'])
        return a
        log.info("待审核=：{}".format(a))

    def alreadyplan(self):
        self.focus(search['提交'])
        self.send_key(search['计划名称'], name)
        self.isclick(search['选择已有计划'])
        self.isclick(search['下拉框'])
        self.isclick(search['选择计划'])
        self.isclick(search['提交'])


if __name__ == '__main__':
    pass
