#coding=utf-8 

def GetDBs():
    '''
    @summary: 后面的数字用来做前端排序
    '''
    dbs = {'prod-mysql-application':['生产数据库',1],
           'pre-mysql-application':['预发布数据库',2],
           'app-db-dev':['联调数据库',3],
           'test-mysql-production-databases':['测试1数据库',4],
           'test2-mysql-application':['测试2数据库',5]}
    return dbs