import os
from string import Template

import yaml


from config.conf import DATA_DIR


class ApiInfo:

    def __init__(self):
        self.base_info_path = os.path.join(DATA_DIR, 'testinfo.yaml')
        self.business_path = os.path.join(DATA_DIR, 'BusinessInterface.yaml')
        self.stand_alone_path = os.path.join(DATA_DIR, 'stand_alone_interface.yaml')
        self.axb_unbind_path = os.path.join(DATA_DIR, 'axb_unbind.yaml')
    @classmethod
    def load(cls, path):
        with open(path, encoding='utf-8') as f:
            return yaml.safe_load(f)

    @property
    def info(self):
        return self.load(self.base_info_path)

    @property
    def business(self):
        return self.load(self.business_path)
    @property
    def unbind(self):
        return self.load(self.axb_unbind_path)

    @property
    def stand_alone(self):
        return self.load(self.stand_alone_path)

    def test_info(self, value):
        """测试信息"""
        return self.info['test_info'][value]

    def login_info(self, value):
        """登录信息"""
        return self.stand_alone['登录'].get(value)

    def business_info(self, name):
        """用例信息"""
        return self.business[name]

    def stand_info(self, name):
        """单个接口"""
        return self.stand_alone[name]

    def yaml_template(self, path, data: dict):
        '''yaml模板字符串替换'''
        with open(path, encoding="utf-8") as f:
            re = Template(f.read()).substitute(data)
            return yaml.safe_load(re)

testinfo = ApiInfo()


if __name__ == '__main__':
    dict1 = {'sign': '497fca80',
             'timestamp': "str1",
             'requestId': "uuid1"}
    print(testinfo.business['登录']['RequestData']['data'])

