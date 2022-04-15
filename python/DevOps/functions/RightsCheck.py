#coding=utf-8
from django.shortcuts import render_to_response   #返回请求模块
import __ConnectDB__

def Check(username):
    sql = 'Select `usertype` From `userinfo` Where `username` = \'%s\';' % username
    right = __ConnectDB__.ConnectDB(sql)
    if username == 'anybody':
        return False
    else:
        return right[0]['usertype']