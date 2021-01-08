a = {'method': 'post', 'route': '/ann/login', 'RequestData': {'data': {'username': 'cus', 'password': 123456, 'rememberMe': False, 'verificationCode': False}}, 'expectcode': 200, 'resultcheck': '"code":1'}

for kv in a.items():
       print(kv)