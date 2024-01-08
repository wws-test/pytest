import time
import uuid

from faker import Faker

from apitest.common.ApiData import testinfo
from apitest.common.Redis import wwredis
from apitest.common.jtype import sign, rawString
from apitest.common.variable import is_vars
from apitest.tools.logger import Log

log = Log().logger

fake = Faker(locale='zh_CN')
telA = fake.phone_number()
telB = fake.phone_number()
now = int(time.time())     # 1533952277
uuid1 = str(uuid.uuid4())
secret = '0c88966ba913d69a0ae61e6a434cbb292d48825349d44923'
str1 = time.strftime("%Y%m%d%H%M%S", time.localtime(now))

# TODO  实现多模式传值
replace_dict = {
    'key': '7d34ee6f',
    'timestamp': str1,
    'requestId': uuid1,
    'telA': telA,
    'telB': telB,
    'telX': ""}
re_nonum_dict = {'key': '7d34ee6f', 'timestamp': str1, 'requestId': uuid1}
axb_dict = testinfo.business['RequestData']['data']
unbind_dict = testinfo.unbind['RequestData']['data']


class sign_wwtest:
    def __init__(self):
        ...
    def ww_update(self, dict, re_dict):
        dict.update(re_dict)
        return dict

    def make_great(self, names):
        for i in range(len(names)):
            names[i] = names[i] + "="

    def sign_in_file(self, path,dict, re_dict, keyword=None,tran=''):  # 路径 主参数 次要参数  关键字  变量传递
        # self.make_great(list1)
        # list23='&'.join([i[0] + str(i[1]) for i in zip(list1, list2)])
        # 传入设定好的接口参数加密并再传回yaml文件
        try:
            if keyword is not None:
                dict[keyword] = tran
            self.ww_update(dict, re_dict)
            # 字典排序
            list23 = rawString(dict)
            # 生成签名
            sign1 = sign(list23, secret)
            log.info('axb签名====%s' % sign1)
            # 更新的键值对
            dict['sign'] = sign1

            # 把yaml文件里的字段读取成json / dcit clean 去除里面的none字段
            return testinfo.dict_clean(testinfo.yaml_template(path, dict))
        except:
            pass


wwtest = sign_wwtest()

if __name__ == '__main__':
    print(wwtest.sign_in_file(testinfo.axb_unbind_path,
                                            unbind_dict,
                                            re_nonum_dict,
                                            "bindId",
                                            wwredis.red_get('bindId')
                                            ))
    # print('asdrqwe'[::-1])