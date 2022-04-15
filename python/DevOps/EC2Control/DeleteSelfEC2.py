#coding=utf-8
from functions import Credentials
from functions import __ConnectDB__
from functions import RightsCheck
from functions import FilterResult
import logging
from django.shortcuts import render_to_response   #返回请求模块

loginfo = logging.getLogger('sourceinfo')
def DeleteEC2(req):
    try:
        username = req.session.get('username','anybody')
        if username == 'anybody':
            return render_to_response('login.html',{})
        else:
            pass
        right = RightsCheck.Check(username)
    except Exception as e:
        loginfo.info('GetEC2Info: %s' % e)
        print e
    try:
        deleteEC2s = []
        ec2Region = Credentials.getCredentials('ec2', 'client')
        ec2Ids = req.POST.getlist('InstanceId')
        ec2Info = ec2Region.describe_instances(InstanceIds=ec2Ids)
        datas = FilterResult.FilterResults(params=ec2Info['Reservations'],filter=["Tags","InstanceId"])
        datas.start()
        allEC2Info = datas.results
        for i in allEC2Info:
            for j in i['Tags']:
                if j['Value'].startswith(username): #只能删除自己创建的实例
                    deleteEC2s.append(i['InstanceId'])
                else:
                    pass
        for i in deleteEC2s: #判断哪些实例不能被删除
            ec2Ids.remove(i)
        ec2Region.terminate_instances(InstanceIds=deleteEC2s)
        loginfo.info('成功: 删除 EC2: %s，不删除的 EC2：%s ' % (deleteEC2s,ec2Ids))
        for i in deleteEC2s:
            sql = 'Update `EC2_CONTROL` Set `StartTime`=NULL, `StopTime`=NULL Where `InstanceId` = \'%s\';'  % i
            __ConnectDB__.ConnectDB(sql)
        return render_to_response('getEC2Info.html',{'ec2Ids':'禁止删除实例：%s' % ec2Ids,'username':username,'right':right,'deleteEC2s':'删除实例成功：%s' % deleteEC2s})
    except Exception as e:
        loginfo.info('失败: 删除 EC2: %s，失败原因：%s' % (ec2Ids,e))
        return render_to_response('getEC2Info.html',{'ec2Ids':'禁止删除实例：%s' % ec2Ids,'error':'错误原因：%s' % e,'username':username,'right':right})