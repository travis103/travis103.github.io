#coding=utf-8 
from functions import awsservices
from functions import RightsCheck
import datetime
from functions import __ConnectDB__
from django.shortcuts import render_to_response   #返回请求模块
import logging

loginfo = logging.getLogger('sourceinfo')

def DeleteDB(req):
    username = req.session.get('username','anybody')
    if username == 'anybody':
        return render_to_response('login.html',{})
    else:
        pass
    right = RightsCheck.Check(username)
    dateNow = datetime.datetime.now()
    dbNames = req.POST.getlist('database_name')
    temp1 = ''
    for dbName in dbNames:
        if dbName.startswith(('app','other','pre-','prod-','test')): #防止恶意删除其他在用数据库
            temp1 = '<h4>请勿恶意删除！已发送告警邮件！</h4>'
            loginfo.info('警告，%s,恶意删除数据库。' % username)
        else:
            try:
                getResult = awsservices.get_awsclient('rds').delete_db_instance(DBInstanceIdentifier=dbName,SkipFinalSnapshot=True) #删除用户自己创建的数据库
                if getResult['DBInstance']['DBInstanceIdentifier']: #判断是否成功发送删除指令
                    sqlCreateTime = 'Select `start_time`,`dbSize` from info WHERE `database_name`=\'%s\';' % dbName #删除数据库后，获得数据库创建时间，以计算数据库的使用时间
                    getCT = __ConnectDB__.ConnectDB(sqlCreateTime)
                    duringTime = int((dateNow - getCT[0]['start_time']).total_seconds()/3600)+1 #用当前时间减去创建时间，获得数据库的使用时长，精确到小时
                    if getCT[0]['dbSize'] == 'db.r3.large':
                        fee = 7.07
                        exfee = 7.07
                    elif getCT[0]['dbSize'] == 'db.t2.micro':
                        fee = 4.22
                        exfee = 1.08
                    if duringTime >= 36:
                        charge = round(36*fee+(duringTime-36)*exfee,2)
                    else:
                        charge = round(duringTime*fee,2)
                    sql = 'UPDATE info SET `status`=1, `during_time`=\'%s\', `charge`=\'%s\' WHERE `database_name`=\'%s\';' % (duringTime,charge,dbName) #更新数据库状态，设置status为1（已关闭）
                    __ConnectDB__.ConnectDB(sql)
                    temp1 = temp1 + '<li><h4>删除数据库 %s 成功!</h4></li>' % dbName
                    loginfo.info('成功，%s,删除数据库成功，数据库：%s。' % (username,dbName))
                else:
                    temp1 = '<h4>Delete DB: %s Failed!</h4>' % dbName
                    loginfo.info('失败，%s,删除数据库失败，数据库：%s。' % (username,dbName))
            except Exception as e:
                temp1 = temp1 + '<h4>删除数据库 %s 失败!</h4><h4>原因: %s</h4>' % (dbName,e)
                loginfo.info('失败，%s,删除数据库失败，数据库：%s。' % (username,dbName,e))
    return render_to_response('deleteDB.html',{'userName':username,'result':temp1,'rights':right})