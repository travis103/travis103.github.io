#coding=utf-8 
def GetFilters(name):
    filter = [
            {
             'Name':'snapshot',
             'Values':[name]
             }
           ]
    return filter