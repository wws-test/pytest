# coding=utf-8
import os
from common.readconfig import ini
import pytest
import allure
from page_object.Createplan import *
from faker import Faker
from page_object.Bd_test import bd_test
from tools.logger import Log

log = Log().logger
fake = Faker(locale='zh_CN')
name = fake.name()


@allure.feature("bd-后台审核")
# @pytest.mark.flaky(reruns=2, reruns_delay=5)
class TestCreatpl:

    @pytest.fixture(scope='function', autouse=True)
    def create(self, drivers):
        bd = bd_test(drivers)
        bd.get_url(ini.bdurl)
        bd.login()

    @pytest.mark.skip(reason="no way of currently testing this")
    @allure.story("创建人群包-搜索")
    def test_cw(self, drivers):
        bd = bd_test(drivers)
        bd.createcw()

    @pytest.mark.dependency(depends=["cart"], scope="session")
    @allure.story("审核-任务")
    def test_ch(self, drivers):
        bd = bd_test(drivers)
        bd.check()


if __name__ == '__main__':
    pass
