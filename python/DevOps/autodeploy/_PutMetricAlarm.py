#coding=utf-8 
from functions import awsservices
import logging

loginfo = logging.getLogger('deploy')
logdeploy = logging.getLogger('lastdeploy')
logerror = logging.getLogger('errorinfo')
def GetMetricAlarm(alarmNames):
    s = awsservices.get_awsclient('cloudwatch').describe_alarms(AlarmNames=alarmNames)['MetricAlarms']
    if s:
        loginfo.info(s)
        logdeploy.info(s)
    else:
        loginfo.info('Alarm is None!')
        logdeploy.info('Alarm is None!')
        logerror.error('Alarm is None!')

def PutMetricAlarm(okPolicy,alarmPolicy):
    awsservices.get_awsclient('cloudwatch').put_metric_alarm(
                AlarmName='ELB-Prod-RoP-Latency',
                AlarmDescription='ELB-Prod-RoP-Latency',
                ActionsEnabled=True,
                OKActions=[
                    okPolicy,
                ],
                AlarmActions=[
                    alarmPolicy,
                ],
                MetricName='Latency',
                Namespace='AWS/ELB',
                Statistic='Average',
                Dimensions=[
                    {
                        'Name': 'LoadBalancerName',
                        'Value': 'Prod-env-RoP-servers-3'
                    },
                ],
                Period=60,
                Unit='Seconds',
                EvaluationPeriods=3,
                Threshold=0.4,
                ComparisonOperator='GreaterThanOrEqualToThreshold'
             )