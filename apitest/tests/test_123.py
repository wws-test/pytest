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
if __name__ == '__main__':
    pass