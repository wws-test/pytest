﻿from page.basepage import Page, sleep
from common.readelement import Element
from common import readconfig
from faker import Faker

fake = Faker(locale='zh_CN')
name = fake.company()
search = Element('search')
post = fake.postcode()


class upload(Page):
    def up(self):
        sleep(1)
        self.isclick(search['营销标签'])
        sleep(1)
        self.isclick(search['人群包管理'])
        self.isclick(search['上传人群包'])
        self.isclick(search['MD5'])
        sleep(1)
        self.isclick(search['定向拓展'])
        self.send_key(search['人群名称md'], name)
        # self.isclick(search['点击上传'])
        self.isclick(search['取消'])

    def search_r(self):
        sleep(1)
        self.isclick(search['营销标签'])
        self.isclick(search['人群包管理'])
        self.send_key(search['人群查询'], "ww")
        self.isclick(search['查询'])

    def imagine(self):
        return [x.text for x in self.find_elements(search['查询结果'])]
    def up1(self):
        self.isclick(search['人群包管理'])
        sleep(1)
        self.isclick(search['上传人群包'])
        self.isclick(search['MD5'])
        sleep(1)
        self.isclick(search['定向拓展'])
        self.send_key(search['人群名称md'], name)
        self.isclick(search['点击上传'])
        sleep(1)
        self.isclick(search['点击上传'])
        self.upload_file('C:\\Users\\Administrator\\Desktop\\sww22.rar')
        self.isclick(search['确定'])
    def created_crowd(self):
        a=self.get_text(search['已创建人群包'])
        return  a
    def na(self):
        return name

    def text(self):
        self.get_text(search['人群名称'])


if __name__ == '__main__':
    pass
