#coding=utf-8
import datetime
import Negative
from functions import __ConnectDB__
'''
根据输入的实例ID，判断数据库中的启停时间，然后算出从当前时间到下次执行时间还剩多长时间
返回值getAll = {'start':{int(400/s),[实例ID1,实例ID2]},'stop':{int(3000/s),[实例ID1,实例ID2]}}
'''

def CalTime():
    dateNow = datetime.datetime.strptime(datetime.datetime.now().strftime('%H:%M:%S'),'%H:%M:%S')
    getAll = {'start':{},'stop':{}}
    getStart = {}
    getStop = {}
    
    getSTsql = 'Select `InstanceId`,`StartTime`,`StopTime` From `EC2_CONTROL` Where `InstanceStatus`=1;'
    getInfo = __ConnectDB__.ConnectDB(getSTsql)
    for getST in getInfo:
        initStartT = datetime.datetime.strptime(getST['StartTime'].strftime('%H:%M:%S'),'%H:%M:%S') - dateNow
        initStopT = datetime.datetime.strptime(getST['StopTime'].strftime('%H:%M:%S'),'%H:%M:%S') - dateNow
        duringStartT = int(Negative.start(initStartT.total_seconds())) #过滤一遍时间，拿到正确的秒数
        duringStopT = int(Negative.start(initStopT.total_seconds()))
        if getStart.has_key(duringStartT):
            getStart[duringStartT].append(getST['InstanceId'])
        else:
            getStart[duringStartT] = [getST['InstanceId']]
        if getStop.has_key(duringStopT):
            getStop[duringStopT].append(getST['InstanceId'])
        else:
            getStop[duringStopT] = [getST['InstanceId']]
    getAll['start'] = getStart
    getAll['stop'] = getStop
    return getAll