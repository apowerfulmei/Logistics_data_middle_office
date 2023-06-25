#与获取集装箱动态信息相关api的数据模型

from typing import List
from pydantic import BaseModel
import pandas as pd


class ctndmsg:
    def __init__(self,
                 Port="",               #港口
                 Ctn_id="",             #集装箱编号
                 Size=0,                #箱尺寸
                 Order_id="",           #订单号
                 Position="",           #堆场位置
                 Operation="",          #操作（出库、入库）
                 Date="",               #操作日期
                 Dict=pd.Series               #pandas series
                 ):
        if Dict.empty==False :
            self.port=Dict['port']
            self.ctn_id=Dict['ctn_id']
            self.size=Dict['size']
            self.order_id=Dict['order_id']
            self.position=Dict['position']
            self.operation=Dict['operation']
            self.date=Dict['date']
        else :
            self.port=Port
            self.ctn_id=Ctn_id
            self.size=Size
            self.order_id=Order_id
            self.position=Position
            self.operation=Operation
            self.date=Date

#返回信息模型，包括数量以及集装箱动态信息list
class ctndmsg_out(BaseModel):
    number: int           #信息数量
    messages: list        #存储集装箱动态信息的列表




ctnd_dict={"堆存港口":'port',
          "集装箱箱号":'ctn_id',
          "箱尺寸（TEU）":'size',
          "提单号":'order_id',
          "堆场位置":'position',
          "操作":'operation',
          "操作日期":'date'}