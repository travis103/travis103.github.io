#coding=utf-8
from django.shortcuts import render_to_response   #返回请求模块
from functions import __ConnectDB__
from functions import RightsCheck

def GetInfo(req):
    username = req.session.get('username','anybody')
    if username == 'anybody':
        return render_to_response('login.html',{})
    else:
        right = RightsCheck.Check(username)
        sql = 'Select `email` From `userinfo` Where `username` = \'%s\';' % username
        results = __ConnectDB__.ConnectDB(sql)
        email = results[0]['email']
        return render_to_response('userProfile.html',{'email':email,'username':username,'right':right})
    
def ModifyUser(req):
    username = req.session.get('username','anybody')
    if username == 'anybody':
        return render_to_response('login.html',{})
    else:
        pwd = req.POST.get('pwd')
        email = req.POST.get('email')
        right = RightsCheck.Check(username)
        sql = "Update `userinfo` Set `pwd` = \'%s\' Where `username` = \'%s\';" % (pwd,username)
        __ConnectDB__.ConnectDB(sql)
        return render_to_response('userProfile.html',{'email':email,'username':username,'result':"修改密码成功！",'right':right})











