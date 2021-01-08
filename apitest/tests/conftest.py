#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import json
import pytest

from apitest.core.checkreult import check_results
from apitest.core.request import req
from common.ApiData import testinfo



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


if __name__ == '__main__':
    pass