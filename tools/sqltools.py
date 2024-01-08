
import os

import pymysql

from apitest.common.ApiData import testinfo
from apitest.common.Redis import wwredis
from apitest.config.conf import DATA_DIR, BASE_DIR
from apitest.tools.logger import log

data_file_path = os.path.join(BASE_DIR, "config", "config.ini")
data = testinfo.load_ini(data_file_path)["mysql"]

DB_CONF = {
    "host": wwredis.red_get('ip'),
    "port": int(data["MYSQL_PORT"]),
    "user": data["MYSQL_USER"],
    "password": data["MYSQL_PASSWD"],
    "db": data["MYSQL_DB"]
}


class MysqlDb():

    def __init__(self, db_conf=DB_CONF):
        # 通过字典拆包传递配置信息，建立数据库连接
        self.conn = pymysql.connect(**db_conf, autocommit=True)
        # 通过 cursor() 创建游标对象，并让查询结果以字典格式输出
        self.cur = self.conn.cursor(cursor=pymysql.cursors.DictCursor)

    # def __del__(self):  # 对象资源被释放时触发，在对象即将被删除时的最后操作
    #     # 关闭游标
    #     self.cur.close()
    #     # 关闭数据库连接
    #     self.conn.close()

    def select_db(self, sql):
        """查询"""
        # 检查连接是否断开，如果断开就进行重连
        self.conn.ping(reconnect=True)
        # 使用 execute() 执行sql
        self.cur.execute(sql)
        # 使用 fetchall() 获取查询结果
        data = self.cur.fetchall()
        return data

    def execute_db(self, sql):
        """更新/新增/删除"""
        try:
            # 检查连接是否断开，如果断开就进行重连
            self.conn.ping(reconnect=True)
            # 使用 execute() 执行sql
            self.cur.execute(sql)
            # 提交事务
            self.conn.commit()
        except Exception as e:
            log.info("操作MySQL出现错误，错误原因：{}".format(e))
            # 回滚所有更改
            self.conn.rollback()


db = MysqlDb(DB_CONF)

if __name__ == '__main__':
    print(db.select_db('SELECT enterprise_id FROM `db_system_info`WHERE enterprise_name = "备案单位2021-07-13-17_40"')[0]['enterprise_id'])
