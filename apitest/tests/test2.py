#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import pytest
import allure

from apitest.tests.operation.axb_operation import login_uesr
from common.ApiData import testinfo
from tools.logger import log


@allure.feature("业务流程API测试")
@allure.story("用例--登录用户")
@allure.description("该用例是针对获取用户注册接口的测试")
@pytest.mark.parametrize(
    "username, password, rememberMe, verificationCode, except_result, except_msg",
    testinfo.load(testinfo.base_login)["test_login_user"],
    ids=['登录成功', '登陆失败'])
@pytest.mark.usefixtures("delete_register_user")
def test_register_user(
        username,
        password,
        rememberMe,
        verificationCode,
        except_result,
        except_msg):

    result=login_uesr(username, password, rememberMe, verificationCode,except_result,except_msg)
    assert except_msg in result.text
    log.info("except_msg就是%s "% result.text)


if __name__ == "__main__":
    pytest.main(['test_business.py'])
