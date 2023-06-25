#基于港口分类的数据分析

class port_analysis :
    port=""         #港口名称
    sdate=""        #起始日期
    edate=""        #结束日期
    def __init__(self):
        pass

    def flush_msg(self,Port="",Sdate="",Edate=""):
        #获取新的信息
        if Port!="" :
            self.port=Port
        if Sdate!="" :
            self.sdate=Sdate
        if Edate!="" :
            self.edate=Edate

    def calcu_throughput(self):
        #计算吞吐量
        #生成各月份吞吐量柱状图与数据

        pass

    def calcu_percentage(self):
        #计算各货物吞吐量与占比以及饼状图
        pass