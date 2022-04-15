#coding=utf-8
from django.template import loader,Context,Template  #本地文件导入和渲染模块
from django.http.response import HttpResponse   #返回请求模块
import conf

def index(req):
    contents = open('%s/lastestdeploy.log' % conf.LOGDIR,'r')
    line = contents.readlines()
    cont = Context({'conts':line})
    temp = Template('{% for i in conts %}<li>{{i}}</li>{% endfor %}')
    return HttpResponse(temp.render(cont))
