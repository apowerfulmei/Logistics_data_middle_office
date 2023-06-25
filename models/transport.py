from typing import List
from pydantic import BaseModel
from models import others
import pandas as pd

class transmsg:
    def __init__(self,
                 Ship_company="",                    #船公司名
                 Ship="",                            #船名
                 Task_begin="",                      #作业开始时间
                 Task_end="",                        #作业结束时间
                 Trans_begin="",                     #运输开始时间
                 Trans_end="",                       #运输结束时间
                 Port="",                            #港口
                 Order_id="",                        #订单号
                 Containers=others.container,        #集装箱
                 Size=0,                             #箱尺寸（TEU）
                 Src="",                             #启运地
                 Dst="",                             #目的地
                 Dict=pd.Series                            #pandas series类型数据
                 ):
        if Dict.empty==False :
            self.ship_company=Dict['ship_company']
            self.ship=Dict['ship']
            self.task_begin=Dict['task_begin']
            self.task_end=Dict['task_end']
            self.trans_begin=Dict['trans_begin']
            self.trans_end=Dict['trans_end']
            self.port=Dict['port']
            self.order_id=Dict['order_id']
            self.containers=self.containers=Dict['containers']              #others.container(others.split_ctn_str(Dict['containers']))
            self.size=Dict['size']
            self.src=Dict['src']
            self.dst=Dict['dst']
        else :
            self.ship_company=Ship_company
            self.ship=Ship
            self.task_begin=Task_begin
            self.task_end=Task_end
            self.trans_begin=Trans_begin
            self.trans_end=Trans_end
            self.port=Port
            self.order_id=Order_id
            self.containers=Containers.join_str()
            self.size=Size
            self.src=Src
            self.dst=Dst



#返回信息模型，包括数量以及货物操作信息list
class transmsg_out(BaseModel):
    number: int           #货物操作信息数量
    messages: list        #存储货物操作信息的列表



trans_dict={"船公司":"ship_company",
            "船名称":'ship',
            "作业开始时间":'task_begin',
            "作业结束时间":'task_end',
            "始发时间":'trans_begin',
            "到达时间":'trans_end',
            "作业港口":'port',
            "提单号":'order_id',
            "集装箱箱号":'containers',
            "箱尺寸（TEU）":'size',
            "启运地":'src',
            "目的地":'dst'}
