#coding=utf-8
import boto3
import conf

def get_credentials(local=False):
    if(local==True):
        credentials={"AccessKeyId" : conf.ACCESS_ID,
                     "SecretAccessKey" : conf.ACCESS_KEY,
                     "SessionToken" : ""}
    else:
        sts_client = boto3.client('sts')
        assumedRoleObject = sts_client.assume_role(
            RoleArn="arn:aws-cn:iam::303361436695:role/devops",
            RoleSessionName="AssumeRoleSession1"
        )
        credentials = assumedRoleObject['Credentials']
    return credentials

def get_resource(resource):
    credentials = get_credentials(local=conf.LOCAL)
    resource_handle = boto3.resource(resource,
                                     aws_access_key_id = credentials['AccessKeyId'],
                                     aws_secret_access_key = credentials['SecretAccessKey'],
                                     aws_session_token = credentials['SessionToken'])
    return resource_handle

def get_awsclient(resource):
    credentials = get_credentials(local=conf.LOCAL)
    ec2_handle = boto3.client(resource,
                              aws_access_key_id=credentials['AccessKeyId'],
                              aws_secret_access_key=credentials['SecretAccessKey'],
                              aws_session_token=credentials['SessionToken'])
    return ec2_handle


def get_autoscalinggroup(server):

    autoscalinggroups = get_awsclient('autoscaling').describe_auto_scaling_groups()
    result=[]
    for asg in autoscalinggroups['AutoScalingGroups']:
        if (asg['DesiredCapacity'] != 0 and asg['AutoScalingGroupName'].startswith(server)):
            result.append(asg['AutoScalingGroupName'])
    if (len(result) == 1):
        return result[0]
    else:
        raise Exception("错误!! %s 该类型服务器有多个扩展组: %s" % (server,result))

"""
获取安全组信息
server：server名，例如：Pre-SoA
inf:想要获取的安全组信息，可填：securityGroupIds，subnetIds，aZs
"""
def get_secgroup(server, inf):
    filter =[{'Name': 'tag-key','Values': ['Name']},{'Name': 'tag-value','Values': [server]},
             {'Name': 'instance-state-name','Values': ['running']}]

    instances_params = get_awsclient('ec2').describe_instances(Filters=filter)

    # 初始化参数
    subnetIds = []
    aZs = []
    securityGroupIds = []

    for reservation in instances_params['Reservations']:
        for instance in reservation['Instances']:
            if (inf == 'subnetIds'):
                subnetId = instance['SubnetId']
                if (subnetId not in subnetIds):  # 如果目标环境有两台在同一区域的服务器，会导致无法创建扩展组
                    subnetIds.append(subnetId)
                delimiter = ','
                result = delimiter.join(subnetIds)  # 返回值需要为字符串
            elif (inf == 'aZs'):
                az = instance['Placement']['AvailabilityZone']
                aZs.append(az)
                result = aZs  # 返回值为list
            elif (inf == 'securityGroupIds'):
                for securityGroup in instance['SecurityGroups']:
                    securityGroupIds.append(securityGroup['GroupId'])
                result = list(set(securityGroupIds))  # 返回值为list，如果对端有多台服务器，会重复拿到安全组Id，使用set清除重复的
    return result

"""
获取预发布或测试环境server的instance id
默认只有一个处于sunning状态的实例
"""
def get_instanceid(server):
    filter = [{'Name': 'tag-key', 'Values': ['Name']}, {'Name': 'tag-value', 'Values': [server]},
              {'Name': 'instance-state-name','Values': ['running']}]
    instances_params = get_awsclient('ec2').describe_instances(Filters=filter)
    for reservation in instances_params['Reservations']:
        for instance in reservation['Instances']:
            instanceid = instance['InstanceId']
    return instanceid


"""
获取某个扩展组实例状态
"""
def get_inservice_instance(as_name):
    instanceIds = []
    try:
        as_group_des = get_awsclient('autoscaling').describe_auto_scaling_groups(AutoScalingGroupNames=[as_name])
        as_group = as_group_des['AutoScalingGroups'][0]
    except:
        raise

    if as_group['Instances']:
        for instance in as_group['Instances']:
            if (instance['LifecycleState'] != 'InService'):    #Health状态切换时间非常短
                return False
            else:
                instanceIds.append(instance['InstanceId'])
    return instanceIds


#检查EC2的实例状态，输入值为实例ID，类型为list；输出值为布尔值
def check_instance_ok(instanceIds):
    try:
        instances_des = get_awsclient('ec2').describe_instance_status(InstanceIds=instanceIds)
    except:
        raise

    for instancestatuse in instances_des['InstanceStatuses']:
        if (instancestatuse['InstanceStatus']['Status'] != 'ok'):
            return False
    return True

