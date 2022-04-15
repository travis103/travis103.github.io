#coding=utf-8

SSH_PUB_KEY='Dev-Key-China-Brian'

DEVOPS_DB_HOST='other-db.cofh1myagdtp.rds.cn-north-1.amazonaws.com.cn'
DEVOPS_DB='aws_resource'
DEVOPS_DB_USER='devops'
DEVOPS_DB_PWD='.ehLHuOo(1@84H3'

#Local代表是否在本地执行，在服务器上运行为False，把代码下到本地运行为True。下到本地时需要指定ACCESS_ID 和 ACCESS_KEY
LOCAL=True

ACCESS_ID='AKIAOGQB7DGGMWLGVBDA'
ACCESS_KEY='Jk1iuWyTmkhd2ZElsYwmQqFr4yBDM/cueKhwJqGs'

if LOCAL==True:
    LOGDIR='/Users/onion/Documents/yunwei/DevOps/logs'
else:
    LOGDIR='/home/ec2-user/DevOps/logs'

if True==LOCAL:
    PRE_ZOOKEEP='54.223.200.139:2181,54.223.200.46:2181,54.223.130.146:2181'
    PROD_ZOOKEEP='54.223.221.160:2181,54.223.232.138:2181,54.223.238.211:2181,54.223.203.103:2181'
else:
    PRE_ZOOKEEP='10.20.37.5:2181,10.20.37.6:2181,10.20.37.7:2181'
    PROD_ZOOKEEP='10.30.36.5:2181,10.30.38.6:2181,10.30.36.7:2181,10.30.38.8:2181'
