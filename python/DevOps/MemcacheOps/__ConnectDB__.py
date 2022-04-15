#coding=utf-8 
import MySQLdb
import MySQLdb.cursors
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

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
        conn.close()
        return result
    except Exception as e:
        print (e)
        