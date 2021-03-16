# coding=utf-8
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys

from common.readconfig import ini
from page.basepage import Page, sleep
from common.readelement import Element
from common import readconfig
from faker import Faker


fake = Faker(locale='zh_CN')
fake.seed(4321)
name = fake.company()
ad = fake.address()
post = fake.postcode()
url = fake.url()
search = Element('search')



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
    def Fill_note_plan(self):
        """填写短信内容"""
        sleep(1)
        self.focus(search['提交'])
        self.send_key(search['短信计划名称'], post)
        self.send_key(search['内容'], "【短信签名】%s" % ad)
        self.isclick(search['置入动态短链'])
        self.send_key(search['短链'], url)
        self.isclick(search['提交审核'])

    def Fill_video_plan(self):
        """填写视频短信内容"""
        sleep(1)
        self.focus(search['提交审核'])
        self.isclick(search['选择视频短信'])
        self.send_key(search['视频计划名称'], post)
        self.isclick(search['选择模板'])
        self.isclick(search['点击模板'])
        self.isclick(search['模板确定'])
        self.isclick(search['提交审核'])

    def get_result(self):
        a = self.get_text(search['待审核'])
        return a


    def alreadyplan(self):
        """提交已有计划"""
        self.focus(search['提交'])
        self.send_key(search['短信计划名称'], name)
        self.isclick(search['选择已有计划'])
        self.isclick(search['下拉框'])
        self.isclick(search['下拉框第一个'])
        self.isclick(search['提交审核'])

    def Create_template(self):
        """创建短信模板"""
        self.isclick(search['我的模板'])
        self.isclick(search['视频短信'])
        self.isclick(search['创建模板'])
        self.send_key(search['主题'],post)
        self.isclick(search['文本帧'])
        self.isclick(search['视频帧'])
        self.send_key(search['输入文本帧'],"【短信签名】%s" % ad)
        self.isclick(search['点击上传视频'])
        self.upload_file("C:\\Users\\Administrator\\Desktop\\passages\\test.mp4")
        self.isclick(search['提交审核'])


if __name__ == '__main__':
    pass
