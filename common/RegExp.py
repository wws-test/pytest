import re

from apitest.core.serialize import is_json_str
from common.variable import is_vars
from tools.logger import log

import jsonpath

import json


class RegExp(object):

    def __init__(self):
        self.reg = re.compile
        """ 全量替换"""

    def findall(self, string):
        key = self.reg(r"\{{.*?}}").findall(string)
        return key
    # 替换变量

    def subs(self, keys, string):
        result = None
        for i in keys:
            log.info("替换变量 : {}".format(i))
            result = self.reg(r"\{{%s}}" % i).sub(is_vars.get(i), string)
        log.info("替换结果: {}".format(result))
        return result

    def __call__(self, exp, string):
        if is_json_str(string):
            return self.reg(r'\"%s":"(.*?)"' % exp).findall(string)
        return self.reg(r'%s' % exp).findall(string)[0]
    def getvalue(self,exp,string,num=0,is_all=False):
        try:
            self.data = json.loads(string)  # json转成字典
        except Exception as e:
            print('这里报错了%s'%e)
            self.data = string
        if is_all == True:
            data = jsonpath.jsonpath(self.data, '$..{}'.format(exp))
        else:
            data = jsonpath.jsonpath(self.data, '$..{}'.format(exp))
            data = data[num]  #这里报错一般就是响应没有提取值
        return data
regs = RegExp()


if __name__ == '__main__':
    # a= {"code":1,"msg":"","data":{"userId":1,"entityId":0,"username":"manager","nickname":"管理员","phone":"13575766869","companyName":"安全号","createTime":"2020-05-08 15:36:06","updateTime":"2020-05-08 15:36:06","status":1}}
    # print(regs.getvalue('data',a))
    print(regs.subs(['{{data}}'],'{"data": {"userId": "{{data}}"}}'))
