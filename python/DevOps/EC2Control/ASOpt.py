#coding=utf-8
from functions import Credentials
from functions import __ConnectDB__
import sys

'''
        数据库InstanceStatus：0：实例不会自动关闭
                        1：实例加入自动关闭列表
                        2：扩展组不会自动关闭
                        3：扩展组加入自动关闭列表
'''

def CloseAS():
    asRegion = Credentials.getCredentials('autoscaling', 'client')
    getASs = asRegion.describe_auto_scaling_groups()
    values = ""
    for i in getASs['AutoScalingGroups']:
        if i['AutoScalingGroupName'].startswith('Pre-') and i['DesiredCapacity'] != 0:
            asRegion.update_auto_scaling_group(AutoScalingGroupName=i['AutoScalingGroupName'],
                                               MinSize=0,
                                               DesiredCapacity=0)
            instanceTypes = asRegion.describe_launch_configurations(LaunchConfigurationNames=[i['AutoScalingGroupName']])
            instanceType = instanceTypes['LaunchConfigurations'][0]['InstanceType']
            if values:
                values = values + ",('autoScaling',\'%s\',\'%s\',3)" % (i['AutoScalingGroupName'],instanceType)
            else:
                values = "('autoScaling',\'%s\',\'%s\',3)" % (i['AutoScalingGroupName'],instanceType)
    sql = "Insert Into `EC2_CONTROL` (`InstanceId`,`InstanceName`,`InstanceType`,`InstanceStatus`) Values %s;COMMIT;" % values
    __ConnectDB__.ConnectDB(sql)

def ChzAS():
    asRegion = Credentials.getCredentials('autoscaling', 'client')
    sql = "Select `InstanceName` From `EC2_CONTROL` Where `InstanceId` = \'autoScaling\' And `InstanceStatus` = 3;"
    aSInfos = __ConnectDB__.ConnectDB(sql)
    values = ""
    for aSinfo in aSInfos:
        asRegion.update_auto_scaling_group(AutoScalingGroupName=aSinfo['InstanceName'],
                                               MinSize=1,
                                               DesiredCapacity=1)
        if values:
            values = values + ",\'%s\'" % aSinfo['InstanceName']
        else:
            values = "\'%s\'" % aSinfo['InstanceName']
    sql = "Update `EC2_CONTROL` Set `InstanceStatus` = 2 Where `InstanceName` In (%s);COMMIT;" % values
    __ConnectDB__.ConnectDB(sql)
    
if __name__ == '__main__':
    optType=sys.argv[1]
    if optType == 'start':
        ChzAS()
    if optType == 'stop':
        CloseAS()
    else:
        print 'Error!'
        exit