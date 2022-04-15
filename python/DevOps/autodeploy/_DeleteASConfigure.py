#coding=utf-8 
from functions import awsservices
from functions import __ConnectDB__
import logging

loginfo = logging.getLogger('deploy')
logdeploy = logging.getLogger('lastdeploy')

def __init__():
    launchConfigurationNames = []
    result = CheckASConfigure()
    if result:
        for i in result['LaunchConfigurations']:
            launchConfigurationNames.append(i['LaunchConfigurationName'])
        for launchConfigurationName in launchConfigurationNames:
            try:
                DeleteASConfigure(launchConfigurationName)
                loginfo.info("Delete AS Configure: %s" % launchConfigurationName)
                logdeploy.info("Delete AS Configure: %s" % launchConfigurationName)
                sql = 'UPDATE deploy_info SET `Status`=5 WHERE `AsgName`=\'%s\' AND `Status`!=9;' % launchConfigurationName #状态5为扩展组已删除
                __ConnectDB__.ConnectDB(sql)
            except:
                pass

def DeleteASConfigure(launchConfigurationName):
    awsservices.get_awsclient('autoscaling').delete_launch_configuration(LaunchConfigurationName=launchConfigurationName)

def CheckASConfigure():
    aS = awsservices.get_awsclient('autoscaling').describe_auto_scaling_groups()
    aSCfg = awsservices.get_awsclient('autoscaling').describe_launch_configurations()
    if (len(aS['AutoScalingGroups']) == len(aSCfg['LaunchConfigurations'])):
        if len(aSCfg['LaunchConfigurations']) >= 90:
            loginfo.info("Too many AutoScaling Group, Please REMOVE some inactive ASs!!")
            logdeploy.info("Too many AutoScaling Group, Please REMOVE some inactive ASs!!")
        return False
    else:
        return aSCfg
    