import os
import configparser
from config.conf import INI_PATH

HOST = 'HOST'
BD = 'BD'
HOSS = 'HOSS'
USER = 'USER'
PASSWD = 'PASSWD'

PEUSER = 'PEUSER'
PEPASSWD = 'PEPASSWD'

BDUSER = 'BDUSER'
BDPASSWD = 'BDPASSWD'


class ReadConfig:
    """配置文件"""

    def __init__(self):
        if not os.path.exists(INI_PATH):
            raise FileNotFoundError("配置文件%s不存在！" % INI_PATH)
        self.config = configparser.RawConfigParser()  # 当有%的符号时请使用Raw读取
        self.config.read(INI_PATH, encoding='utf-8')

    def _get(self, section, option):
        """获取"""
        return self.config.get(section, option)

    def _set(self, section, option, value):
        """更新"""
        self.config.set(section, option, value)
        with open(INI_PATH, 'w') as f:
            self.config.write(f)

    @property
    def url(self):
        return self._get(HOST, HOST)

    @property
    def bdurl(self):
        return self._get(HOST, BD)

    @property
    def peurl(self):
        return self._get(HOST, HOSS)

    @property
    def account(self):
        return self._get(USER, USER)

    @property
    def passwd(self):
        return self._get(USER, PASSWD)

    @property
    def peaccount(self):
        return self._get(USER, PEUSER)

    @property
    def pepasswd(self):
        return self._get(USER, PEPASSWD)

    @property
    def bdaccount(self):
        return self._get(USER, BDUSER)

    @property
    def bdpasswd(self):
        return self._get(USER, BDPASSWD)


ini = ReadConfig()

if __name__ == '__main__':
    print(ini.url)
    print(ini.bdaccount)
    print(ini.bdpasswd)
