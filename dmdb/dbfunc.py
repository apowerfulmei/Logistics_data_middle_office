
from . import cus_db,lgs_db,lgsco_db,ctnd_db,trans_db
def store_data(data,data_type) :
    #存储数据
    #data pandas dataframe
    #data_type数据类型
    if(data_type==1):
        #cus_db
        cus_db.store_data(data)
    elif(data_type==2):
        #lgs_db
        lgs_db.store_data(data)
    elif(data_type==3 or data_type==4):
        #trans_db
        trans_db.store_data(data,data_type-3)
    elif(data_type==5):
        #lgsco_db
        lgsco_db.store_data(data)
    elif(data_type==6):
        #ctnd_db
        ctnd_db.store_data(data)
