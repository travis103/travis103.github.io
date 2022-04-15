#coding=utf-8 
'''
单独执行！！
用来删除多余的快照，节约成本
'''
from functions import __ConnectDB__
from functions import awsservices
import logging
from django.shortcuts import render_to_response   #返回请求模块

def DeleteSnapshot():
    loginfo = logging.getLogger('info')
    snapshotIds = []
    ec2Region = awsservices.get_awsclient('ec2')
    result = ec2Region.describe_images(Owners=['303361436695'])
    for images in result['Images']:
        for i in images['BlockDeviceMappings']:
            snapshotIds.append(i['Ebs']['SnapshotId'])
    print snapshotIds
    #筛选EBS快照
    getSnapshotIds = ec2Region.describe_snapshots(OwnerIds=['303361436695'])
    for s in getSnapshotIds['Snapshots']:
        if s['SnapshotId'] not in snapshotIds:
            print s['SnapshotId']
            #删除无用的快照
            ec2Region.delete_snapshot(SnapshotId=s['SnapshotId'])
            loginfo.info("Delete %s" % s['SnapshotId'])

def DeleteAMI(req):  
    username = req.session.get('username','anybody')
    if username == 'anybody':
        return render_to_response('login.html',{})
    else:
        loginfo = logging.getLogger('info')
        ec2Region = awsservices.get_awsclient('ec2')
        errorAMIs = []
        results = ['删除AMIs成功。']
        #镜像创建时间超过1个月的才删除...别再自己删了...
        getAMIs = req.GET.getlist('imageid')
        for aMIId in getAMIs:
            try:
                ec2Region.deregister_image(ImageId=aMIId)
            except Exception as e:
                errorAMIs.append("%s, Reason: %s" % (aMIId,e))
                results.append("Error AMIs: %s, Reason: %s" % (aMIId,e))
            #删除镜像后，将数据库状态设置为10，彻底删除
            sqlUpdStatus = 'UPDATE `deploy_info` SET `Status`=10 WHERE `ImageId`=\'%s\';' % aMIId
            __ConnectDB__.ConnectDB(sqlUpdStatus)
        DeleteSnapshot()
        loginfo.info("Error AMIs: %s" % errorAMIs)
        return render_to_response('amiMngresults.html',{'errorInfo':results,'username':username})