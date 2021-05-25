#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import  sys
sys.path.append(r"D:\pytst\conftest.py")
import os
import base64
import pytest
import allure
from py._xmlgen import html
from selenium import webdriver
from common.readconfig import ini
from config.conf import SCREENSHOT_DIR
from common.inspects import inspect_element
from tools.time import datetime_strftime, timestamp
from tools.clear import picclear
driver = None


@pytest.fixture(scope='session', autouse=True)
def drivers(request):
    global driver
    if driver is None:
        options = webdriver.ChromeOptions()
        options.add_argument('--blink-settings=imagesEnabled=false')
        driver = webdriver.Chrome(
            options=options,
            executable_path=r"C:\\Program Files\\Google\Chrome\\Application\\chromedriver.exe")
    inspect_element()
    picclear()

    def fn():
        driver.quit()
    # 将fn方法作为整体运行的结尾
    request.addfinalizer(fn)
    return driver


# 注册自定义参数 cmdopt 到配置对象
def pytest_addoption(parser):
    parser.addoption("--testenv", action="store",
                     default="http://192.168.0.202/precision-web/login#/login",
                     help="将自定义命令行参数 ’--testenv' 添加到 pytest 配置中")
    parser.addoption("--bdenv", action="store",
                     default="http://192.168.0.202/mgt/login",
                     help="将自定义命令行参数 ’--bdenv' 添加到 pytest 配置中")

@pytest.mark.hookwrapper
def pytest_runtest_makereport(item):
    """
    当测试失败的时候，自动截图，展示到html报告中
    :param item:
    """
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, 'extra', [])

    if report.when == 'call' or report.when == "setup":
        xfail = hasattr(report, 'wasxfail')
        if (report.skipped and xfail) or (report.failed and not xfail):
            screen_img = _capture_screenshot()
            if screen_img:
                html = '<div><img src="data:image/png;base64,%s" alt="screenshot" style="width:1024px;height:768px;" ' \
                       'onclick="window.open(this.src)" align="right"/></div>' % screen_img
                extra.append(pytest_html.extras.html(html))
        report.extra = extra
        report.description = str(item.function.__doc__)


@pytest.mark.optionalhook
def pytest_html_results_table_header(cells):
    cells.insert(1, html.th('用例名称'))
    cells.insert(2, html.th('Test_nodeid'))
    cells.pop(2)


@pytest.mark.optionalhook
def pytest_html_results_table_row(report, cells):
    cells.insert(1, html.td(report.description))
    cells.insert(2, html.td(report.nodeid))
    cells.pop(2)


@pytest.mark.optionalhook
def pytest_html_results_table_html(report, data):
    if report.passed:
        del data[:]
        data.append(html.div('通过的用例未捕获日志输出.', class_='empty log'))


@pytest.mark.optionalhook
def pytest_html_report_title(report):
    report.title = "pytest示例项目测试报告"


@pytest.mark.optionalhook
def pytest_configure(config):
    config._metadata.clear()
    config._metadata['测试项目'] = "精准营销"
    config._metadata['测试地址'] = ini.url


@pytest.mark.optionalhook
def pytest_html_results_summary(prefix, summary, postfix):
    # prefix.clear() # 清空summary中的内容
    prefix.extend([html.p("所属部门: 艾塔公司测试部")])
    prefix.extend([html.p("测试执行人: sww")])


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """收集测试结果"""
    result = {
        "total": terminalreporter._numcollected,
        'passed': len(terminalreporter.stats.get('passed', [])),
        'failed': len(terminalreporter.stats.get('failed', [])),
        'error': len(terminalreporter.stats.get('error', [])),
        'skipped': len(terminalreporter.stats.get('skipped', [])),
        # terminalreporter._sessionstarttime 会话开始时间
        'total times': timestamp() - terminalreporter._sessionstarttime
    }
    print(result)
    # if result['failed'] or result['error']:
    #     send_report()


def _capture_screenshot():
    '''
    截图保存为base64
    '''
    now_time = datetime_strftime("%Y%m%d%H%M%S")
    if not os.path.exists(SCREENSHOT_DIR):
        os.makedirs(SCREENSHOT_DIR)
    screen_path = os.path.join(SCREENSHOT_DIR, "{}.png".format(now_time))
    driver.save_screenshot(screen_path)
    allure.attach.file(screen_path, "测试失败截图...{}".format(
        now_time), allure.attachment_type.PNG)
    with open(screen_path, 'rb') as f:
        imagebase64 = base64.b64encode(f.read())
    return imagebase64.decode()


def pytest_configure(config):
    config.addinivalue_line("markers", "precision:精准营销")
    config.addinivalue_line("markers", "business:后台")
    config.addinivalue_line("markers", "test1:测试单一用例")
