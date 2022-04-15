#coding=utf-8 
from django.http.response import HttpResponseRedirect   #返回请求模块
from django.shortcuts import render_to_response   #返回请求模块
import telnetConn
import thread
from functions import RightsCheck
import logging

loginfo = logging.getLogger('memcacheinfo')

def Delete(req):
    try:
        '''用户身份验证'''
        username = req.session.get('username','anybody')
        if username == 'anybody':
            return render_to_response('login.html',{})
        else:
            pass
        if 'userIds' in req.FILES:
            getFile = req.FILES['userIds'] #获得待删除的用户IDs，类型为FILES
            userIds = getFile.read().split()
        else:
            userIds = []
        useridList = req.POST.get('useridList').split()
        attr = req.POST.getlist('attr') #获得待删除的用户缓存属性，类型为LIST
        addr = req.POST.get('addr') #获得待执行的缓存环境名。pre, prod, test1, test2, dev
        port = 11211 #缓存服务器端口
        if attr:
            pass
        else:
            result = '请选择需要删除的属性'
            return render_to_response('memcache.html',{'username':username,'result':result})
        right = RightsCheck.Check(username)
        if addr == 'prod' and (right == 10 or right == 100):
            host = 'prod-memcache.0xekmi.cfg.cnn1.cache.amazonaws.com.cn'
        elif addr == 'pre':
            host = 'pre-memcache.0xekmi.cfg.cnn1.cache.amazonaws.com.cn'
        elif addr == 'test1':
            host = 'test-memcache.0xekmi.cfg.cnn1.cache.amazonaws.com.cn'
        elif addr == 'test2':
            host = 'test2-memcache.0xekmi.cfg.cnn1.cache.amazonaws.com.cn'
        elif addr == 'dev':
    #         host = '54.223.164.243'
            host = 'memcache1-0.0xekmi.cfg.cnn1.cache.amazonaws.com.cn'
        else:
            print ('Env. Error!!')
            result = '环境选择错误 or 没有相应权限'
            loginfo.info('环境选择错误 or 没有相应权限:')
            return render_to_response('memcache.html',{'username':username,'result':result})
        userIds.extend(useridList)
        telnetConn.COUNT['total'] = len(userIds)*len(attr)
        telnetConn.COUNT['matched'] = 0
        telnetConn.COUNT['notmatched'] = 0
        thread.start_new_thread(telnetConn.getUserIds, (host, port, userIds, attr, username,addr))
        return HttpResponseRedirect('/memcache/index/')
    except Exception as e:
        loginfo.info(e)

'''
@summary: 跳转到进度查询页面
'''
def Index(req):
    '''用户身份验证'''
    username = req.session.get('username','anybody')
    if username == 'anybody':
        return render_to_response('login.html',{})
    else:
        pass
    right = RightsCheck.Check(username)
    return render_to_response('checkresult.html',{'username':username,'right':right})

'''
@summary: 跳转到操作页面
'''
def OptIndex(req):
    '''用户身份验证'''
    username = req.session.get('username','anybody')
    if username == 'anybody':
        return render_to_response('login.html',{})
    else:
        pass
    right = RightsCheck.Check(username)
    return render_to_response('memcache.html',{'username':username,'right':right})
