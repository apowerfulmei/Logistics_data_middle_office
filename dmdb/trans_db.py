from dmdb import mydb,ctn_db,lgs_db
from dmdb.mydb import db
from models import transport
import time

dbname=["datas.transport_out","datas.transport_in"]     #数据库名



def fetch_data(type:int,option=1):
    #获取transport数据库中的数据
    a=time.time()
    data=[]
    db.execute('select * from %s' % dbname[type])
    back = db.fetchall()
    b=time.time()
    print("数据库操作：",b-a)
    #将数据直接以列表的形式返回
    if option==0 :
        return back
    #将数据库数据以transmsg对象列表返回
    for item in back:
        cus = transport.transmsg(item[0],item[1],item[2],item[3],item[4],item[5],item[6],item[7],
                                 ctn_db.fetch_data(item[7]),
                                 item[8],item[9],item[10])
        data.append(cus)
    c=time.time()
    print("转化操作：",c-b)
    return data

def store_data(data,type):
    #获取字典与文件数据，type代表信息类型，0为装货信息，1为卸货信息
    #储存数据
    #转化为元组
    data_trans=data.iloc[:,[0,1,2,3,4,5,6,7,9,10,11]]
    tuples = [tuple(x) for x in data_trans.values]
    #批量存储
    db.executemany("insert into %s values(?,?,?,?,?,?,?,?,?,?,?) "%(dbname[type]),tuples)


def already_exist(row,type:int) :
    #判断数据是否已经存在
    #传入的数据格式为pandas series类型
    #type为0，检查装货信息，type为1，检查卸货信息
    #装卸货信息检查港口、提单
    db.execute('select * from %s where "order_id"= \'%s\' and "port"=\'%s\'' % (dbname[type],row['order_id'],row['port']))
    data = db.fetchall()
    if len(data)==0 :
        return False
    else :
        return True