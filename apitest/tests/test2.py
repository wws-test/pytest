#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import pytest
import allure
#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import pytest
import allure

from apitest.core.checkreult import check_results
from apitest.core.request import req
from common.ApiData import testinfo



@allure.feature("业务流程API测试")
class TestBusiness:
    @pytest.mark.parametrize('case', testinfo.business.values(), ids=testinfo.business.keys())
    def test_business_interface(self, case):
        r = req(case['method'], case['route'], case.get('extractresult'), **case['RequestData'])
        check_results(r, case)


if __name__ == "__main__":
    pytest.main(['test_business.py'])
