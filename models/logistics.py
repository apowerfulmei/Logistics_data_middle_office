#与获取物流信息api相关的数据模型

from typing import List
from pydantic import BaseModel
from models import others
import pandas as pd



class lgsmsg:
    #物流信息类
    def __init__(self,
                 Order_id="",                  #订单号
                 Cus_name="",                  #用户名
                 Cus_id="",                    #用户身份证号
                 Company="",                   #公司名
                 Containers=others.container,  #集装箱
                 Goods="",                     #货物名
                 Weight=0,                     #重量（吨）
                 Dict=pd.Series
                 ):
        if Dict.empty==False :
            #print(Dict)
            self.order_id=Dict['order_id']
            self.cus_name=Dict['cus_name']
            self.cus_id=Dict['cus_id']
            self.company=Dict['company']
            self.containers=Dict['containers']             #others.container(others.split_ctn_str(Dict['containers']))
            self.goods=Dict['goods']
            self.weight=Dict['weight']
        else :
            self.order_id=Order_id
            self.cus_name=Cus_name
            self.cus_id=Cus_id
            self.company=Company
            self.containers=Containers.join_str()
            self.goods=Goods
            self.weight=Weight


#返回信息模型，包括数量以及物流信息list
class lgsmsg_out(BaseModel):
    number: int           #物流信息数量
    messages: list        #存储物流信息的列表



lgs_dict={"提单号":'order_id',
          "货主名称":'cus_name',
          "货主代码":'cus_id',
          "物流公司（货代）":'company',
          "集装箱箱号":'containers',
          "货物名称":'goods',
          "货重（吨）":'weight'}