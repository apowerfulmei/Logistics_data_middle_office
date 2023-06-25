#文件转化与读取模块

import pandas as pd
import io
from models import lgscompany,logistics,customer,ctndynamic,transport

class filereader() :
    #读取文件
    myfile=io.FileIO
    file_type=0
    data_type=0
    dict=[]
    transfunc=[]
    def __init__(self):
        self.myfile=io.BytesIO
        self.transfunc.append(self.read_excel)
        self.transfunc.append(self.read_txt)
        self.transfunc.append(self.read_csv)
        self.dict.append(customer.cus_dict)
        self.dict.append(logistics.lgs_dict)
        self.dict.append(transport.trans_dict)
        self.dict.append(transport.trans_dict)
        self.dict.append(lgscompany.lgsco_dict)
        self.dict.append(ctndynamic.ctnd_dict)
        pass

    def get_file_read(self, file, file_type,data_type):
        self.myfile=io.BytesIO(file)
        self.file_type=file_type
        self.data_type=data_type

        #转化为pandas dataframe
        content=self.transfunc[self.file_type-1]()
        #去除原列名中可能存在的双引号
        content=content.rename(columns=lambda k: k.replace('"', ''))
        #列名转化
        content = content.rename(columns=self.dict[data_type-1])
        #print(content)
        return content


    def read_txt(self):
        return pd.read_table(self.myfile,sep=',',quotechar="'",encoding='gbk')

    def read_csv(self):

        return pd.read_csv(self.myfile,sep=',',quotechar="'",encoding='gbk')

    def read_excel(self):
        return pd.read_excel(self.myfile)

# file=io.FileIO('d://testbench//2.csv')
# reader=filereader()
# x=reader.get_file_read(file,data_type=3,file_type=3)
#
# for row_index,row in x.iterrows() :
#     print(row['containers'])

reader=filereader()
