#与获取客户信息api相关的数据模型

from typing import List
from pydantic import BaseModel
import pandas as pd
#单体基本信息
class cusmsg():
    #姓名        cus_name: str
    #身份证号    cus_id: str
    #电话号码    phone: str
    #地区       location: str
    def __init__(self,
                 Cus_name="",
                 Cus_id="",
                 Phone="",
                 Location="",
                 Dict=pd.Series           #pandas series类
                 ):
        if Dict.empty==False :
            self.cus_name=Dict['cus_name']
            self.cus_id=Dict['cus_id']
            self.phone=Dict['phone']
            self.location=Dict['location']
        else :
            self.cus_name=Cus_name
            self.cus_id=Cus_id
            self.phone=Phone
            self.location=Location




#返回信息模型，包括数量以及用户信息list
class cusmsg_out(BaseModel):
    number: int           #用户信息数量
    messages: list        #存储用户信息的列表




cus_dict={
          "客户名称":'cus_name',
          "客户编号":'cus_id',
          "手机号":'phone',
          "省市区":'location'}