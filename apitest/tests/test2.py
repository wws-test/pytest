#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import json

import pytest
import allure

from apitest.core.checkreult import check_results
from apitest.core.request import req
from apitest.tests.conftest import repeat
from apitest.tests.operation.axb_operation import login_uesr
from common.ApiData import testinfo
from tools.logger import log


@allure.feature("业务流程API测试")
@allure.story("用例--登录用户")
@allure.description("该用例是针对获取用户登录接口的测试")
@pytest.mark.parametrize(
    "username, password, force, except_result, except_msg",
    testinfo.load(testinfo.base_login)["RequestData"],
    ids=['登录成功'])
def test_register_user(
        username,
        password,
        force,
        except_result,
        except_msg):

    result=login_uesr(username, password, force,except_result,except_msg)
    assert except_msg in result.text
    if 'token' in result:
        req.headers['Authorization'] = "JWT " + result['token']
    log.info("except_msg就是%s "% result.text)

@pytest.mark.parametrize('case',
                             testinfo.load(testinfo.check_create)['RequestData'],
                             ids=['新建考评任务'])
def test_check_create(case):
    try:
        #拼装参数
        data={'data':case}
        #发送请求
        r = req(
            testinfo.load(testinfo.check_create)['method'],
            testinfo.load(testinfo.check_create)['route'],
            testinfo.load(testinfo.check_create).get('extractresult'),
            **data)
        check_results(r, testinfo.load(testinfo.check_create))
    except:
        pass
@repeat(3)
def test_axc():
       print("112323")

if __name__ == "__main__":
    pytest.main(['test_business.py'])
