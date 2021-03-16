#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import pytest
import allure
#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import pytest
import allure

from apitest.core.checkreult import check_results
from apitest.core.request import req
from common.ApiData import testinfo
from tools.logger import log


@allure.feature("业务流程API测试")
def login_uesr(
        username,
        password,
        rememberMe,
        verificationCode,
        except_code,
        except_msg):
    json_data = {"data":{
        "username": username,
        "password": password,
        "rememberMe": rememberMe,
        "verificationCode": verificationCode
    }}
    result = req(
        testinfo.load(testinfo.base_login)['method'],
        testinfo.load(testinfo.base_login)['route'],
        testinfo.load(testinfo.base_login).get('extractresult'),
        **json_data)
    #检查响应码
    # check_results(r, except_code)
    # print(result.__dict__)
    log.info("code ==>> 期望结果：{}， 实际结果：【 {} 】".format(
        except_code, result.json().get("code")))
    return result
