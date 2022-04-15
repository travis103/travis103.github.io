#coding=utf-8
import os
import thread
import logging
import _GetUserData
import time
import conf
import zookeeper

from django.shortcuts import render_to_response   #返回请求模块
from functions import awsservices
from functions import SendSNS
from functions import __ConnectDB__

loginfo = logging.getLogger('deployinfo')
logdeploy = logging.getLogger('lastdeploy')
imageidlist={}

def create_autoscalinggroup(src_server, pub_server,version,pub_lbs,optor):

    aws_ec2_client = awsservices.get_awsclient('ec2')
    aws_autoscaling_client = awsservices.get_awsclient('autoscaling')
    aws_cloud_client = awsservices.get_awsclient('cloudwatch')

    timeNow = time.strftime("%Y%m%d-%H%M%S", time.localtime())
    autoscalinggroup = '%s-%s-%s' % (pub_server, timeNow, version)
    instancetype = 't2.small' if pub_server=='Pre-3rdParty' else 'm3.medium'
    ami_name = "%s-%s" % (src_server, timeNow)
    secgroups = awsservices.get_secgroup(pub_server, 'securityGroupIds')
    subnetid = awsservices.get_secgroup(pub_server, 'subnetIds')
    az = awsservices.get_secgroup(pub_server, 'aZs')
    instanceId = awsservices.get_instanceid(src_server)
    imageid=aws_ec2_client.create_image(InstanceId=instanceId, Name=ami_name, NoReboot=True)['ImageId']
    imageidlist[autoscalinggroup]=imageid
    userDate = _GetUserData.GetUserData(autoscalinggroup)
    healthCheck = 'ELB' if ('ROP' in pub_server) or ('3rdParty' in pub_server) else 'EC2'

    launch_configurations = aws_autoscaling_client.describe_launch_configurations()
    scaling_configurations = aws_autoscaling_client.describe_auto_scaling_groups()

    #由于有最大100条的限制，删除多余的扩展组配置
    if (len(scaling_configurations['AutoScalingGroups'])>=90):
        raise NameError("Too many AutoScaling Group, Please REMOVE some inactive ASs!!")

    launch_cfg_list=[]
    autoscaling_list=[]
    if (len(scaling_configurations['AutoScalingGroups']) != len(launch_configurations['LaunchConfigurations'])):
        for launchcfg in launch_configurations['LaunchConfigurations']:
            launch_cfg_list.append(launchcfg['LaunchConfigurationName'])
        for autoscaling in scaling_configurations['AutoScalingGroups']:
            autoscaling_list.append(autoscaling['AutoScalingGroupName'])
        for launch_cfg in list(set(launch_cfg_list).difference(set(autoscaling_list))):
            aws_autoscaling_client.delete_launch_configuration(LaunchConfigurationName=launch_cfg)
    try:
        create_launchcfg_response = aws_autoscaling_client.create_launch_configuration(
            LaunchConfigurationName=autoscalinggroup,
            ImageId=imageid,
            KeyName=conf.SSH_PUB_KEY,
            SecurityGroups=secgroups,
            UserData=userDate,
            InstanceType=instancetype,
            AssociatePublicIpAddress=True
        )
    except:
        raise

    try:
        create_as_response = aws_autoscaling_client.create_auto_scaling_group(
        AutoScalingGroupName=autoscalinggroup,
        LaunchConfigurationName=autoscalinggroup,
        MinSize=1,
        MaxSize=200,
        DesiredCapacity=1,
        AvailabilityZones=az,  # 多可用区
        VPCZoneIdentifier=subnetid,  # 子网
        HealthCheckGracePeriod=300,
        HealthCheckType=healthCheck,
        DefaultCooldown=300,
        LoadBalancerNames=pub_lbs if ('ROP' in pub_server) or ('3rdParty' in pub_server ) else [],
        TerminationPolicies=['OldestInstance'],
        Tags=[{'Key': 'Name', 'Value':pub_server }])

        if (create_as_response['ResponseMetadata']['HTTPStatusCode'] != 200):
            raise NameError("Creat Autoscaling Group %s Fail" % autoscalinggroup)
    except:
        raise

    if (pub_server == 'Prod-RoP'):
        # 创建扩展策略
        alarm_policy=aws_autoscaling_client.put_scaling_policy(
                AutoScalingGroupName=autoscalinggroup,
                PolicyName='RoP-ELB-HTTP-Increase',
                AdjustmentType='ChangeInCapacity',
                ScalingAdjustment=2)
        ok_policy = aws_autoscaling_client.put_scaling_policy(
                AutoScalingGroupName=autoscalinggroup,
                PolicyName='RoP-ELB-HTTP-Decrease',
                AdjustmentType='ChangeInCapacity',
                ScalingAdjustment=-1)
        #定义触发条件（设置告警）
        aws_cloud_client.put_metric_alarm(
                AlarmName='ELB-Prod-RoP-Latency',
                AlarmDescription='ELB-Prod-RoP-Latency',
                ActionsEnabled=True,
                OKActions=[ok_policy,],
                AlarmActions=[alarm_policy,],
                MetricName='Latency',
                Namespace='AWS/ELB',
                Statistic='Average',
                Dimensions=[{'Name': 'LoadBalancerName', 'Value': 'Prod-env-RoP-servers-3'},],
                Period=60,
                Unit='Seconds',
                EvaluationPeriods=3,
                Threshold=0.4,
                ComparisonOperator='GreaterThanOrEqualToThreshold')

    return autoscalinggroup

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
        logdeploy.info("扩展组：%s 实例正在创建..." % as_name)
    logdeploy.info("扩展组：%s 实例创建成功..." % as_name)

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
        logdeploy.info("扩展组：%s 实例正在初始化..." % as_name)
    logdeploy.info("扩展组：%s 实例正在初始化完成..." % as_name)


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
                    break
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
                    break
            if (cnt >= 20): raise NameError("zookeeper注册检查超时")

        time.sleep(30)
        cnt = cnt + 1
        logdeploy.info("扩展组：%s 应用正在启动..." % as_name)
    logdeploy.info("扩展组：%s 应用启动完成..." % as_name)

def deploy(src_servers,version,optor):
    aws_autoscaling_client = awsservices.get_awsclient('autoscaling')
    pub_lbs=[]
    as_nows=[]
    as_news=[]
    imageidlist.clear()
    logdeploy.info('开发执行发布!!=============================================================')

    try:
        for src_server in src_servers:
            src_env = src_server.split('-')[0]
            pub_env = 'Pre' if src_env.startswith('Test')  else 'Prod'
            pub_server = "%s-%s" % (pub_env, src_server.split('-')[1])
            pub_lb=['%s-env-%s-servers' % (pub_env, src_server.split('-')[1])]
            if (pub_server == 'Prod-RoP'):  # Prod-RoP有三个负载均衡器
                pub_lb.append('Prod-env-RoP-servers-2')
                pub_lb.append('Prod-env-RoP-servers-3')
            as_now = awsservices.get_autoscalinggroup(pub_server)  #获取要发布的server当前扩展组
            as_new = create_autoscalinggroup(src_server, pub_server, version, pub_lb, optor) #关键步骤：创建新的扩展组
            as_nows.append(as_now)
            as_news.append(as_new)
            pub_lbs.append(pub_lb)

            logdeploy.info("扩展组创建成功，服务器开始启动......%s" % as_new)

        for as_new in as_news:
            wait_instances_ok(as_new)
            wait_application_ok(as_new)

    except Exception as e:
        logdeploy.info(e)
        logdeploy.info("版本发布失败,执行回滚")
        if as_news:
            for as_new in as_news:
                sql = 'INSERT INTO deploy_info(`VersionId`,`ImageId`,`AsgName`,`Env`,`Status`,`Optor`) VALUES(\'%s\',\'%s\',\'%s\',\'%s\',9,\'%s\');' % (
                    version, imageidlist[as_new], as_new, pub_env, optor)
                __ConnectDB__.ConnectDB(sql)
                aws_autoscaling_client.delete_auto_scaling_group(AutoScalingGroupName=as_new, ForceDelete=True)
        return

    logdeploy.info("版本发布完成")
    if pub_env=='Prod':
        for as_new in as_news:
            sql = 'INSERT INTO deploy_info(`VersionId`,`ImageId`,`AsgName`,`Env`,`Status`,`Optor`) VALUES(\'%s\',\'%s\',\'%s\',\'%s\',1,\'%s\');' % (
                version, imageidlist[as_new], as_new, pub_env, optor)
            __ConnectDB__.ConnectDB(sql)
            if False == as_new.startswith('Prod-PMS'):
                aws_autoscaling_client.update_auto_scaling_group(AutoScalingGroupName=as_new, MinSize=2, DesiredCapacity=2)
    for as_now in as_nows:
        aws_autoscaling_client.update_auto_scaling_group(AutoScalingGroupName=as_now, MinSize=0, DesiredCapacity=0)

    subject1 = '版本号:%s 发布成功, 交付环境: %s' % (version,pub_env)
    message = "版本号: %s 发布成功!\n发布的服务器有: %s" % (version,as_news)
    SendSNS.SendEmail(subject=subject1, message=message)
    loginfo.info("%s" % message)
    logdeploy.info("%s" % message)

def index(req):
    servers = req.GET.getlist('servers')
    version = req.GET.get('version')
    env = req.GET.get('env')
    username = req.session.get('username','anybody')
    if env.startswith('Pre'):
        pwd = req.GET.get('pwd')
        if pwd == 'A&cd!2#4':
            pass
        else:
            temp1 = '<h4>密码错误!</h4>'
            return render_to_response('deploy.html',{'username':username,'errorInfo':temp1})
    for i in range(0,len(servers)):
        servers[i] = env + servers[i]
    if username == 'anybody':
        return render_to_response('login.html',{})
    else:
        os.system('cat /dev/null > %s/lastestdeploy.log' % conf.LOGDIR)
        thread.start_new_thread(deploy,(servers,version,username))    #建立子线程，执行发布
        return render_to_response('deploylog.html',{'username':username})
