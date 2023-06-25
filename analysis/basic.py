#通用分析
from dmdb import trans_db,lgs_db
from time import time
def get_port_goods() :
    #获取所有港口名称
    portname=[]
    goodsname=[]
    tran_out=trans_db.fetch_data(0)
    tran_in=trans_db.fetch_data(1)
    lgs=lgs_db.fetch_data()
    a=time()
    for item in tran_out :
        portname.append(item.port)
    for item in tran_in :
        portname.append(item.port)
    for item in lgs:
        goodsname.append(item.goods)
    portname=list(set(portname))
    goodsname=list(set(goodsname))
    b=time()
    print("set：",b-a)
    # print(portname)
    # print(goodsname)
    return {"ports":portname,"goods":goodsname}


def get_allgoods() :
    #获取所有货物名称
    pass



