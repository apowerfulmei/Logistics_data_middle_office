from dmdb import mydb
from dmdb.mydb import db
from models import ctndynamic
import pandas as pd


dbname="datas.ctndynamic"     #数据库名



def fetch_data(option=1):
    #获取ctndynamic数据库中的数据
    #option表示是否需要转化为对象，1表示需要，0不需要，默认为1
    data=[]
    db.execute('select * from %s' % dbname)
    back= db.fetchall()
    if option==0 :
        return back
    #将数据库数据以ctndmsg对象列表返回
    for item in back:
        cus = ctndynamic.ctndmsg(item[0],item[1],item[2],item[3],item[4],item[5],item[6])
        data.append(cus)
    return data

def store_data(data):
    #储存数据
    #转化为元组
    tuples = [tuple(x) for x in data.values]
    #批量存储速度远远快于逐个存储
    # for i in tuples:
    #     db.execute("insert into %s values(?,?,?,?,?,?,?) "%dbname,i)
    db.executemany("insert into %s values(?,?,?,?,?,?,?) "%dbname,tuples)



current=0           #当前数据
total=0             #总共数据量
alldata=pd.DataFrame
def already_exist(row,number_to_check=0) :
    #判断数据是否已经存在
    #传入的数据格式为pandas series类型
    #集装箱动态信息检查提单号、操作与集装箱号
    #number_to_check为此次需要检查的数据数量
    #提前提取出所有信息
    # global current,total,alldata
    # if number_to_check!=0 and current==0 :
    #     total=number_to_check
    #     alldata=pd.DataFrame(data=fetch_data(0),columns=ctndynamic.ctnd_dict.values())
    # current+=1
    # if current==total:
    #     #解析完毕
    #     current=0
    #     total=0
    # if ((alldata['order_id'] ==row['order_id']) & (alldata['operation'] == row['operation'])  & (alldata['ctn_id'] == row['ctn_id'])).any() :
    #     return True
    # else :
    #     return False

    db.execute('select * from %s where "order_id"= \'%s\' and "operation"=\'%s\' and "ctn_id"=\'%s\''% (dbname,row['order_id'],row['operation'],row['ctn_id']))
    data = db.fetchall()
    if len(data)==0 :
        return False
    else :
        return True