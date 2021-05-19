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


@allure.feature("基础平台登录")
def login_uesr(
        username,
        password,
        force,
        except_code,
        except_msg):
    json_data = {"data":{
        "username": username,
        "password": password,
        "force": force
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
    log.info("msg就是{}".format(result.json().get("message")))
    return result