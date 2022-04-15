#coding=utf-8
from django.shortcuts import render_to_response   #返回请求模块
import zookeeper
from urllib import unquote
import time
'''
从数据库获得所有应用服务器信息，写入数据库是为了后期可以动态管理服务器。
'''

def index(request):
    return render_to_response('_widgets.html',{})
def myWatch(handler,type,state,path):
    print "handler:"+str(handler)+",type:"+str(type)+",state:"+str(state)+",path:"
    zookeeper.get(handler,path,myWatch)
        
def Zookeeper():
    handler = zookeeper.init('54.223.200.139:2181,54.223.200.46:2181,54.223.130.146:2181')
    result = zookeeper.get_children(handler,'/DevOps/servers')
    print result
    for i in result:
        print unquote(i)
        
if __name__ == '__main__':
    Zookeeper()
