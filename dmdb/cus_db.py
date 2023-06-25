from dmdb import mydb
from dmdb.mydb import db
from models import customer


dbname="datas.customer"     #数据库名



def fetch_data(option=1):
    #获取customer数据库中的数据
    data=[]
    db.execute('select * from %s' % dbname)
    back = db.fetchall()
    if option==0 :
        return back
    #将数据库数据以cusmsg对象列表返回
    for item in back:

        cus = customer.cusmsg(item[0],item[1],item[2],item[3])
        data.append(cus)
    return data

def store_data(data):
    #客户信息储存数据
    #data为pandas dataframe数据
    #转化为元组
    tuples = [tuple(x) for x in data.values]
    #批量存储
    db.executemany("insert into %s values(?,?,?,?) "%dbname,tuples)



def already_exist(row) :
    #判断数据是否已经存在
    #传入的数据格式为pandas series类型
    #客户信息检查身份证
    db.execute('select * from %s where "cus_id"= \'%s\'' % (dbname,row['cus_id']))
    data = db.fetchall()
    if len(data)==0 :
        #print("row already exst", row)
        return False
    else :
        #print("row already exst", row)
        return True




