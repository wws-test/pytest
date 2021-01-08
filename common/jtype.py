import jpype
import os

jvmPath = jpype.getDefaultJVMPath()
#找到jar包
jarpath = os.path.join(os.path.abspath("."), "C:\\Users\\Administrator\\Desktop\\test.jar")
# 开启jvm
jpype.startJVM(jvmPath, "-ea", "-Djava.class.path=%s" % (jarpath))

# 找到class
javaClass = jpype.JClass("test1.test1")
#实例化
javaClass=javaClass()
#

def sign(rawSting,secret):
    '''参数加密'''
    result = (javaClass.sign(rawSting,secret))
    return result
    jpype.shutdownJVM()
def rawString(dict):
    '''参数加密'''
    result = (javaClass.rawString(dict))
    return result
    jpype.shutdownJVM()

if __name__ == '__main__':
    dict1 = {'key': 'aa049341',
             'timestamp': '20210107142207',
             'requestId': '34470cb1-5b47-4e67-a99c-6faf2defb6f0',
             'telA': '14747635722',
             'telB': '16188015753',
             'telX': '',
             'areaCode': '',
             'anuCode': '',
             'expiration': '300',
             'callRecording': '1',
             'callDisplay': '1',
             'callRestrict': '1'
             }
    print(rawString(dict1))
