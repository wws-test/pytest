from pymongo import MongoClient


class Mongo(object):
    """mongodb增删改查的操作"""
    client = MongoClient(host="localhost", port=27017)
    col = client["wwtest"]["test"]

    @classmethod
    def insert(cls, data,flg=True):
        """添加数据"""
        if flg:
            if isinstance(data, dict):  # 插入一条数据
                ret = cls.col.insert_one(data)
                return ret

        elif isinstance(data, list):  # 插入多条数据
            for i in data:
                if not isinstance(i, dict):
                    return "数据格式有误"
            ret = cls.col.insert_many(data)
            return ret
        else:
            return "数据格式为dict或者[{},{}]形式的列表但你传入的是%s," % type(data)

    @classmethod
    def find(cls, data, flg=True):
        """查找数据"""
        try:
            if flg:
                rt = cls.col.find_one(data)  # 查一条数
                return rt
            else:
                rt = cls.col.find(data)  # 查多条数据
                result = []
                for i in rt:
                    result.append(i)
                return result
        except Exception:
            return "查询数据格式有误"

    @classmethod
    def update(cls, org_data, new_data, flg=True): # flg = True  只更新一条
        """更新数据"""
        if flg:
            ret = cls.col.update_one(org_data, {"$set": new_data})  # 之更细一条
            return ret

        else:
            ret = cls.col.update_many(org_data, {"$set": new_data})  # 更新全部数据
            return ret

    @classmethod
    def delete(cls, data, flg=True):
        """删除数据"""
        if flg:
            ret = cls.col.delete_one(data)  # 删除一条
            return ret
        else:
            ret = cls.col.delete_many(data)  # 删除全部
            return ret


if __name__ == '__main__':
    # data=[{"name":"寂寞撕碎了回忆"},{"name":"我们注定擦肩而过"},{"name":"那年夏天那片海"}]
    # ret=MongoHelp.insert(data)

    # print(ret)
    # ret=MongoHelp.find({"name":"平凡的世界"},3)
    # print(ret)
    # ret=MongoHelp.update({"name" : "流血的仕途" },{"name":"我的程序之路"})
    # print(ret)


    ret = Mongo.find('bindId')
    print(ret)