#coding=utf-8 
import logging

import awsservices

logerror = logging.getLogger('error')
def getCredentials(service, resourceorclient):
    #配置证书
    if resourceorclient=='resource':
        serRegion = awsservices.get_resource(service)
    elif resourceorclient=='client':
        serRegion = awsservices.get_awsclient(service)
    else:
        logerror.error("Param Error!!")
    return serRegion