from common.Redis import wwredis


class MetaSingleton(type):
    def __call__(cls, *args, **kwargs):
        print("cls:{}".format(cls.__name__))
        print("====1====")
        if not hasattr(cls, "_instance"):
            print("====2====")
            cls._instance = type.__call__(cls, *args, **kwargs)
        return cls._instance

class User(metaclass=MetaSingleton):
    def __init__(self, *args, **kw):
        print("====3====")
        for k,v in kw:
            setattr(self, k, v)
def test_www():
    id = wwredis.red_get('id')
    js = {
        "processDefinitionId": id,
        "businessKey": "",
        "businessType": "",
        "businessName": "",
        "tenantId": "",
        "formData": {"username": "task"}
    }
    tmp = str(js)

if __name__ == '__main__':
    print(test_www())