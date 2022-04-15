#coding=utf-8 
from functions import awsservices
from functions import RightsCheck
import time
from functions import __ConnectDB__
from django.shortcuts import render_to_response   #返回请求模块
import CheckDBStatus
from django.http import HttpResponse,HttpResponseRedirect
import thread
import logging

loginfo = logging.getLogger('sourceinfo')


'''
userName: String
snapshot: String, from website
dbSize: String, db.m2.xlarge |db.m2.2xlarge | db.m2.4xlarge | db.m3.medium | db.m3.large | db.m3.xlarge | db.m3.2xlarge | db.m4.large | db.m4.xlarge | db.m4.2xlarge | db.m4.4xlarge | db.m4.10xlarge | db.r3.large | db.r3.xlarge | db.r3.2xlarge | db.r3.4xlarge | db.r3.8xlarge | db.t2.micro | db.t2.small | db.t2.medium | db.t2.large
'''
def CreateDB(req):
    username = req.session.get('username','anybody')
    dbRegion = awsservices.get_awsclient('rds')
    if username == 'anybody':
        return render_to_response('login.html',{})
    else:
        right = RightsCheck.Check(username)
        snapshot=req.GET.get('snapname') #快照名用来创建新的数据库
        dbSize=req.GET.get('dbSize') #数据库的默认配置为单核，1G内存。
        try:
            timeNow = time.strftime("%Y%m%d-%H%M%S",time.localtime())
            dbName = username+timeNow
            if dbSize == 'db.r3.large':
                getResult = dbRegion.restore_db_instance_from_db_snapshot(DBInstanceIdentifier=dbName, #数据库名=用户名+时间戳
                                                                      DBSnapshotIdentifier=snapshot, #快照名称
                                                                      DBInstanceClass=dbSize, #数据库配置（大小）
                                                                      AvailabilityZone='cn-north-1a', #可用区AZ
                                                                      DBSubnetGroupName='default', #子网组
                                                                      PubliclyAccessible=True, #公网访问策略
                                                                      MultiAZ=False, #多可用区AZ
                                                                      StorageType='io1', #存储类型：标准SSD和IOPS
                                                                      Iops=3000 #IOPS值，与生产保持相同
                                                                      )
            elif dbSize == 'db.t2.micro':
                getResult = dbRegion.restore_db_instance_from_db_snapshot(DBInstanceIdentifier=dbName, #数据库名=用户名+时间戳
                                                                      DBSnapshotIdentifier=snapshot, #快照名称
                                                                      DBInstanceClass=dbSize, #数据库配置（大小）
                                                                      AvailabilityZone='cn-north-1a', #可用区AZ
                                                                      DBSubnetGroupName='default', #子网组
                                                                      PubliclyAccessible=True, #公网访问策略
                                                                      MultiAZ=False, #多可用区AZ
                                                                      StorageType='standard', #存储类型：标准SSD和IOPS
                                                                      )
            else:
                pass
            if getResult['DBInstance']['DBInstanceIdentifier']: #判断是否创建成功
                loginfo.info('成功，%s,创建数据库成功,数据库：%s' % (username,dbName))
                sql = 'INSERT INTO info(`staff_name`,`database_name`,`dbSize`) VALUES(\'%s\',\'%s\',\'%s\');' % (username,dbName,dbSize) #成功写入数据库，status默认为0，为1时为关闭
                __ConnectDB__.ConnectDB(sql)
                thread.start_new_thread(CheckDBStatus.CheckDBStatus,(dbName,username)) #创建检查子线程
                temp1 = '<h4>Create DB Success! Please waiting for success Email.</h4>'
                return HttpResponseRedirect('/src/getdb/')
            else:
                temp1 = '<h4>Create DB Failed!</h4>'
                loginfo.info('失败，%s,创建数据库失败,数据库：%s' % (username,dbName))
                return render_to_response('createDB.html',{'result':temp1})
        except Exception as e:
            loginfo.info('失败，%s,创建数据库失败,数据库：%s，原因%s' % (username,dbName,e))
            return render_to_response('createDB.html',{'result':e})