#coding=utf-8 
from django.shortcuts import render_to_response   #返回请求模块
from functions import __ConnectDB__
import json

'''
从数据库获得所有应用服务器信息，写入数据库是为了后期可以动态管理服务器。
'''

def index(req):
    username = req.session.get('username','anybody')
    if username == 'anybody':
        return render_to_response('login.html',{})
    else:
        sqlGetAMI = 'SELECT * FROM `deploy_info` WHERE `Status` IN (5,9) AND `Upt`<date_sub(now(),interval 30 day);'
        getAMIsInfo = __ConnectDB__.ConnectDB(sqlGetAMI)
        allInfos = []
        for i in getAMIsInfo:
            amiInfo = {}
            amiInfo['versionid'] = i['VersionId']
            amiInfo['imageid'] = i['ImageId']
            amiInfo['asgname'] = i['AsgName']
            amiInfo['env'] = i['Env']
            amiInfo['ct'] = str(i['Ct'])
            allInfos.append(amiInfo)
        a = json.dumps(allInfos)
        return render_to_response('amiMng.html',{'allInfos':a,'username':username})