#coding=utf-8
from functions import awsservices
from functions import FilterResult
from functions import SendEmail
import datetime

def StartInstance(instanceIds):
    dateNow = datetime.datetime.now()
    correctInstances = []
    errorInstances = []
    ec2Region = awsservices.get_awsclient('ec2')
    result = ec2Region.start_instances(InstanceIds=instanceIds)
    for i in result['StartingInstances']:
        instanceInfo = ec2Region.describe_instances(InstanceIds=[i['InstanceId']])
        datas = FilterResult.FilterResults(params=instanceInfo['Reservations'],filter=["Value"])
        datas.start()
        if i['CurrentState']['Name'] == 'pending' and i['PreviousState']['Name'] == 'shutting-down':
            correctInstances.append(datas.results[0])
        else:
            errorInstances.append(datas.results[0])
    receiver = 'kuang.brian@51onion.com'
    subject = 'Start-%s' % dateNow
    text = 'Start EC2 instances finished.\nStarted Instances are: %s\nUnStart Instances are: %s' % (correctInstances,errorInstances) 
    SendEmail.SendEmail(receiver=receiver,subject=subject,text=text)
    
def StopInstance(instanceIds):
    dateNow = datetime.datetime.now()
    correctInstances = []
    errorInstances = []
    ec2Region = awsservices.get_awsclient('ec2')
    result = ec2Region.stop_instances(InstanceIds=instanceIds)
    for i in result['StoppingInstances']:
        instanceInfo = ec2Region.describe_instances(InstanceIds=[i['InstanceId']])
        datas = FilterResult.FilterResults(params=instanceInfo['Reservations'],filter=["Value"])
        datas.start()
        if i['CurrentState']['Name'] == 'stopping' and i['PreviousState']['Name'] == 'running':
            correctInstances.append(datas.results[0])
        else:
            errorInstances.append(datas.results[0])
    receiver1 = 'kuang.brian@51onion.com'
    subject1 = 'Stop-%s' % dateNow
    text1 = 'Stop EC2 instances finished.\nStarted Instances are: %s\nUnStop Instances are: %s' % (correctInstances,errorInstances) 
    SendEmail.SendEmail(receiver=receiver1,subject=subject1,text=text1)