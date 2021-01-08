import json
import allure
import requests
import urllib3

from requests import Response
from requests.exceptions import RequestException
from requests.status_codes import codes
from apitest.core.getresult import get_result
from apitest.core.serialize import serialization, deserialization
from common.ApiData import testinfo
from common.RegExp import regs
from tools.logger import log
urllib3.disable_warnings()

__all__ = ['req', 'codes']

class HttpRequest(object):

    def __init__(self):
        self.timeout = 30.0
        self.r = requests.session()
        self.headers = testinfo.test_info('headers')

    def send_request(self, method: str, route: str, extract: str, **kwargs):
        """发送请求
                :param method: 发送方法
                :param route: 发送路径
                optional 可选参数
                :param extract: 要提取的值
                :param params: 发送参数-"GET"
                :param data: 发送表单-"POST"
                :param json: 发送json-"post"
                :param headers: 头文件
                :param cookies: 验证字典
                :param files: 上传文件,字典：类似文件的对象``
                :param timeout: 等待服务器发送的时间
                :param auth: 基本/摘要/自定义HTTP身份验证
                :param allow_redirects: 允许重定向，默认为True
                :type bool
                :param proxies: 字典映射协议或协议和代理URL的主机名。
                :param stream: 是否立即下载响应内容。默认为“False”。
                :type bool
                :param verify: （可选）一个布尔值，在这种情况下，它控制是否验证服务器的TLS证书或字符串，在这种情况下，它必须是路径到一个CA包使用。默认为“True”。
                :type bool
                :param cert: 如果是字符串，则为ssl客户端证书文件（.pem）的路径
                :return: request响应
                """
        pass
        method = method.upper()
        url = testinfo.test_info('url') + route
        try:
            log.info("Request Url: {}".format(url))
            log.info("Request Method: {}".format(method))
            if kwargs:
                kwargs_str = serialization(kwargs)
                is_sub = regs.findall(kwargs_str)
                if is_sub:
                    new_kwargs_str = deserialization(regs.subs(is_sub, kwargs_str))
                    kwargs = new_kwargs_str
            log.info("Request Data: {}".format(kwargs))
            if method == "GET":
                response = self.r.get(
                    url, **kwargs, headers=self.headers, timeout=self.timeout)
            elif method == "POST":
                response = self.r.post(
                    url, **kwargs, headers=self.headers, timeout=self.timeout)
            elif method == "PUT":
                response = self.r.put(
                    url, **kwargs, headers=self.headers, timeout=self.timeout)
            elif method == "DELETE":
                response = self.r.delete(
                    url, **kwargs, headers=self.headers, timeout=self.timeout)
            elif method in ("OPTIONS", "HEAD", "PATCH"):
                response = self.r.request(
                    method,
                    url,
                    **kwargs,
                    headers=self.headers,
                    timeout=self.timeout)
            else:
                raise AttributeError("send request method is ERROR!")
            with allure.step("%s请求接口" % method):
                allure.attach(url, name="请求地址")
                allure.attach(str(response.headers), "请求头")
                if kwargs:
                    allure.attach(
                        json.dumps(
                            kwargs,
                            ensure_ascii=False),
                        name="请求参数")
                allure.attach(str(response.status_code), name="响应状态码")
                allure.attach(str(elapsed_time(response)), name="响应时间")
                allure.attach(response.text, "响应内容")
            log.info(response)
            log.info("Response Data: {}".format(response.text))
            if extract:
                get_result(response, extract)
            return response
        except RequestException as e:
            log.exception(format(e))
        except Exception as e:
            raise e

    def __call__(self, *args, **kwargs):
        return self.send_request(*args, **kwargs)

    def close_session(self):
        print("关闭会话")
        self.r.close()


def elapsed_time(func: Response, fixed: str = 's'):
    """
    用时函数
    :param func: response实例
    :param fixed: 1或1000 秒或毫秒
    :return:
    """
    try:
        if fixed.lower() == 's':
            second = func.elapsed.total_seconds()
        elif fixed.lower() == 'ms':
            second = func.elapsed.total_seconds() * 1000
        else:
            raise ValueError("{} not in ['s'，'ms']".format(fixed))
        return second
    except RequestException as e:
        log.exception(e)
    except Exception as e:
        raise e


req = HttpRequest()

if __name__ == '__main__':
    req()
