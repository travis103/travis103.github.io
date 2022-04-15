#coding=utf-8 
import MySQLdb
import MySQLdb.cursors
import sys
'''解决数据库编码问题'''
reload(sys)
sys.setdefaultencoding('utf-8')

'''用作用户认证和信息记录'''
def ConnectDB(sql):
    conn = MySQLdb.connect(host='other-db.cofh1myagdtp.rds.cn-north-1.amazonaws.com.cn',
                           user='devops',
                           passwd='.ehLHuOo(1@84H3',
                           db='aws_resource',
                           charset='utf8',
                           cursorclass=MySQLdb.cursors.DictCursor)
    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        conn.commit()
        conn.close()
        return result
    except Exception as e:
        print (e)

'''创建完数据库后，对allen这个用户授权写权限使用'''
def GrantDB(sql,host):
    conn = MySQLdb.connect(host=host,
                           user='root',
                           passwd='%daitou@Appmysqlroot01',
                           db='ALA_ONION',
                           charset='utf8',
                           cursorclass=MySQLdb.cursors.DictCursor)
    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        conn.close()
        return result
    except Exception as e:
        print (e)