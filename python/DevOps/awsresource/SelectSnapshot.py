#coding=utf-8 
from functions import awsservices
from functions import RightsCheck
import GetDBInfo
from django.shortcuts import render_to_response   #返回请求模块
from django.http.response import HttpResponse   #返回请求模块
import operator
from dateutil import tz


def GetDBs(req):
    dbName = req.GET.get('dbName')
    username = req.session.get('username','anybody')
    if username == 'anybody':
        return render_to_response('login.html',{})
    else:
        pass
    right = RightsCheck.Check(username)
    snaps = {}
    dbInfos = GetDBInfo.GetDBs()
    for key,value in dbInfos.items():
        snapshotInfos = awsservices.get_awsclient('rds').describe_db_snapshots(DBInstanceIdentifier=key)
        for snap in snapshotInfos['DBSnapshots']:
            info = {}
            info['snapname'] = snap['DBSnapshotIdentifier']
            info['ct'] = str(snap['SnapshotCreateTime'].astimezone(tz.gettz('CST')))
            if snaps.has_key(key):
                snaps[key][0].append(info)
            else:
                #预先定义好snaps的格式：{数据库实例id:[[镜像信息1，镜像信息2],1]，数据库实例id:[[镜像信息1，镜像信息2],2]}，字典数组的第一位是该数据库实例镜像的所有信息，第二个是前端页面展示时tab的序号（同时也可以用来做顺序控制，数值再数据库中设定）
                snaps[key] = [[],0] 
                snaps[key][0] = [info]
        #获得数据库中定义好的，该数据库的序号标签
        snaps[key][1] = value[1]
    result = sorted(dbInfos.iteritems(),key=lambda asd:asd[1][1], reverse=False)
    return render_to_response('getSnapshot.html',{'snapshotInfos':snaps,'envtype':result,'username':username,'rights':right})