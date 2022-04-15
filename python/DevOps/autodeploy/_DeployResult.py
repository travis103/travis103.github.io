#coding=utf-8 
from django.shortcuts import render_to_response   #返回请求模块
from functions import __ConnectDB__
import json

def GetResults(req):
    username = req.session.get('username','anybody')
    if username == 'anybody':
        return render_to_response('login.html',{})
    else:
        sql = 'Select * From `deploy_info`;'
        results = __ConnectDB__.ConnectDB(sql)
        deployinfos = []
        for i in results:
            deployinfo = {}
            deployinfo['versionid'] = i['VersionId']
            deployinfo['asgname'] = i['AsgName']
            deployinfo['optor'] = i['Optor']
            deployinfo['env'] = i['Env']
            deployinfo['ct'] = str(i['Ct'])
            if i['Status'] == 9:
                deployinfo['state'] = "失败"
            else:
                deployinfo['state'] = "成功"
            deployinfos.append(deployinfo)
        a = json.dumps(deployinfos)
        return render_to_response('deployHistory.html',{'allInfos':a,'username':username})