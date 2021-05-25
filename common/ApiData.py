import json
import os
from string import Template
import yaml
from configparser import ConfigParser

from common.Redis import wwredis
from config.conf import DATA_DIR, INI_PATH, WORKFLOW
from tools.logger import log
from typing import Tuple, Dict, Union, Text, List, Callable


class MyConfigParser(ConfigParser):
    # 重写 configparser 中的 optionxform 函数，解决 .ini 文件中的 键option 自动转为小写的问题
    def __init__(self, defaults=None):
        ConfigParser.__init__(self, defaults=defaults)

    def optionxform(self, optionstr):
        return optionstr


class ApiInfo:

    def __init__(self):
        self.base_info_path = os.path.join(DATA_DIR, 'testinfo.yaml')
        self.business_path = os.path.join(DATA_DIR, 'BusinessInterface.yaml')
        self.stand_alone_path = os.path.join(
            DATA_DIR, 'stand_alone_interface.yaml')
        self.axb_unbind_path = os.path.join(DATA_DIR, 'axb_unbind.yaml')
        self.base_login = os.path.join(DATA_DIR, 'basics_login.yaml')
        self.check_create = os.path.join(DATA_DIR, 'basics_check_create.yaml')
        self.get_start=os.path.join(WORKFLOW, 'form_getstart.yaml')
        self.get_3150 = os.path.join(DATA_DIR, '3150_info.yaml')

    @classmethod
    def load(cls, file_path: Text) -> Dict:
        with open(file_path, encoding='utf-8') as f:
            try:
                data = yaml.safe_load(f)
            except yaml.YAMLError as ex:
                err_msg = f"YAMLError:\nfile: {file_path}\nerror: {ex}"
                log.info(err_msg)
        # log.info("读到数据 ==>>  {} ".format(data))
        return data

    @classmethod
    def load_json(self, file_path):
        with open(file_path, encoding='utf-8') as f:
            data = json.load(f)
        log.info("读到数据 ==>>  {} ".format(data))
        return data

    @classmethod
    def load_ini(self, file_path):
        config = MyConfigParser()
        config.read(file_path, encoding="UTF-8")
        data = dict(config._sections)
        # print("读到数据 ==>>  {} ".format(data))
        return data

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
    #
    # def business_info(self, name):
    #     """用例信息"""
    #     return self.business[name]
    #
    # def stand_info(self, name):
    #     """单个接口"""
    #     return self.stand_alone[name]

    def yaml_template(self, path, data: dict):
        '''yaml模板字符串替换'''
        with open(path, encoding="utf-8") as f:
            re = Template(f.read()).substitute(data)
            return yaml.safe_load(re)

    # 去除字符串替换过程中过的none问题
    def dict_clean(self, dict):

        r = json.dumps(dict).replace('null', '""')

        tmp = json.loads(r)
        return tmp



testinfo = ApiInfo()


if __name__ == '__main__':
    pass
