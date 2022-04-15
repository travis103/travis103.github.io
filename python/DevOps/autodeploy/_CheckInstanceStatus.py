#coding=utf-8 
#GetOldAS(server)：    获得旧的扩展组名称，用作发布成功后，对旧的实例进行清除。
#CheckASInstanceStatus(newAS)：    检查新的扩展组中实例的状态，等待时间一般为AMI的创建时间。正常后为Inservice状态。
#CheckEC2Status(instanceIds)：    检查EC2的状态，包含系统启动和自检时间。启动后为running状态。
#CheckELBStatus(instanceIds,loadbalanceName,count)：    检查实例在ELB中的状态，初始应为OutofService状态，等待实例的自启动脚本执行后，程序正常云行的话应为Inservice状态。
from functions import awsservices
from functions import _Functions
from functions import FilterResult
import time
import logging
import zookeeper
import conf

loginfo = logging.getLogger('deployinfo')
logdeploy = logging.getLogger('lastdeploy')
errorinfo = logging.getLogger('errorinfo')


#检查新的扩展组实例启动状态
#返回值InstanceIds类型为list，返回所有新扩展组中新建的实例ID

def CheckASInstanceStatus(newAS):
    instanceIds = []
    aSName = awsservices.get_awsclient('autoscaling').describe_auto_scaling_groups(AutoScalingGroupNames=newAS)
    try:
        for i in aSName['AutoScalingGroups']:
            k = 0   #判断标志位
            if i['Instances']:
                for j in i['Instances']:
                    print j['LifecycleState']
                    if (j['LifecycleState'] == 'InService'):    #Health状态切换时间非常短
                        if (j['InstanceId'] not in instanceIds):    #做一次输出限制，不重复输出已成功启动的实例结果
                            loginfo.info("扩展组: %s 状态变为: %s !!" % (j['InstanceId'],j['HealthStatus']))
                            logdeploy.info("扩展组: %s 状态变为: %s !!" % (j['InstanceId'],j['HealthStatus']))
                            instanceIds.append(j['InstanceId'])
                    else:
                        loginfo.info("扩展组: %s 当前状态不可用: %s ..." % (j['InstanceId'],j['HealthStatus']))
                        logdeploy.info("扩展组: %s 当前状态不可用: %s ..." % (j['InstanceId'],j['HealthStatus']))
                        k = 1
            else:
                getResult = awsservices.get_awsclient('autoscaling').describe_scaling_activities(AutoScalingGroupName=i['AutoScalingGroupName'])    #拿扩展组无法启动的历史事件
                if getResult['Activities']:
                    loginfo.info("扩展组: %s's 实例未创建 ...\n     原因: %s" % (i['AutoScalingGroupName'],getResult['Activities'][0]['Description'])) #获得实例无法启动的原因
                    logdeploy.info("扩展组: %s's 实例未创建 ...\n     原因: %s" % (i['AutoScalingGroupName'],getResult['Activities'][0]['Description']))
                k = 1
        if (k == 0 and len(instanceIds) == len(newAS)): #判断条件为：标志位为0，并且获得的实例数目与扩展组数目相同。
            loginfo.info("扩展组: 所有实例已创建，开始实例状态检查: %s\n" % instanceIds)
            logdeploy.info("扩展组: 所有实例已创建，开始实例状态检查: %s\n" % instanceIds)
            return instanceIds
        else:
            loginfo.info("扩展组: 等待所有实例创建成功，请耐心等待 ...\n")
            logdeploy.info("扩展组: 等待所有实例创建成功，请耐心等待 ...\n")
            time.sleep(30)
            return CheckASInstanceStatus(newAS) #循环执行，至所有新的扩展组中实例状态为Inservice为止。
    except Exception as e:
        loginfo.info(e)
        logdeploy.info(e)
        errorinfo.info(e)
        return False

#检查EC2的实例状态，输入值为实例ID，类型为list；输出值为布尔值
def CheckEC2Status(instanceIds):
    checkEC2Instances = [] #初始化检查结果，下面对该list做判断，如果和输入的instanceIds长度相当，则认为所有实例都为running状态
    try:
        instances = awsservices.get_awsclient('ec2').describe_instance_status(InstanceIds=instanceIds)
        for i in instances['InstanceStatuses']:
            if (i['InstanceStatus']['Status'] == 'ok'):
                if (i['InstanceId'] not in checkEC2Instances):
                    checkEC2Instances.append(i['InstanceId'])
                    loginfo.info("EC2: %s 启动成功！" % i['InstanceId'])
                    logdeploy.info("EC2: %s 启动成功！" % i['InstanceId'])
            else:
                loginfo.info("EC2: %s 还没启动 ..." % i['InstanceId'])
                logdeploy.info("EC2: %s 还没启动 ..." % i['InstanceId'])
        if _Functions.ListLenCompare(instanceIds, checkEC2Instances):
            loginfo.info("EC2: 所有实例启动成功，开始检查应用状态: %s\n" % checkEC2Instances)
            logdeploy.info("EC2: 所有实例启动成功，开始检查应用状态: %s\n" % checkEC2Instances)
            return True
        else:
            loginfo.info("EC2: 等待所有实例启动完成，请耐心等待 ...\n")
            logdeploy.info("EC2: 等待所有实例启动完成，请耐心等待 ...\n")
            time.sleep(15)
            return CheckEC2Status(instanceIds)
    except Exception as e:
        loginfo.info(e)
        logdeploy.info(e)
        errorinfo.info(e)
        return False

#instanceIds：    需要检查的新建实例ID。类型为list
#loadbalanceName：    需要检查的ELB名称。类型为list
#count：    计数器，超时后判定版本发布失败，进行回退。类型int
def CheckELBStatus(instanceIds,count):  
    checkELBInstances = []
    time.sleep(30)
    state = True
    try:
        ec2result = awsservices.get_awsclient('ec2').describe_instances(InstanceIds=instanceIds)
        getIPs = FilterResult.FilterResults(ec2result['Reservations'],['PrivateIpAddress','InstanceId','Tags'])
        getIPs.start()
        getIDandIP = getIPs.results
        for i in getIDandIP:
            for j in i['Tags']:
                if j['Key'] == 'Name':
                    i['Tags'] = j['Value'] #把i['Tags']替换成真正需要的实例名称比如：Pre-RoP
                else:
                    pass
            ec2Info = i['Tags'].split('-')
            if ec2Info[1] in ('RoP','3rdParty'):
                loadbalanceName = '%s-env-%s-servers' % (ec2Info[0],ec2Info[1])
                getELB = awsservices.get_awsclient('elb').describe_instance_health(LoadBalancerName=loadbalanceName)
                for j in getELB['InstanceStates']:
                    if (j['InstanceId'] in instanceIds):
                        if (j['State'] == 'InService'):
                            if (j['InstanceId'] not in checkELBInstances):
                                loginfo.info("应用检查: %s - %s 状态变为可用!" % (ec2Info[1],j['InstanceId']))
                                logdeploy.info("应用检查: %s - %s 状态变为可用!" % (ec2Info[1],j['InstanceId']))
                                checkELBInstances.append(j['InstanceId'])
                        else:
                            loginfo.info("应用检查: %s - %s 状态不可用，请耐心等待 ..." % (ec2Info[1],j['InstanceId']))
                            logdeploy.info("应用检查: %s - %s 状态不可用，请耐心等待 ..." % (ec2Info[1],j['InstanceId']))
                            state = False
            else:
                if ec2Info[0] == 'Pre':
                     host = conf.PRE_ZOOKEEP
                elif ec2Info[0] == 'Prod':
                     host = conf.PROD_ZOOKEEP
                else:
                    loginfo.info("应用检查: 环境检查失败: %s!" % ec2Info[0])
                    logdeploy.info("应用检查: 环境检查失败: %s!" % ec2Info[0])
                    return False
                try:
                    handler = zookeeper.init(host)
                    zkresult = zookeeper.get_children(handler,'/DevOps/servers/%s' % ec2Info[1])
                except Exception:
                    zkresult = []
                if i['PrivateIpAddress'] in zkresult:
                    if i['InstanceId'] not in checkELBInstances:
                        loginfo.info("应用检查: %s - %s 状态变为可用!" % (ec2Info[1],i['InstanceId']))
                        logdeploy.info("应用检查: %s - %s 状态变为可用!" % (ec2Info[1],i['InstanceId']))
                        checkELBInstances.append(i['InstanceId'])
                    else:
                        pass
                else:
                    loginfo.info("应用检查: %s - %s 状态不可用，请耐心等待 ..." % (ec2Info[1],i['InstanceId']))
                    logdeploy.info("应用检查: %s - %s 状态不可用，请耐心等待 ..." % (ec2Info[1],i['InstanceId']))
                    state = False
        if state:
            if (_Functions.ListLenCompare(instanceIds, checkELBInstances)):
                loginfo.info("应用检查: 所有应用均已提供服务！ %s...\n" % checkELBInstances)
                logdeploy.info("应用检查: 所有应用均已提供服务！ %s...\n" % checkELBInstances)
                return True
        elif (count < 15):
            loginfo.info("应用检查: 有应用尚未启动，请耐心等待 ...%s\n" % count)
            logdeploy.info("应用检查: 有应用尚未启动，请耐心等待 ...%s\n" % count)
            count += 1
            return CheckELBStatus(instanceIds,count)
        elif (count >= 15):
            return False
    except Exception as e:
        loginfo.info(e)
        logdeploy.info(e)
        errorinfo.info(e)
        return False
