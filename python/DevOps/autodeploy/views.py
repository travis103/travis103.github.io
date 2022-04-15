#coding=utf-8
from django.template import loader,Context  #本地文件导入和渲染模块
from django.shortcuts import render_to_response   #返回请求模块
from django.http import HttpResponse,HttpResponseRedirect
from django import forms
from functions import __ConnectDB__
from functions import RightsCheck
import logging

loginfo = logging.getLogger('info')

class UserForm(forms.Form):
    username = forms.CharField()

#用户登录
def login(req):
    username = req.session.get('username','anybody')
    if username == 'anybody':
        if req.method == "POST":
            uf = UserForm(req.POST)
            if uf.is_valid():
                dbusername = req.POST.get('username')
                sql = 'Select `pwd` From `userinfo` Where `username` = \'%s\' And `usertype` >= 0;' % dbusername
                pwd = __ConnectDB__.ConnectDB(sql)
                if req.POST.get('password') == pwd[0]['pwd']: 
                    username = uf.cleaned_data['username']
                    #把获取表单的用户名传递给session对象
                    req.session['username'] = username
                    loginfo.info("Login Successed, User: %s" % dbusername)
                    return HttpResponseRedirect('/autodeploy/index/')
                else:
                    errorInfo = '用户名或密码错误！'
                    loginfo.info("Login Failed, User: %s" % dbusername)
                    return render_to_response('login.html',{'uf':uf,'errorInfo':errorInfo})
        else:
            uf = UserForm()
        return render_to_response('login.html',{'uf':uf})
    else:
        right = RightsCheck.Check(username)
        return render_to_response('index.html',{'username':username,'right':right})

#获得用户session
def index(req):
    username = req.session.get('username','anybody')
    right = RightsCheck.Check(username)
    if username == 'anybody':
        return render_to_response('login.html',{})
    else:
        return render_to_response('index.html',{'right':right,'username':username})

#登出
def logout(req):
    loginfo.info("Logout, User: %s" % req.session.get('username'))
    del req.session['username']  #删除session
    return render_to_response('login.html',{})

'''
从数据库获得所有应用服务器信息，写入数据库是为了后期可以动态管理服务器。
'''
#获得历史版本发布信息
def GetServersInfo():
    sql = 'Select `Server_Name` From `Deploy_Server_Info`;'
    getResult = __ConnectDB__.ConnectDB(sql)
    return getResult

#跳转到版本发布页面
def autodeploy(req):
    username = req.session.get('username','anybody')
    right = RightsCheck.Check(username)
    if username == 'anybody':
        return render_to_response('login.html',{})
    elif right == 10 or right == 100:
        getServers = GetServersInfo()
        serversName = []
        for i in getServers:
            serversName.append(i['Server_Name'])
        return render_to_response('deploy.html',{'serversInfo':serversName,'username':username,'right':right})
    else:
        return render_to_response('login.html',{'errorInfo':'未授权的操作'})

#跳转到版本发布日志查询页面
def deploylog(req):
    username = req.session.get('username','anybody')
    right = RightsCheck.Check(username)
    if username == 'anybody':
        return render_to_response('login.html',{})
    elif right == 10 or right == 100:
        return render_to_response('deploylog.html',{'username':username})
    else:
        return render_to_response('login.html',{'errorInfo':'未授权的操作'})

# from django.shortcuts import render_to_response #直接使用，返回类型为render_to_response(temp,cont)


'''html中if的判断格式：
    {% if %}
    {% else %}
    {% endif %}
    1. 不能使用or and
    2. 不能使用()
'''
    
'''html中的for：
    {% for $var in []%}
    {% endfor %}
    
   forloop参数：
    {{forloop.counter}}.{{k}}{{v}}
    效果：
    1. k1 v1
    2. k2 v2
    
   for也可以做判断：for ... empty
    {% for i in [] %}
    {% empty %}    #如果循环为空，则执行empty中的内容
    
    
    一个dict的笔记：
    {% for k,v in user.items %} k是key，v是value，直接输出
    {% endfor %}
'''

'''通过url.py可以进行传参
    url(r'^blog/index/\d{字符串长度}/$','工程目录.文件.函数') #传参值为函数括号中的参数设定
'''