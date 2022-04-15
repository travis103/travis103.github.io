#coding=utf-8

class FilterResults(object):
    '''根据输入项，过滤出filter所输入的值
    filter为字典的key值，类型为list
    params为需要从中筛出key值的原数据，类型为list
    datas为输出值，在__init__中初始化为空，类型为list
    可以返回同一字典下的多个key参数，包括其中数组中再包含的字典key参数
    '''
    def __init__(self,params,filter):
        self.filter = filter
        self.params = params
        self.result = {}
        self.results = []
    
    def GetInfo(self,params):
        if isinstance(params, dict):
            for i in self.filter:
                if params.has_key(i) and i not in self.result.keys():
                    self.result[i] = params[i]
                else:
                    for key,value in params.items():
                        self.GetInfo(value)
        elif isinstance(params, list):
            for i in params:
                self.GetInfo(i)
        else:
            pass
    
    '''
            初始化输入
            根据输入项，过滤出filter所输入的值
        filter为字典的key值，类型为list
        params为需要从中筛出key值的一串数据，可以是数组或者字典类型
    '''
    def start(self):
        if isinstance(self.params, list):
            for i in self.params:
#                 if self.result:
#                     self.results.append(self.result)
#                     self.result = {}
                self.GetInfo(i)
                self.results.append(self.result)
                self.result = {}
        else:
            pass
    def end(self):
        #返回的值为需要筛选的key值集合，[{key1,key2,key3},{},{}...]
        return self.resutls
   
# filter = ['InstanceId','Name','PrivateIpAddress','Status']
# params = region.describe_instances()
# test = FilterResults(filter=filter,params=params['Reservations'])
# test.start()
# haha = test.results
# for i in haha:
#     print i