from dmdb import mydb,ctn_db,trans_db
from dmdb.mydb import db
from models import logistics
import pandas as pd


dbname="datas.logistics"     #数据库名



def fetch_data(option=1):
    #获取logistics数据库中的数据
    data=[]
    db.execute('select * from %s' % dbname)
    back = db.fetchall()
    #print(back)
    if option==0 :
        return back
    #将数据库数据以lgsmsg对象列表返回
    for item in back:
        cus = logistics.lgsmsg(item[0],item[1],item[2],item[3],
                               ctn_db.fetch_data(item[0]),
                               item[4],item[5])
        data.append(cus)
    return data

def store_data(data):
    #储存数据
    #data为pandas dataframe数据
    data_lgs=data.iloc[:,[0,1,2,3,5,6]]       #保存在logistics数据库中的数据
    data_ctn=data.iloc[:,[0,4]]               #保存在containers数据库中的数据
    tuples = [tuple(x) for x in data_lgs.values]
    #批量存储
    db.executemany("insert into %s values(?,?,?,?,?,?) "%dbname,tuples)
    #存储集装箱编号与提单号的对应关系
    ctn_db.store_data(data_ctn)

current=0           #当前数据
total=0             #总共数据量
alldata=pd.DataFrame
def already_exist(row,number_to_check=0) :
    #判断数据是否已经存在
    #传入的数据格式为pandas series类型
    #物流信息检查提单号
    # global current,total,alldata
    # if number_to_check!=0 and current==0 :
    #     total=number_to_check
    #     x=list(logistics.lgs_dict.values())
    #     x.pop(4)
    #     print("aaa",x)
    #     alldata=pd.DataFrame(data=fetch_data(0),columns=x)
    # current+=1
    # if current==total:
    #     #解析完毕
    #     current=0
    #     total=0
    # if ((alldata['order_id'] ==row['order_id']) ).any() :
    #     return True
    # else :
    #     return False
    db.execute('select * from %s where "order_id"= \'%s\'' % (dbname,row['order_id']))
    data = db.fetchall()
    if len(data)==0 :
        return False
    else :
        return True