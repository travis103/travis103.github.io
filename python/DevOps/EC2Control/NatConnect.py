#coding=utf-8
#iptables -A PREROUTING -t nat -p tcp -d 0.0.0.0/0 -j DNAT --to  180.153.89.75

from functions import Credentials
from functions import __ConnectDB__
from functions import RightsCheck
from django.shortcuts import render_to_response   #返回请求模块
from django.http import HttpResponseRedirect
import logging
import time
import thread

loginfo = logging.getLogger('sourceinfo')
def GetUserData(dst,level):
    if level == 100:
        sql = 'Select * From `Nat_Info`;'
    elif level:
        sql = 'Select * From `Nat_Info` Where `Level` = %s;' % level
    else:
        loginfo.info('失败，没有对应的权限，输入值为: %s' % level)
    result = __ConnectDB__.ConnectDB(sql)
    for i in result:
        if dst == i['Dst']:
            userData = '''#!/bin/bash
iptables -A PREROUTING -t nat -p tcp -d 0.0.0.0/0 -j DNAT --to %s
iptables -A INPUT -p tcp --dport 80 -i eth0 -j ACCEPT
iptables -A INPUT -p tcp --dport 8000 -i eth0 -j ACCEPT
iptables -A INPUT -p tcp --dport 2202 -i eth0 -j ACCEPT
service iptables save
service iptables restart
            ''' % i['IP']
            break
        else:
            pass
    try:
        loginfo.info('成功，返回用户数据，UserData：%s' % userData)
        return userData
    except Exception as e:
        loginfo.info('失败，返回用户数据，原因: %s' % e)
        return False
    
def AssociateIP(instanceId,args):
    ec2Region = Credentials.getCredentials('ec2', 'client')
    loginfo = logging.getLogger('sourceinfo')
    while 1:
        time.sleep(10)
        result = ec2Region.describe_instances(InstanceIds=[instanceId])
        if result['Reservations'][0]['Instances'][0]['State']['Name'] == 'running':
            result = ec2Region.associate_address(InstanceId=instanceId,PublicIp='54.223.203.103',AllowReassociation=True)
            loginfo.info('成功，分配弹性IP成功，AssociationId: %s' % result)
            break
        else:
            loginfo.info('等待，分配弹性IP，当前状态: %s' % result['Reservations'][0]['Instances'][0]['State']['Name'])
            time.sleep(5)
    
def StartEC2(req):
    username = req.session.get('username','anybody')
    if username == 'anybody':
        return render_to_response('login.html',{})
    else:
        pass
    dst = req.GET.get('Dst')
    sql = 'Select `Nat_Level` From `userinfo` Where `username` = \'%s\';' % username
    result = __ConnectDB__.ConnectDB(sql)
    userData = GetUserData(dst,result[0]['Nat_Level'])
    if userData:
        ec2Region = Credentials.getCredentials('ec2', 'client')
        try:
            getInfo = ec2Region.run_instances(
                ImageId='ami-24895e49',
                MinCount=1,
                MaxCount=1,
                SecurityGroupIds=['sg-5f03f23b'],
                UserData=userData,
                InstanceType='t2.micro'
                )
            instanceID = getInfo['Instances'][0]['InstanceId']
            loginfo.info('成功，创建EC2实例，实例ID: %s' % instanceID)
            ec2Region.create_tags(Resources=[getInfo['Instances'][0]['InstanceId']],
                          Tags=[
                              {
                                  'Key':'Name',
                                  'Value':'%s-NAT' % username
                                }])
            loginfo.info('成功，修改EC2实例Tag，Tag: %s-NAT' % username)
            thread.start_new_thread(AssociateIP,(instanceID,'success'))    #建立子线程，后台监控实例状态，并且分配弹性IP
        except Exception as e:
            loginfo.info('失败，创建EC2实例失败，原因: %s' % e)
    return HttpResponseRedirect('/ec2control/getinfo/')

def Index(req):
    username = req.session.get('username','anybody')
    if username == 'anybody':
        return render_to_response('login.html',{})
    else:
        pass
    right = RightsCheck.Check(username)
    sql = 'Select `Nat_Level` From `userinfo` Where `username` = \'%s\';' % username #查看该用户的NAT权限
    result = __ConnectDB__.ConnectDB(sql)
    userLevel = result[0]['Nat_Level']
    if userLevel == 100: #超级管理员有所有权限
        sql = 'Select `IP`,`Dst`,`DstName` From `Nat_Info`;'
    elif userLevel != 0:
        sql = 'Select `IP`,`Dst`,`DstName` From `Nat_Info` Where `Level` = %s;' % result[0]['Nat_Level']
    else:
        return render_to_response('getNATInfo.html',{'noRights':1,'username':username,'rights':right})
    result = __ConnectDB__.ConnectDB(sql)
    return render_to_response('getNATInfo.html',{'Nat_Info':result,'username':username,'rights':right})
