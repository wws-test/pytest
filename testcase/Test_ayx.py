# coding=utf-8
import os
import re
import pytest
import allure
from pytest_base_url.plugin import base_url

from page_object.Createplan import *
from faker import Faker

from page_object.upload import upload
from tools.logger import Log

log = Log().logger
fake = Faker(locale='zh_CN')
name = fake.name()


@allure.feature("jzyx-基本流程")
# @pytest.mark.flaky(reruns=2, reruns_delay=5)
@pytest.mark.precision
class TestCreatpl():
    @pytest.fixture(scope='function', autouse=True)
    def login(self, drivers):
        Create = Createpl(drivers)
        Create.get_url(ini.url)
        Create.login()

    # @pytest.mark.skip(reason="no way of currently testing this")
    # @pytest.mark.run(order=1)
    @allure.story("创建计划-输入内容-提交计划")
    @pytest.mark.run(order=1)
    def test_createplan(self, drivers):
        """点击营销
            创建计划
            选择人群包-输入计划内容"""
        Create = Createpl(drivers)
        Create.clickprecision()
        Create.Selectcrowd()
        Create.Fillplan()
        result = Create.get_result()
        log.info("结果".format(result))
        assert result == "提交成功，等待审核..."

    # @pytest.mark.skip(reason="no way of currently testing this")
    @pytest.mark.run(order=2)
    @allure.story("创建人群包-上传人群包")
    @pytest.mark.test1
    def test_crowd(self, drivers):
        uploading = upload(drivers)
        uploading.up1()
        result = uploading.created_crowd()
        log.info("人群包名称".format(result))
        assert result == uploading.na()

    @allure.story("创建人群包-搜索")
    @pytest.mark.run(order=3)
    def test_search(self, drivers):
        uploading = upload(drivers)
        uploading.search_r()


if __name__ == '__main__':
    pytest.main(['testcase/Test_ayx::test_createplan'])

    print(name)
