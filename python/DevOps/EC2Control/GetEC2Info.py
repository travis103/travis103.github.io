#coding=utf-8
from django.shortcuts import render_to_response   #返回请求模块
from django.http.response import HttpResponse   #返回请求模块
from functions import Credentials
from functions import _GetFilters
from functions import FilterResult
from functions import __ConnectDB__
from functions import RightsCheck
import logging

loginfo = logging.getLogger('sourceinfo')
def GetEC2Info(req):
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
    ec2Region = Credentials.getCredentials('ec2', 'client')
    aSRegion = Credentials.getCredentials('autoscaling','client')
    ec2Info = {}
    #获取所有实例信息
    if right == 1:
        filters = 'Dev-*'
    elif right == 10:
        filters = 'Test*'
    elif right == 100:
        filters = '*'
    else:
        filters = ''
    try:
        filters = _GetFilters.GetMoreFilters([filters,username+'*'])
        result = ec2Region.describe_instances(Filters=filters)
        datas = FilterResult.FilterResults(params=result['Reservations'],filter=["Tags","InstanceType","Name","InstanceId","PrivateIpAddress","PublicIpAddress"])
        datas.start()
        allEC2Info = datas.results
        count = 0
        asInstanceIds = []
        sql = 'Select * From `EC2_CONTROL` Where `InstanceStatus` In(1,3);'
        result = __ConnectDB__.ConnectDB(sql)
    except Exception as e:
        loginfo.info('GetEC2Info: %s' % e)
    try:
        for i in allEC2Info:
            for k in i['Tags']:
                if k['Key'] == 'Name':
                    j = k['Value'].split('-')
                    i['Tags'] = k['Value']
                else:
                    pass
            if j[0] == 'Prod':
                pass
            else:
                if i['Tags'] in ('Pre-RoP','Pre-SoA','Pre-Joboffline','Pre-PMS','Pre-3rdParty'):
                    asInstanceIds.append(i['InstanceId'])
                else:
                    pass
                #赋值数据库中该实例的启停时间
                for m in result:
                    if i['InstanceId'] == m['InstanceId']:
                        if m['StartTime']:
                            i['StartTime'] = str(m['StartTime'])
                        if m['StopTime']:
                            i['StopTime'] = str(m['StopTime'])
                if ec2Info.has_key(j[0]):
                    ec2Info[j[0]][1].append(i)
                else:
                    ec2Info[j[0]] = [count,[i]]
                    count += 1
        if right == 100:
            asInstanceInfo = aSRegion.describe_auto_scaling_instances(InstanceIds=asInstanceIds)
            for i in asInstanceInfo['AutoScalingInstances']:
                for j in ec2Info['Pre'][1]:
                    if j['InstanceId'] == i['InstanceId']:
                        j['Tags'] = i['AutoScalingGroupName']
                        for m in result:
                            if j['Tags'] == m['InstanceName']:
                                if m['StartTime']:
                                    i['StartTime'] = m['StartTime']
                                if m['StopTime']:
                                    i['StopTime'] = m['StopTime']
        else:
            loginfo.info('GetEC2Info: %s 查询实例数据' % username)
            pass
    except Exception as e:
        loginfo.info('GetEC2Info: %s' % e)
        print e
    return render_to_response('getEC2Info.html',{'AllInfo':ec2Info,'username':username,'rights':right})