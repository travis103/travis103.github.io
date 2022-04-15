#coding=utf-8
from django.http.response import HttpResponse   #返回请求模块
from django.shortcuts import render_to_response   #返回请求模块
from functions import RightsCheck
from functions import __ConnectDB__
import logging

loginfo = logging.getLogger('sourceinfo')
def Modify(req):
    username = req.session.get('username','anybody')
    if username == 'anybody':
        return render_to_response('login.html',{})
    else:
        pass
    getInstanceId = 'i-'+req.POST.get('instanceId').split('-')[1]
    getInstanceName = req.POST.get('instanceName')
    getInstanceType = req.POST.get('instanceType')
    try:
        #过滤出预发布使用扩展组的服务器
        if getInstanceName.startswith(('Pre-RoP','Pre-SoA','Pre-Joboffline','Pre-PMS','Pre-3rdParty')):
            instanceStatus = 3
            deleteStatus = 2
        else:
            instanceStatus = 1
            deleteStatus = 0
        sql = 'Select * From `EC2_CONTROL` Where `InstanceName`=\'%s\' And `InstanceStatus` In(1,3);' % getInstanceName
        result = __ConnectDB__.ConnectDB(sql)
        if req.POST.get('StartTime'):
            getTime = req.POST.get('StartTime')
            if result:
                sql = 'Update `EC2_CONTROL` Set `StartTime`=\'%s\' Where `InstanceName`=\'%s\' And `InstanceStatus` In(1,3);' % (getTime,getInstanceName)
            else:
                sql = 'Insert Into `EC2_CONTROL`(`InstanceId`,`InstanceName`,`InstanceType`,`StartTime`,`InstanceStatus`) Values(\'%s\',\'%s\',\'%s\',\'%s\',%s);' % (getInstanceId,getInstanceName,getInstanceType,getTime,instanceStatus)
        elif req.POST.get('StopTime'):
            getTime = req.POST.get('StopTime')
            if result:
                sql = 'Update `EC2_CONTROL` Set `StopTime`=\'%s\' Where `InstanceName`=\'%s\' And `InstanceStatus` In(1,3);' % (getTime,getInstanceName)
            else:
                sql = 'Insert Into `EC2_CONTROL`(`InstanceId`,`InstanceName`,`InstanceType`,`StopTime`,`InstanceStatus`) Values(\'%s\',\'%s\',\'%s\',\'%s\',%s);' % (getInstanceId,getInstanceName,getInstanceType,getTime,instanceStatus)
        elif 'StartTime' in req.POST:
            sql = 'Select `StopTime` From `EC2_CONTROL` Where `InstanceName`=\'%s\' And `InstanceStatus` In (1,3);' % getInstanceName
            result = __ConnectDB__.ConnectDB(sql)
            if result[0]['StopTime']:
                sql = 'Update `EC2_CONTROL` Set `StartTime`=NULL Where `InstanceName`=\'%s\' And `InstanceStatus` In (1,3);' % getInstanceName
            else:
                sql = 'Update `EC2_CONTROL` Set `StartTime`=NULL, `InstanceStatus`=%s Where `InstanceName`=\'%s\' And `InstanceStatus` In (1,3);' % (deleteStatus,getInstanceName)
        elif 'StopTime' in req.POST:
            sql = 'Select `StartTime` From `EC2_CONTROL` Where `InstanceName`=\'%s\' And `InstanceStatus` In (1,3);' % getInstanceName
            result = __ConnectDB__.ConnectDB(sql)
            if result[0]['StartTime']:
                sql = 'Update `EC2_CONTROL` Set `StopTime`=NULL Where `InstanceName`=\'%s\' And `InstanceStatus` In (1,3);' % getInstanceName
            else:
                sql = 'Update `EC2_CONTROL` Set `StartTime`=NULL, `InstanceStatus`=%s Where `InstanceName`=\'%s\' And `InstanceStatus` In (1,3);' % (deleteStatus,getInstanceName)
        else:
            pass
        __ConnectDB__.ConnectDB(sql)
        temp1 = 'Success'
    except Exception as e:
        loginfo.info(e)
        print e
    return HttpResponse(temp1)