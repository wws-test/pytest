#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import ast
import json
import os
import random

from urllib import request

import deepdiff
import pytest
import allure
from deepdiff.commands import grep
from apitest.core.checkreult import check_results, check_code, check_message
from apitest.core.request import req
from common.ApiData import testinfo
from config.conf import DATA_DIR, WORKFLOW
import requests

@allure.feature("form模型测试")
class Test_form:

    @allure.story("查询所有流程模型")
    def test_get_models(self):
        json={'modelType':"0"}
        result = req("get", '/workflow/model/rest/models','message', params=json)
        check_code(result,200)
        check_message(result,'成功')

        # reuslt = json | grep("mike*", use_regexp=True)  diff 判断接口细粒度变化
    @allure.story("表单--查询申请表单")
    @allure.description("功能用途：让用户按照设计好的表单结构，进行申报填写")
    @pytest.mark.parametrize('case',testinfo.load(testinfo.get_start)['RequestData'], ids=['发布流程'])
    def test_get_StartTaskFormData(self,case):
        data={'data':case}
        r = req(
            testinfo.load(testinfo.get_start)['method'],
            testinfo.load(testinfo.get_start)['route'],
            testinfo.load(testinfo.get_start).get('extractresult'),
            **data)
        check_results(r, testinfo.load(testinfo.get_start))

if __name__ == "__main__":
    pytest.main(['test_business.py'])
