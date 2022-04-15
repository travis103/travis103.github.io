#coding=utf-8 
from functions import awsservices
from functions import __ConnectDB__
import AS_Info
from functions import SendSNS
import _CheckInstanceStatus
from django.http import HttpResponse,HttpResponseRedirect #返回请求模块
from django.shortcuts import render_to_response   #返回请求模块
import logging
import thread
import os
import time
import conf
import zookeeper
loginfo = logging.getLogger('deploy')
logdeploy = logging.getLogger('lastdeploy')
logerror = logging.getLogger('errorinfo')

#删除扩展组函数。输入参数为扩展组名称
def deleteAS(asNames):
    for asName in asNames:
        awsservices.get_awsclient('autoscaling').delete_auto_scaling_group(AutoScalingGroupName=asName,ForceDelete=True)
        sql = 'UPDATE deploy_info SET `Status`=9 WHERE `AsgName` = \'%s\';' % asName #状态9为扩展组发布失败，回滚
        __ConnectDB__.ConnectDB(sql)

#扩展组名称asNames，类型为list
#action的合法参数为"increase"增加为2和"decrease"减少为0
def updateASDesired(asNames,action):
    for asName in asNames:
        if (action == 'increase'):
            number = 2
            if (asName.startswith('Prod-PMS')):
                number = 1
        elif (action == 'decrease'):
            number = 0
            sql = 'UPDATE deploy_info SET `Status`=3 WHERE `AsgName` = \'%s\';' % asName #状态3为扩展组已下线，但是未删除。
            __ConnectDB__.ConnectDB(sql)
        elif (action == 'rollback'):
            number = 1
        else:
            loginfo.error("Update AS action input error!")
            logdeploy.error("Update AS action input error!")
            logerror.error("Update AS action input error!")
            return False
        awsservices.get_awsclient('autoscaling').update_auto_scaling_group(AutoScalingGroupName=asName,MinSize=number,DesiredCapacity=number)

def index(req):
    env = req.GET.get('env')
    username = req.session.get('username','anybody')
    if username == 'anybody':
        return render_to_response('login.html',{})
    else:
        if not env:
            env = "Prod"
        sql = 'Select `EnvName`,`EnvSName` From `Env_Info` Where `Rollback_Control`=1;'
        result = __ConnectDB__.ConnectDB(sql)
        envInfo = {}
        k = 0
        for i in result:
            envInfo[k] = [i['EnvName'],i['EnvSName']]
            k += 1
        sorted(envInfo.iteritems(),key=lambda asd:asd[1], reverse=True)
        result = awsservices.get_awsclient('autoscaling').describe_auto_scaling_groups()
        datas = AS_Info.SplitASInfo(aSInfo=result['AutoScalingGroups'], env=env)
        datas.Start()
        '''最后获得的值datas.baseServer类型为dick，以服务器类型为key，环境信息在页面已经做了选择。
        baseServer：{'RoP':[扩展组列表],...}
        '''
        return render_to_response('rollback.html',{'EnvInfo':envInfo,'ASInfo':datas.baseServer,'username':username,'env':env})


def wait_instances_ok(as_name):

    cnt = 0

    while True:
        try:
            instance_ids = awsservices.get_inservice_instance(as_name)
        except:
            raise
        if instance_ids :
            if ( len(instance_ids) !=0 ) :
                break
        if (cnt<10):
            time.sleep(30)
            cnt = cnt + 1
        else:
            raise NameError("扩展组实例创建超时")

    while True:
        try:
            if awsservices.check_instance_ok(instance_ids): return True
        except:
            raise

        if (cnt < 20):
            time.sleep(30)
            cnt = cnt + 1
        else:
            raise NameError("扩展组实例启动超时")


def wait_application_ok(as_name):
    pri_ips = []
    server = as_name.split('-')[1]
    lb=['%s-env-%s-servers' % (as_name.split('-')[0], as_name.split('-')[1])]
    check_ok = False
    cnt=0

    instance_ids = awsservices.get_inservice_instance(as_name)
    instance_des = awsservices.get_awsclient('ec2').describe_instances(InstanceIds=instance_ids)
    elb_handle = awsservices.get_awsclient('elb')

    for reserv in instance_des['Reservations']:
        pri_ips.append(reserv['Instances'][0]['NetworkInterfaces'][0]['PrivateIpAddress'])

    while check_ok==False:
        if (server=='ROP') or (server=='3rdParty'):
            elb_des = elb_handle.describe_instance_health(LoadBalancerName=lb)
            check_ok=True
            for instancestate in elb_des['InstanceStates']:
                if (instancestate['State'] != 'InService'):
                    check_ok=False
                    cnt=cnt+1
                    break
            time.sleep(30)
            cnt = cnt + 1
            if(cnt>=10): raise NameError("检查%s 超时" % lb)

        else:
            try:
                if as_name.startswith('Pre'):
                    zookeeper_host=conf.PRE_ZOOKEEP
                else:
                    zookeeper_host = conf.PROD_ZOOKEEP
                handler = zookeeper.init(zookeeper_host)
                time.sleep(30)
                zkresult = zookeeper.get_children(handler, '/DevOps/servers/%s' % server)

            except Exception:
                raise NameError("获取zookeeper信息失败")
            check_ok = True
            for pri_ip in pri_ips:
                if pri_ip not in zkresult:
                    check_ok = False
                    cnt = cnt + 1
                    break
            time.sleep(30)
            cnt = cnt + 1
            if (cnt >= 20): raise NameError("zookeeper注册检查超时")

def Start(newASs):
    toServers = []  #初始化发布的目标服务器类型，类型List
    oldASs = [] #初始化旧扩展组名称，类型List
    loadbalanceName = []    #初始化负载均衡器名称，类型List
    loginfo.info('Start RollBack!!=============================================================')
    logdeploy.info('Start RollBack!!=============================================================')
    try:
        for server in newASs:        
            #分割输入的服务器名称，获得待发布服务器的环境和类型，获得ELB名称。
            s = server.split('-')
                
            loadbalance = '%s-env-%s-servers' % (s[0],s[1])
            loadbalanceName.append(loadbalance) #获得ELB名称，这里是用来做健康检查的
            
            toName = "%s-%s" % (s[0],s[1])  #获得待发布服务器的环境和类型
            toServers.append(toName)    #收集发布过的服务器类型

            #获得旧的扩展组
            oldAS=awsservices.get_autoscalinggroup(toName)
            if oldAS:
                oldASs.append(oldAS)    #添加匹配上的旧扩展组名称
            else:   #故障原因一般为有多个相同类型的扩展组中有运行的实例，这样会导致获取的数据重复，所以默认只有一个扩展组中有实例才继续
                result = "Cause Check Old AS Failed, Stop Process!!"
                raise
        
        #开始将需要会退到的扩展组实例设置为1，启动回滚
        updateASDesired(newASs, 'rollback')

        for as_new in newASs:
            wait_instances_ok(as_new)
            logdeploy.info("服务器启动成功, 开始检查应用......：%s " % as_new)
            wait_application_ok(as_new)
            logdeploy.info("应用检查完成，状态正常......：%s" % as_new)

        if newASs[0].startswith('Prod'):  # 如果服务器是从预发布到生产的，则将创建完成的生产实例升级为2
            updateASDesired(newASs, 'increase')
        updateASDesired(oldASs, 'decrease')  # 将旧的扩展组实例数量设置为0，即删除旧的实例
        loginfo.info("Rollback Finished!!")
        logdeploy.info("Rollback Finished!!")

        # 发送发布成功邮件
        subject1 = 'Rollback Success, Env: %s' % (s[0])
        message = "Version: %s Rollback Success!\nRollback servers: %s" % (s[-1], toServers)
        SendSNS.SendEmail(subject=subject1, message=message)
        loginfo.info("%s" % message)
        logdeploy.info("%s" % message)

        try:
            for i in newASs:
                print i
                sql = 'UPDATE deploy_info SET `Status`=1 WHERE `AsgName` = \'%s\';' % i  # 将回退到的扩展组状态重新设置为1。
                __ConnectDB__.ConnectDB(sql)
        except Exception as e:
            print e

    except Exception as e:
        loginfo.info(result)
        logdeploy.info(result)
        print e
        updateASDesired(newASs, 'decrease')  #回滚，将目标回滚的扩展组设置为0
        
        #发送失败的邮件
        subject1 = 'Rollback Failed, Version: %s' % s[-1]
        message = "Rollback Failed, reason: %s\nVersion: %s\nServers: %s" % (result,s[-1],toServers)
        SendSNS.SendEmail(subject=subject1, message=message)
        
def OptRollback(req):
    if req.GET.get('env') == 'Prod':
        pwd = req.GET.get('pwd')
        if pwd == 'A&cd!2#4':
            pass
        else:
            return HttpResponseRedirect('/autodeploy/rollback/')
    else:
        pass
    newASs = [] #整合需要回退到的扩展组名称，类型List
    if req.GET.get('RoP'):
        newASs.append(req.GET.get('RoP'))
    if req.GET.get('SoA'):
        newASs.append(req.GET.get('SoA'))
    if req.GET.get('Joboffline'):
        newASs.append(req.GET.get('Joboffline'))
    if req.GET.get('PMS'):
        newASs.append(req.GET.get('PMS'))
    if req.GET.get('3rdParty'):
        newASs.append(req.GET.get('3rdParty'))
    username = req.session.get('username','anybody')
    if username == 'anybody':
        return render_to_response('login.html',{})
    else:
        os.system('cat /dev/null > %s/lastestdeploy.log' % conf.LOGDIR)
        thread.start_new_thread(Start,(newASs,))    #建立子线程，执行发布
        return render_to_response('deploylog.html',{'username':username})
