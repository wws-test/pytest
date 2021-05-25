#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import pytest
import allure
#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import pytest
import allure

from apitest.core.checkreult import check_results, check_code, check_message
from apitest.core.request import req
from common.ApiData import testinfo
from common.variable import is_vars
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
    req.headers=testinfo.load(testinfo.get_3150)['test_info']['headers']
    result = req(
        testinfo.load(testinfo.base_login)['method'],
        testinfo.load(testinfo.base_login)['route'],
        testinfo.load(testinfo.base_login).get('extractresult'),
        **json_data)
    bind = is_vars.get("companyId")
    log.info("提取只{}".format(bind))
    #检查响应码
    check_code(result, except_code)
    check_message(result,except_msg)
    # print(result.__dict__)
    log.info("code ==>> 期望结果：{}， 实际结果：【 {} 】".format(
        except_code, result.json().get("code")))
    log.info("msg就是{}".format(result.json().get("message")))
    return result