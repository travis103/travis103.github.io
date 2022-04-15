#coding=utf-8 
from functions import awsservices
from functions import __ConnectDB__
from functions import SendEmail
import thread
import time
import logging

loginfo = logging.getLogger('sourceinfo')

def CheckDBStatus(dbName,userName):
    dbRegion = awsservices.get_awsclient('rds')
    try:
        while 1:
            result = dbRegion.describe_db_instances(DBInstanceIdentifier=dbName) #获得dbName数据库当前状态
            if result['DBInstances'][0]['DBInstanceStatus'] != 'creating': #如果为修改中状态，则证明创建成功。一般该状态会持续15分钟以上，可作为监控指标，不至于跳过该阶段。
                host = "%s.cofh1myagdtp.rds.cn-north-1.amazonaws.com.cn" % dbName #数据库的DNS规则为dbName+固定值
                grantSQL = 'Grant all on `ALA_ONION`.* to \'allen\'@\'%\';flush privileges;' #给allen用户授权读写权限
                __ConnectDB__.GrantDB(grantSQL, host)
                loginfo.info('成功，%s,数据库：%s,授权完成，用户名allen' % (userName,dbName))
                '''修改该数据库实例的状态为10，表示已经可以正常提供服务'''
                updateSQL = "Update `info` Set `status` = 10, `dnsname`=\'%s\' Where `database_name`=\'%s\';" % (host,dbName)
                __ConnectDB__.ConnectDB(updateSQL)
                '''发送创建成功邮件'''
                subject = 'Create DB Success! DB: %s' % dbName
                message = "Dear %s：\n数据库地址：\n%s" % (userName,host)
                emailSQL = "SELECT `email` FROM `userinfo` WHERE `username`=\'%s\';" % userName
                getEmail = __ConnectDB__.ConnectDB(emailSQL)
                SendEmail.SendEmail(getEmail[0]['email'],subject,message)
                loginfo.info('成功，%s,数据库：%s,修改状态为10，发送邮件成功' % (userName,dbName))
                thread.exit()
            else:
                print ('still checking %s' % result['DBInstances'][0]['DBInstanceStatus'])
                time.sleep(30)
    except Exception as e:
        print (e)
        loginfo.info('失败，%s,数据库：%s,检查数据库状态失败，原因：%s' % (userName,dbName,e))
        return False
