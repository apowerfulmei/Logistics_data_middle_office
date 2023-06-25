import dmPython




conn=dmPython.connect()
db=conn.cursor()



def init()->bool:
    global db
    try:
        #raise Exception('错误了。。。')
        conn = dmPython.connect(user='SYSDBA', password='SYSDBA', server='127.0.0.1', port=5236)
        db = conn.cursor()
        #print("funny")
    except Exception as e:
        print("连接失败：%s"%e)
        return False
    else:
        return True

init()



