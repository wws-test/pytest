import pytest
import allure

from apitest.core.checkreult import check_results
from apitest.core.request import req
from common.ApiData import testinfo
from common.sign import wwtest, axb_dict


@allure.feature("单个API测试")
class TestStandAlone:

    @pytest.mark.parametrize('case', testinfo.stand_alone.values(), ids=testinfo.stand_alone.keys())
    def test_stand_alone_interface(self, case):
        r = req(case['method'], case['route'], case.get('extractresult'), **case['RequestData'])
        check_results(r, case)
        print(r.cookies)

    @allure.feature("AXB绑定")
    @pytest.mark.parametrize('case', wwtest.in_file(axb_dict).values(), ids=testinfo.business.keys())
    def test_business_interface(self, is_login, case):
        r = req(case['method'], case['route'], case.get('extractresult'), **case['RequestData'])
        check_results(r, case)
    @allure.feature("AXB解绑")
    @pytest.mark.parametrize('case', wwtest.in_file(axb_dict).values(), ids=testinfo.business.keys())
    def test_business_interface(self, is_login, case):
        r = req(case['method'], case['route'], case.get('extractresult'), **case['RequestData'])
        check_results(r, case)


if __name__ == "__main__":
    pytest.main(['test1.py'])
