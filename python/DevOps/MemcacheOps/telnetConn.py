#coding=utf-8
import telnetlib
from django.http.response import HttpResponse   #返回请求模块
from functions import SendEmail
from functions import __ConnectDB__
import getResults
import logging

loginfo = logging.getLogger('memcacheinfo')

COUNT = {}
COUNT['matched'] = 0
COUNT['notmatched'] = 0 
COUNT['total'] = 0

def getUserIds(host, port, allUserIds, attr, userName,addr):
    try:
        getEmailSQL = "SELECT `email` FROM `userinfo` WHERE `username`=\'%s\'" % userName
        email = __ConnectDB__.ConnectDB(getEmailSQL)
        matched = 0
        notmatched = 0
        total = len(allUserIds)
        try:
            threads = []
            userIds = []
            countDown = len(allUserIds)/30
            for i in allUserIds: #从上传的文件中获得数据，如果单个文件超过2.4M，则进行分片操作。
                userIds.append(i) #用户过多的时候，不确定数组是否能够撑住...待优化
                if len(userIds) == countDown:
                    threads.append({'func':telnetConn,'args':(host, port, userIds, attr, userName)})
                    userIds = []
            threads.append({'func':telnetConn,'args':(host, port, userIds, attr, userName)})
            newThread = getResults.NumThread()
            newThread.set_thread_func_list(threads,COUNT)
            newThread.start()
            #         '''发送成功邮件'''
            subject = '%s，Deleted User\'s Memcache Success' % userName
            text = 'Dear %s，\n Deleted User\'s Memcache Success，Matched%s，Not Matched%s。\n Env: %s' % (userName,COUNT['matched'],COUNT['notmatched'],addr)
            SendEmail.SendEmail(email[0]['email'], subject, text)
            result = 'Success'
        except Exception as e:
            '''发送失败邮件'''
            subject = '%s，Delete User\'s Memcache Fail' % userName
            #失败邮件内容：用户名，匹配次数，不匹配次数，报错原因
            text = 'Dear %s，\n Deleted User\'s Memcache Fail，Matched%s，Not Matched%s。\n Env: %s\n Reason：%s' % (userName,COUNT['matched'],COUNT['notmatched'],addr,e)
            SendEmail.SendEmail(email[0]['email'], subject, text)
            result = 'Failed'
        attr = ','.join(attr)
        #sql 中的 total 不是总执行次数，而是用户 ID 的总数
        resultSQL = 'Insert Into `Audit_Memcache`(`staff_name`,`attr`,`result`,`matched`,`notmatched`,`total`,`env`) Values(\'%s\',\'%s\',\'%s\',%s,%s,%s,\'%s\');' % (userName,attr,result,COUNT['matched'],COUNT['notmatched'],total,addr)
        __ConnectDB__.ConnectDB(resultSQL)
    except Exception as e:
        loginfo.info(e)

'''
host为缓存服务器地址，可以是域名或者IP
port为缓存服务器端口，默认为11211
userIds为UploadFile对象，有如下方法：
UploadFile.read(),从文件中读取全部上传数据。当上传文件过大时，可能会耗尽内存，慎用。
UploadFile.multiple_chunks(),如上传文件足够大，要分成多个部分读入时，返回True.默认情况,当上传文件大于2.5M时，返回True。但这一个值可以配置。
UploadFile.chunks(),返回一个上传文件的分块生成器。如multiple_chunks()返回True,必须在循环中使用chrunks()来代替read()。一般情况下直接使用chunks()就行。
UploadFile.size(),上传文件的文件名
UploadFile.name()，上传文件的文件大小（字节）

attr为用户缓存属性，如下：
attr:'avatar_',用户扩展纪录缓存，包括 昵称、头像等字段
    'db_user_basic_',用户基本表，包括 手机号、姓名、状态等
    'db_user_circle_',用户联盟信息记录，包括下级人数等
    'clientId_',没看到应用
    'db_user_dynamic_',用户账户信息，包括投资余额等
'''    
def telnetConn(host,port,userIds,attr,userName):
    try:
        match = 0 #统计执行匹配的次数
        notMatch = 0 #统计执行不匹配的次数
        t=telnetlib.Telnet() #建立实例
        t.open(host=host,port=port) #建立缓存服务器连接
        for i in userIds:
            if i:
                for j in attr: #获得每个用户需要删除的属性
                    t.write('delete %s%s\n' % (str(j),str(i))) #循环执行，每个用户和所有属性
                    result=t.read_until('DELETED',timeout=0.5)
                    if result.startswith('NOT_FOUND'):
                        notMatch+=1
                        COUNT['notmatched'] += 1
                    else:
                        match+=1
                        COUNT['matched'] += 1
            else:
                pass
        return match,notMatch
    except Exception as e:
        print e
        return False,False
        