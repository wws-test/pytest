#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import functools
import json
import os

import pytest
from tep.fixture import TepVars

from apitest.core.checkreult import check_results
from apitest.core.request import req
from common.ApiData import testinfo
from typing import List

from config.conf import BASE_DIR, DATA_DIR
from tools.logger import log


# 中文编码


def pytest_collection_modifyitems(
    session: "Session", config: "Config", items: List["Item"]
) -> None:
    for item in items:
        item.name = item.name.encode('utf-8').decode('unicode-escape')
        item._nodeid = item.nodeid.encode('utf-8').decode('unicode-escape')


def get_data(yaml_file_name):
    try:
        data_file_path = os.path.join(DATA_DIR, yaml_file_name)
        yaml_data = testinfo.load(data_file_path)
    except Exception as ex:
        pytest.skip(str(ex))
    else:
        return yaml_data


base_data = get_data("base_data.yaml")


@pytest.fixture(scope='session')
def test_is_login(request):
    """登录"""
    r = req(
        testinfo.load(testinfo.base_login)('method'),
        testinfo.load(testinfo.base_login)('route'),
        testinfo.load(testinfo.base_login)('extractresult'),
        **testinfo.load(testinfo.base_login)('RequestData'))
    result = json.loads(r.text)
    check_results(r, testinfo.stand_info('登录'))
    if 'token' in result:
        req.headers['Authorization'] = "JWT " + result['token']

    def fn():
        req.close_session()

    request.addfinalizer(fn)
    
#用例重复执行装饰器
def repeat(count=1):
    def callables(func):
        @functools.wraps(func)
        def warpper(*args,**kwargs):
            for i in range(count):
                print("当前执行第%d"%i)
                func(*args,**kwargs)
        return warpper
    return callables

# @pytest.fixture(scope="function")
# def delete_register_user():
#     """注册用户前，先删除数据，用例执行之后，再次删除以清理数据"""
#     try:
#         del_sql = base_data["init_sql"]["delete_register_user"]
#         db.execute_db(del_sql)
#         log.info("注册用户操作：清理用户--准备注册新用户")
#         log.info("执行前置SQL：{}".format(del_sql))
#     except:
#         print('sql报错')
#     yield  # 用于唤醒 teardown 操作  yield转后置
#     db.execute_db(del_sql)
#     log.info("注册用户操作：删除注册的用户")
#     log.info("执行后置SQL：{}".format(del_sql))


if __name__ == '__main__':
    pass
