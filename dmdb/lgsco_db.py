from dmdb import mydb
from dmdb.mydb import db
from models import lgscompany


dbname="datas.lgscompany"     #数据库名



def fetch_data(option=1):
    #获取lgscompany数据库中的数据
    data=[]
    db.execute('select * from %s' % dbname)
    back = db.fetchall()
    if option==0 :
        return back
    #将数据库数据以lgscomsg对象列表返回
    for item in back:
        cus = lgscompany.lgscomsg(item[0],item[1],item[2],item[3],item[4])
        data.append(cus)
    return data

def store_data(data):
    #获取字典与文件数据
    #储存数据
    #转化为元组
    tuples = [tuple(x) for x in data.values]
    #批量存储
    db.executemany("insert into %s values(?,?,?,?,?) "%dbname,tuples)

def already_exist(row) :
    #判断数据是否已经存在
    #传入的数据格式为pandas series类型
    #物流公司信息检查公司名
    db.execute('select * from %s where "company"= \'%s\'' % (dbname,row['company']))
    data = db.fetchall()
    if len(data)==0 :
        return False
    else :
        return True