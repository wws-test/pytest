import pytest
import allure

from apitest.core.checkreult import check_results
from apitest.core.request import req
from common.Redis import wwredis
from common.sign import *
from common.variable import is_vars

global bind
@allure.feature("单个API测试")
class TestStandAlone:

    @pytest.mark.parametrize('case',
                             testinfo.stand_alone.values(),
                             ids=testinfo.stand_alone.keys())
    @pytest.mark.skip(reason="no way of currently testing this")
    def test_stand_alone_interface(self, case):
        r = req(
            case['method'],
            case['route'],
            case.get('extractresult'),
            **case['RequestData'])
        check_results(r, case)
        print(r.cookies)

    @allure.feature("AXB绑定")
    @pytest.mark.parametrize('case',
                             wwtest.in_file(testinfo.business_path,
                                            axb_dict,
                                            replace_dict).values(),
                             ids=testinfo.business.keys())
    def test_business_interface(self, case ):
        global bind
        r = req(
            case['method'],
            case['route'],
            case.get('extractresult'),
            **case['RequestData'])
        check_results(r, case)
        bind = is_vars.get('bindId')
        wwredis.red_set("bindId",bind)
        log.info('bind%s'%bind)

    @allure.feature("AXB解绑")
    @pytest.mark.parametrize('case',
                             wwtest.in_file(testinfo.axb_unbind_path,
                                            unbind_dict,
                                            re_nonum_dict,
                                            "bindId",
                                            wwredis.red_get('bindId')
                                            ).values(),
                             ids=testinfo.unbind.keys())
    def test_axb_unbind(self, case):
        r = req(
            case['method'],
            case['route'],
            case.get('extractresult'),
            **case['RequestData'])
        check_results(r, case)
        log.info('传递bind%s'%bind)


if __name__ == "__main__":
    pytest.main(['test1.py'])
