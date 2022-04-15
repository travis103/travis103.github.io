#coding=utf-8 
#import boto.ec2.securitygroup
from functions import awsservices

def GetSecurityGroup(filter):
# 返回值为dict，如下：
# {'ResponseMetadata': {'HTTPStatusCode': 200, 'RequestId': 'bb21ad56-6ec2-46bc-9fab-63e8e05805d8'}, 'SecurityGroups': [{'IpPermissionsEgress': [{'UserIdGroupPairs': [], 'PrefixListIds': [], 'IpRanges': [{'CidrIp': '54.222.0.0/16'}], 'IpProtocol': 'tcp', 'ToPort': 65535, 'FromPort': 0}], 'GroupName': 'Pre-RoP', 'VpcId': 'vpc-fba8b799', 'GroupId': 'sg-6fc7260a', 'Tags': [{'Key': 'Name', 'Value': 'Pre-RoP'}, {'Key': '名称', 'Value': 'Pre-RoP'}], 'IpPermissions': [{'UserIdGroupPairs': [], 'PrefixListIds': [], 'IpRanges': [{'CidrIp': '0.0.0.0/0'}], 'IpProtocol': 'tcp', 'ToPort': 80, 'FromPort': 80}, {'UserIdGroupPairs': [], 'PrefixListIds': [], 'IpRanges': [{'CidrIp': '0.0.0.0/0'}], 'IpProtocol': 'tcp', 'ToPort': 8888, 'FromPort': 8888}, {'UserIdGroupPairs': [], 'PrefixListIds': [], 'IpRanges': [{'CidrIp': '58.250.82.16/32'}], 'IpProtocol': 'tcp', 'ToPort': 22, 'FromPort': 22}, {'UserIdGroupPairs': [], 'PrefixListIds': [], 'IpRanges': [{'CidrIp': '0.0.0.0/0'}], 'IpProtocol': 'tcp', 'ToPort': 443, 'FromPort': 443}], 'OwnerId': '303361436695', 'Description': 'Pre-RoP'}]}
# ex:SecurityGroupId = getCredential['SecurityGroups'][0]['GroupId']
    getCredential = awsservices.get_awsclient('ec2').describe_security_groups(Filters=filter)
    return getCredential
