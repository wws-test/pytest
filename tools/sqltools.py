import pymysql
import pandas as pd

localhost = "192.168.0.200"
user = "root"
pwd = "at#mysql!321"
db1 = "cc_detection"
try:
    cnx = pymysql.connect(localhost, user, pwd, db1, charset='utf8')
except:
    print('连接数据库失败,请检查连接条件')
# 通过 cursor() 创建游标对象，并让查询结果以字典格式输出
cursor = cnx.cursor(cursor=pymysql.cursors.DictCursor)

def execute_sql(sql):

    try:
        cursor.execute(sql)
    except:
        print('查询失败，请检查sql')
    results = cursor.fetchall()
    col = cursor.description

    data = pd.DataFrame(list(results), columns=pd.DataFrame(list(col))[0])

    cnx.close()
    return data

def insert(table_name,insert_dict):
  param='';
  value='';
  if(isinstance(insert_dict,dict)):
    for key in insert_dict.keys():
      param=param+key+","
      value=value+insert_dict[key]+','
    param=param[:-1]
    value=value[:-1]
  sql="insert into %s (%s) values(%s)"%(table_name,param,value)
  cursor.execute(sql)
  id=cursor.lastrowid
  cnx.commit()
  return id

def delete(table_name,where=''):
  if(where!=''):
    str='where'
    for key_value in where.keys():
      value=where[key_value]
      str=str+' '+key_value+'='+value+' '+'and'
    where=str[:-3]
    sql="delete from %s %s"%(table_name,where)
    cursor.execute(sql)
    cnx.commit()
#取得数据库信息
# print(select({'table':'gelixi_help_type','where':{'help_show': '1'}},'type_name,type_id'))
def select(param,fields='*'):
  table=param['table']
  if('where' in param):
    thewhere=param['where']
    if(isinstance (thewhere,dict)):
      keys=thewhere.keys()
      str='where';
      for key_value in keys:
        value=thewhere[key_value]
        str=str+' '+key_value+'='+value+' '+'and'
      where=str[:-3]
  else:
    where=''
  sql="select %s from %s %s"%(fields,table,where)
  cursor.execute(sql)
  result=cursor.fetchall()
  return result

if __name__ == '__main__':
    sql = 'SELECT  * FROM qc_rule_info WHERE name= "wss"'
    data = execute_sql(sql)
    print(data)