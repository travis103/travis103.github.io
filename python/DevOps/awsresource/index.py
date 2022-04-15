#coding=utf-8 
from django.template import loader,Context  #本地文件导入和渲染模块
from django.http.response import HttpResponse   #返回请求模块

def index(req):

    temp = loader.get_template('userlogin.html')

    cont = Context({})    #对应html页面中的变量格式为：{{title}}和{{user}}
    return HttpResponse(temp.render(cont))