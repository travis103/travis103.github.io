#coding=utf-8 
#返回AWS定义的tag值。
def GetFilters(name):
    filter = [
            {
             'Name':'tag-key',
             'Values':['Name']
             },
            {
             'Name':'tag-value',
             'Values':[name]
             }
           ]
    return filter

#name输入值得类型为list
def GetMoreFilters(name):
    filter = [
            {
             'Name':'tag-key',
             'Values':['Name']
             },
            {
             'Name':'tag-value',
             'Values':name
             }
           ]
    return filter