#coding=utf-8 
from functions import __ConnectDB__
from functions import RightsCheck
from django.shortcuts import render_to_response   #返回请求模块
from django.http import HttpResponseRedirect
import datetime
import json
import logging

loginfo = logging.getLogger('sourceinfo')
'''用户登录界面'''
def GetUserInfo(req):
    username = req.session.get('username','anybody')
    if username == 'anybody':
        return render_to_response('login.html',{})
    else:
        pass
    right = RightsCheck.Check(username)
    if int(right) == 100:
        getClosedSQL = 'Select * from info WHERE `status`=1;'#获得关闭的数据库信息，判断依据为status=1
        getRunSQL = 'Select * from info WHERE `status`in (0,10);'#获得仍在运行的数据库信息创建成功状态为10，创建中状态为0
    elif int(right) != 0:
        getClosedSQL = 'Select * from info WHERE `staff_name`=\'%s\' and `status`=1;' % username #获得关闭的数据库信息，判断依据为status=1
        getRunSQL = 'Select * from info WHERE `staff_name`=\'%s\' and `status`in (0,10);' % username #获得仍在运行的数据库信息创建成功状态为10，创建中状态为0
    else:
        return HttpResponseRedirect('/ec2control/getinfo/') #如果权限为0，则跳转到实例操作页面。
    dateNow = datetime.datetime.now()
    try:
        getClosedResults = __ConnectDB__.ConnectDB(getClosedSQL)
        n = len(getClosedResults)
        totalfee = 0
        for i in getClosedResults:
            i['id'] = n
            i['start_time'] = str(i['start_time'])
            i['end_time'] = str(i['end_time'])
            if i['charge']:
                i['fee'] = i['charge']
            else:
                i['fee'] = 0
            totalfee += i['fee']
            n -= 1
        getRunResults = __ConnectDB__.ConnectDB(getRunSQL)
        n = len(getRunResults)
        for j in getRunResults:
            j['id'] = n
            j['during_time'] = int((dateNow - j['start_time']).total_seconds()/3600)+1
            j['start_time'] = str(j['start_time'])
            j['end_time'] = str(j['end_time'])
            if j['status'] == 0:
                j['status'] = '<span style="color:red">正在创建</span>'
            else:
                j['status'] = '<span style="color:#00FF00">创建成功</span>'
            dTime = int(j['during_time'])
            if j['dbSize'] == 'db.r3.large':
                fee = 7.07
                exfee = 7.07
            elif j['dbSize'] == 'db.t2.micro':
                fee = 4.22
                exfee = 1.08
            if dTime >= 36:
                j['fee'] = round(36*fee+(dTime-36)*exfee,2)
            else:
                j['fee'] = round(int(j['during_time'])*fee,2)
            totalfee += j['fee']
            n -= 1
        getClosedResults = json.dumps(getClosedResults)
        getRunResults = json.dumps(getRunResults)
    except Exception as e:
        loginfo.info('查询数据库状态失败，原因：%s' % e)
    return render_to_response('dbMng.html',{'username':username,'getClosedResults':getClosedResults,'getRunResults':getRunResults,'totalfee':totalfee,'rights':right})
