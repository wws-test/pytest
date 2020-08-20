#coding=utf-8
import pytest
from selenium.webdriver.common.keys import Keys

from common.readconfig import ini
from page.basepage import Page, sleep
from common.readelement import Element
from common import readconfig
from faker import Faker

fake = Faker(locale='zh_CN')
name = fake.company()
ad=fake.address()
post=fake.postcode()
post1=fake.postcode()
url=fake.url()
search = Element('back')

class bd_test(Page):
    def login(self):
        self.refresh()
        self.send_key(search['用户名'], ini.bdaccount)
        self.send_key(search['密码'], ini.bdpasswd)
        sleep(1)
        self.isclick(search['登录'])
        sleep(1)


    def check(self):
        self.isclick(search['审核'])
        self.isclick(search['通过'])
        self.isclick(search['确定'])
    def createcw(self):
        self.isclick(search['人群包管理'])
        self.isclick(search['创建人群包'])
        self.isclick(search['人群包选择'])
        self.isclick(search['下拉框选择'])
        sleep(1)
        self.send_key(search['人群名称'],name)
        self.isclick(search['适用行业'])
        self.isclick(search['行业选择'])
        self.send_key(search['人群标签'],post)
        self.isclick(search['添加'])
        self.send_key(search['人群标签'],post1)
        self.isclick(search['添加'])
        self.isclick(search['确定创建'])
