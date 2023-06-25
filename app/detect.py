#异常数据检测模块
import pandas as pd
import re
from dmdb import cus_db,lgs_db,lgsco_db,ctnd_db,trans_db
from models import abnormal,lgscompany,logistics,customer,ctndynamic,transport
import time
class errordetect:
    data_to_detect=[]           #需要进行检测的数据
    error_data=[]               #当前批次存在异常的数据
    pass_data=[]                #通过检测的数据
    rules=[]                    #检测规则
    data_type=0                 #文件类型
    number=0
    #0对应所有数据通用的检查规则
    #1对应客户信息的检查规则
    #2对应物流信息的检查规则
    #3对应装货信息的检查规则
    #4对应卸货信息的检查规则
    #5对应物流公司信息的检查规则
    #6对应集装箱动态信息的检查规则
    def __init__(self):

        for i in range(7):
            self.rules.append([])
        for i in range(7):
            all_edata.append([])
        self.rules[0].append(self.is_already_exist)
        #self.rules[1].append(self.is_phone_num)
        self.rules[1].append(self.is_personal_id)
        self.rules[2].append(self.is_personal_id)
        #self.rules[2].append(self.is_exist_cus)        #客户信息应在物流信息前提交
        self.rules[3].append(self.is_exist_lgs)        #物流信息应在装货信息前提交
        self.rules[4].append(self.is_exist_lgs)        #物流信息应在卸货信息前提交
        self.rules[5].append(self.is_phone_num)


    def get_data_detect(self,data,data_type):
        #获取数据并进行检测
        #清空数据

        self.error_data.clear()
        self.pass_data=[]
        #获取数据与数据类型
        self.data_to_detect=data
        self.number=len(data)
        self.data_type=data_type
        #检测

        self.detectdata()



    def detectdata(self):
        #对pandas dataframe数据进行甄别
        for row_index,row in self.data_to_detect.iterrows() :
            #使用rules中的规则对函数进行判定
            flag=True          #是否存在异常
            judge=[]           #judge[1]为错误原因
            #针对通用数据类型的规则
            for func in self.rules[0] :
                retmsg=func(row)
                if(retmsg[0]==False) :
                    if(flag) :
                        flag = False
                        judge.append(row)
                        judge.append(retmsg[1])
                    else :
                        judge[1]+=','+retmsg[1]
            #若出现通用检查中的错误，则无需进行后续检查
            if flag==False :
                self.error_data.append(judge)
                continue
            #针对特定数据类型的规则
            for func in self.rules[self.data_type] :
                retmsg=func(row)
                if(retmsg[0]==False) :
                    if(flag) :
                        flag = False
                        judge.append(row)
                        judge.append(retmsg[1])
                    else :
                        judge[1]+=','+retmsg[1]
            if(flag) :
                #数据正常无误
                self.pass_data.append(row)
                pass
            else :
                #数据存在异常
                self.error_data.append(judge)


    def get_errdata(self):
        #获取异常数据
        #转化为abnmsg对象列表返回
        data=[]
        transfunc=None
        #根据filetype获取转化方法
        if self.data_type==1:
            transfunc=customer.cusmsg
        elif self.data_type==2 :
            transfunc=logistics.lgsmsg
        elif self.data_type==3 or self.data_type==4:
            transfunc=transport.transmsg
        elif self.data_type==5 :
            transfunc=lgscompany.lgscomsg
        elif self.data_type==6 :
            transfunc=ctndynamic.ctndmsg

        for item in self.error_data :

            #转化为abnormal abnmsg类型
            abn = abnormal.abnmsg(
                transfunc(Dict=item[0]),        #原数据
                item[1],                        #错误原因
                self.data_type                  #数据类型
            )
            data.append(abn)
            all_edata[self.data_type].append(abn)
        #print(data)
        return data



    def get_passdata(self):
        #获取正常数据
        #仍以dataframe的形式返回
        #print(pd.concat(self.pass_data,axis=1).T)
        if len(self.pass_data) !=0 :
            return pd.concat(self.pass_data,axis=1).T
        else :
            return []

    def clear(self,ids:list[str]):
        #清除all_edata中的异常数据
        #ids为要清除的异常数据编号
        for id in ids :
            data_type=int(id[-1])
            #查找相关id的数据
            for edata in all_edata[data_type]:
                if edata.id==id :
                    all_edata[data_type].remove(edata)

    #以下为具体的检测函数
    def is_phone_num(self,row):
        #电话号码格式验证
        retmsg=[]
        phone=row['phone']
        if re.match(r"^1[35678]\d{9}$", phone) :
            retmsg.append(True)
        else :
            retmsg.append(False)

        if(retmsg[0]==False):
            retmsg.append("电话号码格式错误")
        return retmsg

    def is_personal_id(self,row):
        #身份证号验证
        retmsg=[]
        id=str(row['cus_id'])
        if len(id) != 18 and len(id) != 15:
            retmsg.append(False)
            retmsg.append("身份证号格式错误")
            return retmsg
        regularExpression = "(^[1-9]\\d{5}(18|19|20)\\d{2}((0[1-9])|(10|11|12))(([0-2][1-9])|10|20|30|31)\\d{3}[0-9Xx]$)|" \
                            "(^[1-9]\\d{5}\\d{2}((0[1-9])|(10|11|12))(([0-2][1-9])|10|20|30|31)\\d{3}$)"

        if re.match(regularExpression, id):
            if len(id) == 18:
                n = id.upper()
                # 前十七位加权因子
                var = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
                # 这是除以11后，可能产生的11位余数对应的验证码
                var_id = ['1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2']

                sum = 0
                for i in range(0, 17):
                    sum += int(n[i]) * var[i]
                sum %= 11
                if (var_id[sum]) != str(n[17]):
                    retmsg.append(False)
                    retmsg.append("身份证号格式错误")
                    return retmsg
            return [True]
        else:
            return [False,"身份证号格式错误"]

    def is_already_exist(self,row):
        #当前信息是否已经存在于数据库中
        flag=False
        if (self.data_type == 1):
            # cus_db
            flag=cus_db.already_exist(row)
        elif (self.data_type == 2):
            # lgs_db
            flag=lgs_db.already_exist(row,self.number)
        elif (self.data_type == 3 or self.data_type == 4):
            # trans_db
            flag=trans_db.already_exist(row, self.data_type - 3)
        elif (self.data_type == 5):
            # lgsco_db
            flag=lgsco_db.already_exist(row)
        elif (self.data_type == 6):
            # ctnd_db
            flag=ctnd_db.already_exist(row,self.number)
        if flag :
            return [False,"该信息已经录入数据库"]
        else :
            return [True]

    def is_exist_cus(self,row):
        #客户信息是否存在
        id = row['cus_id']
        if cus_db.already_exist(row) :
            return [True]
        else :
            return [False,"客户信息不存在"]

    def is_exist_lgs(self,row):
        #物流信息是否存在
        id = row['order_id']
        if lgs_db.already_exist(row) :
            return [True]
        else :
            return [False,"物流信息不存在"]




# data = pd.DataFrame([['1837139808', '42112100210130050', '没', '湖北'], ['111', '222', '开', '上海'], ['18371389808', '421121200210130050', '开', '上海']],
#                         columns=['phone', 'cus_id', 'cus_name', 'location'])
# print(data)
# test = errordetect(data, 1)
# err = test.get_errdata()
# print(test.get_passdata())
# #for row_index,row in data.iterrows():
#  #   x.is_phone_num(row)
#   #  x.is_personal_id(row)

all_edata=[]                        #存储所有异常数据
detector=errordetect()              #异常数据检测器