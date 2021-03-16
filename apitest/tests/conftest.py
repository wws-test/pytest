#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import json
import os

import pytest

from apitest.core.checkreult import check_results
from apitest.core.request import req
from common.ApiData import testinfo
from typing import List

from config.conf import BASE_DIR, DATA_DIR
from tools.logger import log
from tools.sqltools import db

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
def is_login(request):
    """登录"""
    r = req(testinfo.login_info('method'), testinfo.login_info('route'),
            testinfo.login_info('extractresult'), **testinfo.login_info('RequestData'))
    result = json.loads(r.text)
    check_results(r, testinfo.stand_info('登录'))
    if 'token' in result:
        req.headers['Authorization'] = "JWT " + result['token']

    def fn():
        req.close_session()

    request.addfinalizer(fn)
@pytest.fixture(scope="function")
def delete_register_user():
    """注册用户前，先删除数据，用例执行之后，再次删除以清理数据"""
    del_sql = base_data["init_sql"]["delete_register_user"]
    db.execute_db(del_sql)
    log.info("注册用户操作：清理用户--准备注册新用户")
    log.info("执行前置SQL：{}".format(del_sql))
    yield # 用于唤醒 teardown 操作  yield转后置
    db.execute_db(del_sql)
    log.info("注册用户操作：删除注册的用户")
    log.info("执行后置SQL：{}".format(del_sql))


class TepVars(object):
    pass


@pytest.fixture(scope="session")
def env_vars(config):
    class Clazz(TepVars):
        env = config["env"]

        """Variables define start"""
        # Environment and variables
        mapping = {
            "qa": {
                "domain": "https://qa.com",
                "mysql_engine": mysql_engine("127.0.0.1",  # host
                                             "2306",  # port
                                             "root",  # username
                                             "123456",  # password
                                             "qa"),  # db_name
            },
            "release": {
                "domain": "https://release.com",
                "mysql_engine": mysql_engine("127.0.0.1",
                                             "2306",
                                             "root",
                                             "123456",
                                             "release"),
            }
            # Add your environment and variables
        }
        # Define properties for auto display
        domain = mapping[env]["domain"]
        mysql_engine = mapping[env]["mysql_engine"]
        """Variables define end"""

    return Clazz()
if __name__ == '__main__':
    pass