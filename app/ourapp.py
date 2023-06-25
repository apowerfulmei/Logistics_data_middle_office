#rounter定义
import pandas as pd
from fastapi import FastAPI,UploadFile,Form,Response,status
from models import customer,logistics,transport,lgscompany,ctndynamic,abnormal
from dmdb import cus_db,lgs_db,lgsco_db,ctnd_db,trans_db,dbfunc
from mysqldb import sqldb
from app import detect,reader
from app.detect import detector
from app.reader import reader
from analysis import basic
from time import time  #时间测试

app = FastAPI()


@app.get("/greet/")
def greet(id:str):
    return {"name": "Mei","location": {"province":"Hubei","county":"tuanfeng"}, "right": True,"id":id}


@app.get("/get_cusmsg",response_model=customer.cusmsg_out)
def get_cusmsg():
    items=[]
    number=0
    items = cus_db.fetch_data()    #此处调用数据库接口，获取客户信息列表
    number=len(items)
    return {"number":number,"messages":items}


@app.get("/get_lgsmsg",response_model=logistics.lgsmsg_out)
def get_lgsmsg():
    items=[]
    number=0
    items=lgs_db.fetch_data()      #此处调用数据库接口，获取物流信息列表
    number=len(items)
    return {"number":number,"messages":items}

@app.get("/get_transmsg",response_model=transport.transmsg_out)
def get_transmsg(type:int):
    items=[]
    number=0
    items=trans_db.fetch_data(type)      #此处调用数据库接口，获取货物操作信息列表
    number=len(items)
    return {"number":number,"messages":items}

@app.get("/get_lgscomsg",response_model=lgscompany.lgscomsg_out)
def get_lgscomsg():
    items=[]
    number=0
    items=lgsco_db.fetch_data()     #此处调用数据库接口，获取物流公司信息列表
    number=len(items)
    return {"number":number,"messages":items}


@app.get("/get_ctndmsg",response_model=ctndynamic.ctndmsg_out)
def get_ctndmsg():
    items=[]
    number=0
    items=ctnd_db.fetch_data()      #此处调用数据库接口，获取集装箱动态信息列表
    number=len(items)
    return {"number":number,"messages":items}

@app.get("/admin/get_edata")
def get_edata():
    #获取所有异常数据
    return {"cusmsgs":        detect.all_edata[1],
            "lgsmsgs":        detect.all_edata[2],
            "transmsg_ous":   detect.all_edata[3],
            "transmsg_ins":   detect.all_edata[4],
            "lgscomsgs":      detect.all_edata[5],
            "ctndmsgs":       detect.all_edata[6]}


@app.post("/admin/upload_data")
async def post_uploaddata(response:Response,file_type: int =Form(...), data_type :int=Form(...), file :UploadFile=Form(...)):
    #file_type: 文件类型，1.excel，2.txt，3.csv
    #data_type: 数据类型，1.客户信息，2.物流信息，3.装货、卸货信息，4.物流公司信息，5.集装箱动态信息
    #返回内容：accept_num，成功存数的数据项数量
    #deny_num，存在异常的数据项数量
    #messages列表，每一项包括异常数据项以及错误原因

    # print("file type:",file_type)
    # print("data type:", data_type)
    # print("size:%d,name:%s,type:%s"%(file.size,file.filename,file.content_type))

    #暂定为将各种文件都转化为pandas dataframe格式
    g=time()
    try:
        content=await file.read()
        data=reader.get_file_read(content,file_type=file_type,data_type=data_type)
    except Exception as e:
        # 文件读取失败
        #返回状态码201，并返回错误原因
        response.status_code = status.HTTP_201_CREATED
        return {"error": "文件读取失败，请检查编码、格式等等"}

    #异常数据检测
    a=time()
    print("读取文件:",a-g)
    detector.get_data_detect(data,data_type)

    #筛选出异常数据
    err_data=detector.get_errdata()
    b=time()
    print("检测：",b-a)
    #筛选出正常数据
    data=detector.get_passdata()
    c=time()
    print("筛选：",c-b)
    #根据data_type类型决定数据存储
    if len(data)!=0 :
        dbfunc.store_data(data,data_type)
    v=time()
    print("存储：",v-c)

    #前端上传数据
    return {"accept_num":len(data),"deny_num":len(err_data),"messages":err_data}

@app.post("/admin/upload_edata")
def post_uploadedata(items:abnormal.abnmsg_in):
    #清除原有编号的异常数据
    ids=[]
    accept_num=0
    deny_num=0
    detector.clear(items)
    #异常数据修正回传
    for item in items.messages:
        data = item['message']
        #json转dataframe
        data=pd.DataFrame.from_dict(data,orient='index').T
        data_type=item['data_type']
        #异常数据检测
        detector.get_data_detect(data, data_type)
        edata=detector.get_errdata()
        if len(edata)==0 :
            #数据无异常，进行存储
            dbfunc.store_data(data,data_type)
            ids.append(item.id)
            accept_num+=1
        else :
            #数据存在异常
            deny_num+=1
    detector.clear(ids)
    return {"accept_num":accept_num,"deny_num":deny_num}

@app.post("/admin/delete_edata")
def post_deletedata(items:abnormal.eid_in):
    #删除指定编号的异常数据
    detector.clear(items.ids)
    return {"result":True}


@app.post("/admin/upload_online")
def post_uploadonline(items:abnormal.abnmsg_in):
    error_data=[]
    accept_num=0
    deny_num=0
    #在线上传数据
    for item in items.messages:
        data = item['message']
        #json转dataframe
        data=pd.DataFrame.from_dict(data,orient='index').T
        data_type=item['data_type']
        #异常数据检测
        detector.get_data_detect(data, data_type)
        edata=detector.get_errdata()
        if len(edata)==0 :
            #数据无异常，进行存储
            dbfunc.store_data(data,data_type)
            accept_num+=1
        else :
            #数据存在异常
            error_data.append(detector.get_errdata()[0])
            deny_num+=1

    return {"accept_num":accept_num,"deny_num":deny_num,"messages":error_data}



@app.post("/admin/upload_mysql",status_code=200)
def post_uploadmysql(response:Response,
                    data_type: int  =Form(),
                    host:      str  =Form(),  # 主机
                    port:      int  =Form() , # 端口
                    dbname:    str  =Form(),  # 数据库名
                    user:      str  =Form(),  # 用户名
                    passwd:    str  =Form(),  # 密码
                    tbname:    str  =Form() , # 表名
                     ):
    #获取数据库信息，并从中获取数据
    try :
        #尝试连接数据库
        cur=sqldb.dbconnect(
            host=host,
            port=port,
            dbname=dbname,
            user=user,
            passwd=passwd
        )
        data=sqldb.fetch_data(tbname,cur)
    except Exception as e:
        # 数据库连接失败或者获取数据失败
        response.status_code = status.HTTP_201_CREATED
        return {"error": "数据库连接失败"}
    #对数据进行处理
    #转化为pandas dataframe
    #获取columns
    index=dict
    if(data_type==1):
        index=customer.cus_dict
    elif(data_type==2):
        index=logistics.lgs_dict
    elif(data_type==3 or data_type==4):
        index=transport.trans_dict
    elif(data_type==5):
        index=lgscompany.lgsco_dict
    elif(data_type==6):
        index=ctndynamic.ctnd_dict
    data=pd.DataFrame(data=data,columns=index.values())
    #print(data)

    #异常数据检测
    detector.get_data_detect(data,data_type)
    err_data=detector.get_errdata()
    data=detector.get_passdata()

    #正常数据存储
    dbfunc.store_data(data,data_type)
    return {"accept_num":len(data),"deny_num":len(err_data),"messages":err_data}


@app.get("/get_port_goods")
def get_port_goods() :
    #获取所有港口名称
    return basic.get_port_goods()

@app.post("/port/modify_info")
def post_port_modifyinfo(sdate:str=Form(),edate:str=Form(),port:str=Form()):
    #修改时间与港口
    #调用接口进行修改
    pass

@app.post("/goods/modify_info")
def post_goods_modifyinfo(sdate:str=Form(),edate:str=Form(),goods:str=Form()):
    #修改时间与货物
    #调用接口进行修改
    pass

@app.post("/port/modify_goods")
def post_modifygoods(goods:str=Form()):
    #修改目标货物
    #调用接口进行修改
    pass

@app.get("/port/analy_throughput")
def get_althroughput():
    #筛选出港口各个月的吞吐量数据
    #调用接口获取数据
    pass
    return {"month":[],"throughput":[]}

@app.get("/port/analy_percentage")
def get_alpercentage():
    #筛选出港口各种货物的吞吐量
    #调用接口获取数据

    return {"goods":[],"throughput":[]}

@app.get("/port/analy_goods")
def get_algoods():
    #筛选出港口某种货物各月的吞吐量
    #调用接口获取数据

    return {"month":[],"throughput":[]}