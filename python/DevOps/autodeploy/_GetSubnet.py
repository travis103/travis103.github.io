#coding=utf-8 
from functions import awsservices

'''action： 的合法参数为：
    subnetIds, 返回值为子网Id（string）
    aZs, 返回值可用区（list）
    securityGroupIds，返回值安全组Id（list）'''
def GetSubnet(filter,action):
    #添加过滤条件为运行中实例
    filter1 = {
               'Name':'instance-state-name',
               'Values':['running']
               }
    filter.append(filter1)
    
    #获得reservations
    getParams = awsservices.get_awsclient('ec2').describe_instances(Filters=filter)
    
    #初始化参数
    subnetIds = []
    aZs = []
    securityGroupIds = []
    
    for i in getParams['Reservations']:
        for j in i['Instances']:
            if (action == 'subnetIds'):
                subnetId = j['SubnetId']
                if (subnetId not in subnetIds): #如果目标环境有两台在同一区域的服务器，会导致无法创建扩展组
                    subnetIds.append(subnetId)
                delimiter = ','
                result = delimiter.join(subnetIds)  #返回值需要为字符串
            elif (action == 'aZs'):
                az = j['Placement']['AvailabilityZone']
                aZs.append(az)
                result = aZs    #返回值为list
            elif (action == 'securityGroupIds'):                
                for securityGroup in j['SecurityGroups']:
                    securityGroupIds.append(securityGroup['GroupId'])
                result = list(set(securityGroupIds))    #返回值为list，如果对端有多台服务器，会重复拿到安全组Id，使用set清除重复的
    return result