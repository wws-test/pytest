#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import allure

from requests import Response

from common.ApiData import testinfo
from common.variable import is_vars
from common.RegExp import regs
from tools.logger import log


def get_result(r: Response, extract):
    """获取值"""
    for i in extract:
        value = regs.getvalue(i, r.text)
        log.info("正则提取结果值：{}={}".format(i, value))
        is_vars.set(i, value)
        assert (is_vars.has(i))
    with allure.step("提取返回结果中的值"):
        for i in extract:
            allure.attach(name="提取%s" % i, body=''.join(is_vars.get(i)))






if __name__ == "__main__":
    pass