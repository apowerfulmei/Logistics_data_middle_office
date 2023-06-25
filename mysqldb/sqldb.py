#mysql操作
import pymysql



def dbconnect(host,port,dbname,user,passwd):
    #数据库连接
    conn=pymysql.connect(
            host=host,
            port=port,
            db=dbname,
            user=user,
            password=passwd
    )
    cur=conn.cursor()
    return cur

def fetch_data(tbname,cur):
    #获取数据
    data=[]
    if cur==None :
        print("数据库连接错误")
    else :
        cur.execute("select * from %s"%(tbname))
        data=cur.fetchall()
        print(data)
    return data

# cur=dbconnect('127.0.0.1',3306,'testdb','root','123456')
# fetch_data('user',cur)