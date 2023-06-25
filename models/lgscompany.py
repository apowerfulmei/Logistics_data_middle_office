#与获取物流公司信息api相关的数据模型

from typing import List
from pydantic import BaseModel
import pandas as pd

class lgscomsg:

    def __init__(self,
                 Company="",              #物流公司名
                 Account="",              #客户
                 Contact="",              #联系人
                 Phone="",                #电话
                 Location="",             #省市
                 Dict=pd.Series
                 ):
        if Dict.empty==False :
            self.company=Dict['company']
            self.account=Dict['account']
            self.contact=Dict['contact']
            self.phone=Dict['phone']
            self.location=Dict['location']
        else :
            self.company=Company
            self.account=Account
            self.contack=Contact
            self.phone=Phone
            self.location=Location

#返回信息模型，包括数量以及物流公司信息list
class lgscomsg_out(BaseModel):
    number: int           #物流信息数量
    messages: list        #存储物流公司信息的列表



lgsco_dict={
          "公司名称":'company',
          "客户编号":'account',
          "联系人":"contact",
          "电话":'phone',
          "省市区":'location'}