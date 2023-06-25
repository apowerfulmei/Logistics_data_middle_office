from typing import List
from pydantic import BaseModel
import uuid

class abnmsg() :

    def __init__(self,Msg,Err,Data_type):
        self.message=Msg
        #生成的id的最后一位为data_type
        newid=uuid.uuid1().__str__()+str(Data_type)
        self.id=newid
        self.error=Err

class abnmsg_in(BaseModel):
    messages:list

class eid_in(BaseModel):
    ids:list

#返回信息模型，包括成功存储数据数量，异常数据数量，异常数据列表
class abnmsg_out(BaseModel):
    accept_num: int         #成功存储数据
    deny_num: int           #异常数据
    messages: list          #存储物流公司信息的列表


# a=time()
# for i in range(10000):
#     uuid.uuid1()
# b=time()
# print(b-a)