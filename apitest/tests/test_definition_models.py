#!/usr/bin/env python3
# -*- coding:utf-8 -*-
#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from common.variable import is_vars
import pytest
import allure
from faker import Faker
from apitest.core.checkreult import check_results, check_code, check_message
from apitest.core.request import req
fake = Faker()


@allure.feature("models模型测试")
class Test_models:

    @allure.story("2.1创建模型")
    def test_get_deploy(self):
        json = {'modelId':'ww'}
        result = req("POST", '/workflow/model/deploy', ['id'], data=json)
        check_code(result, 200)
        check_message(result, '服务器内部错误')
        # reuslt = json | grep("mike*", use_regexp=True)  diff 判断接口细粒度变化

    @allure.story("2.2查询所有流程模型")
    def test_get_models(self):
        result = req(
            "GET",
            '/workflow/model/rest/models',
            ['key'])
        check_code(result, 200)
        check_message(result, '操作成功')
        list=result.json()['result']
        #把list放入全局变量
        is_vars.set('list',list)

    @allure.story("2.3查询模型相关联的模型")
    def test_get_rest_model(self):
        a=is_vars.get('list')[1]
        json = {'modelKey': a['key'], 'modelType': 0}
        result = req("GET", '/workflow/model/rest/model', ['id'], params=json)
        check_code(result, 200)
        check_message(result, '操作成功')
        # reuslt = json | grep("mike*", use_regexp=True)  diff 判断接口细粒度变化

    @allure.story("2.4流程模型打印(图片的字节流数据)")
    def test_get_resourceRead(self):
        a=is_vars.get('list')[1]
        json = {'processDefinitionKey': a['key']}
        result = req("GET", '/workflow/model/resourceRead', '', params=json)
        check_code(result, 200)
        with open(r'D:\\new1.png', 'wb') as f:
            if result.status_code == 200:
                for chunk in result.iter_content(
                        chunk_size=1):  # todo iter_content循环读取信息写入，chunk_size设置文件大小
                    f.write(chunk)
        # reuslt = json | grep("mike*", use_regexp=True)  diff 判断接口细粒度变化

    @allure.story("2.4模型xml下载")
    def test_get_downloadXml(self):
        a=is_vars.get('list')[1]
        json = {'processDefinitionKey': a['key']}
        result = req(
            "GET",
            '/workflow/model/resource/downloadXml',
            '',
            params=json)
        check_code(result, 200)
        with open(r'D:\\new.xml', 'wb') as f:
            if result.status_code == 200:
                for chunk in result.iter_content(
                        chunk_size=1):  # 
                    f.write(chunk)
        # reuslt = json | grep("mike*", use_regexp=True)  diff 判断接口细粒度变化


if __name__ == "__main__":
    pytest.main(['test_business.py'])
