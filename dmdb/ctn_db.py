from dmdb.mydb import db
from models import others

dbname="datas.container"

def fetch_data(order_id):
    #获取数据
    data=[]
    back=db.execute('select ctn_id from %s where "order_id"=\'%s\'' % (dbname,order_id))
    for item in back:
        data.append(item[0])
    #print(data)
    return others.container(data)



def store_data(data_ctn):
    #存储数据
    #传入参数：data_ctn为dataframe格式，只包含order_id与containers两列
    #字符串切割
    tuples=[]
    for item in data_ctn.itertuples():
        ctn_ids=others.split_ctn_str(item[2])
        for id in ctn_ids:
            tuples.append(tuple([item[1],id]))
    db.executemany("insert into %s values(?,?) " % dbname, tuples)


