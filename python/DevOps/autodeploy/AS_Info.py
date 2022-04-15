#coding=utf-8 
from functions import FilterResult
import logging

class SplitASInfo(object):
    def __init__(self, aSInfo, env):
        self.aSInfo = aSInfo
        self.aSEnv = env
        self.baseServer = {}
        self.logError = logging.getLogger('errorinfo')
    
    def SplitByMin(self):
        datas = FilterResult.FilterResults(params=self.aSInfo, filter=["AutoScalingGroupName","DesiredCapacity","CreatedTime"])
        datas.start()
        for i in datas.results:
            try:
                splitInfos = i['AutoScalingGroupName'].split('-')
                server = splitInfos[1]
                aSVersion = splitInfos[-1]
                if splitInfos[0] == self.aSEnv:
                    if self.baseServer.has_key(server): #如果该服务器类型为首次收录，则使用=号赋值，否则使用append赋值
                        self.baseServer[server].append(
                            (
                                i["AutoScalingGroupName"],  #该扩展组的第一个参数：扩展组名称
                                i['DesiredCapacity'], #该扩展组的第二个参数：通过期望的实例数来判断是否为active的扩展组
                                i["CreatedTime"],   #该扩展组的创建时间，用来排序
                                aSVersion   #该扩展组的版本号
                             )
                                                       )
                    else:
                        self.baseServer[server] = [ #以服务器对信息进行分割,每个扩展组为一个元组，该类型Server可以有多个扩展组数组
                            (
                                i["AutoScalingGroupName"],  #该扩展组的第一个参数：扩展组名称
                                i['DesiredCapacity'], #该扩展组的第二个参数：通过期望的实例数来判断是否为active的扩展组
                                i["CreatedTime"],   #该扩展组的创建时间，用来排序
                                aSVersion   #该扩展组的版本号
                             )
                                                   ]
                else:
                    pass
            except Exception as e:
                print e
                self.logError.info(e)
                pass
     
    def Start(self):
        self.SplitByMin()
        return self.baseServer