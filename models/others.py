from pydantic import BaseModel


class container:
    #集装箱类
    def __init__(self,
                 Ctn_id=[]      #集装箱号
    ):
        self.number=len(Ctn_id)
        self.ctn_id=Ctn_id

    def join_str(self):
        return ','.join(self.ctn_id)

def split_ctn_str(ctn_ids:str) :
    #用于切割ctn_id字符串
    ctn_id = ctn_ids.split(',')
    return ctn_id

