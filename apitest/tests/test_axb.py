import pytest
import allure


from apitest.core.checkreult import check_results
from apitest.core.request import req
from common.sign import *
from common.variable import is_vars


@allure.feature("单个API测试")
class TestStandAlone:
    # #ids 状态变换
    # def init_data(fixture_value):
    #     if fixture_value == 10:
    #         return "untreated"
    #     elif fixture_value == 20:
    #         return "processing"
    #     elif fixture_value == 30:
    #         return "done"
    @pytest.mark.parametrize('case',
                             [testinfo.stand_alone],
                             ids=['登录'])
    @pytest.mark.skip(reason="no way of currently testing this")
    @pytest.mark.parametrize('case',
                             testinfo.business.values(),
                             ids=testinfo.business.keys())
    def test_business_interface(self, case):
        r = req(
            case['method'],
            case['route'],
            case.get('extractresult'),
            **case['RequestData'])
        check_results(r, case)

    @allure.feature("AXB绑定")
    @pytest.mark.parametrize(
        'case', (wwtest.sign_in_file(
            testinfo.business_path, axb_dict, replace_dict), wwtest.sign_in_file(
            testinfo.business_path, axb_dict, wwtest.ww_update(
                replace_dict, {
                    'telA': fake.phone_number(), 'telX': '15805805920'}))), ids=[
                        '随机x号码绑定', '指定X号码绑定'])
    def test_business_interface(self, case):
        r = req(
            case['method'],
            case['route'],
            case.get('extractresult'),
            **case['RequestData'])
        check_results(r, case)
        bind = is_vars.get('bindId')
        wwredis.red_set("bindId", bind)
        log.info('bind%s' % bind)

    @allure.feature("AXB解绑")
    @pytest.mark.parametrize('case',
                             [wwtest.sign_in_file(testinfo.axb_unbind_path,
                                                  unbind_dict,
                                                  re_nonum_dict,
                                                  "bindId",
                                                  wwredis.red_get('bindId')
                                                  )],
                             ids=["axb解绑"])
    def test_axb_unbind(self, case):
        r = req(
            case['method'],
            case['route'],
            case.get('extractresult'),
            **case['RequestData'])
        check_results(r, case)


if __name__ == "__main__":

    pytest.main(['test_axb.py'])
