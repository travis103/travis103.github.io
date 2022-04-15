#coding=utf-8 
import awsservices
import logging
#topic：String：SNS中的主题，格式为：'arn:aws-cn:sns:cn-north-1:303361436695:Managers_ALL'，后面的Managers_ALL是主题名称
#subject：String：这个是邮件的主题
#message：String：这个是邮件正文，换行使用\n
def SendEmail(topic='arn:aws-cn:sns:cn-north-1:303361436695:dynamodb',subject='',message=''):
    loginfo = logging.getLogger('deploy')
    logdeploy = logging.getLogger('lastdeploy')
    logerror = logging.getLogger('errorinfo')
    try:
        loginfo.info("Mail Sent: %s" % subject)
        logdeploy.info("Mail Sent: %s" % subject)
        awsservices.get_awsclient('sns').publish(TopicArn=topic,Message=message,Subject=subject)
    except Exception as e:
        loginfo.info("Mail Error: %s" % e)
        logdeploy.info("Mail Error: %s" % e)
        logerror.info("Mail Error: %s" % e)