#coding=utf-8
import CalTime
import OptInstance
import time
import thread


def Clock():
    getTime = CalTime.CalTime()
    for key,value in getTime['start'].items():
        thread.start_new_thread(Start,(key,value))
    for key,value in getTime['stop'].items():
        thread.start_new_thread(Stop,(key,value))
    
def Start(sleepS,instanceIds):
    time.sleep(sleepS)
    while 1:
        OptInstance.StartInstance(instanceIds)
        time.sleep(86400)
    
def Stop(sleepS,instanceIds):
    time.sleep(sleepS)
    while 1:
        OptInstance.StopInstance(instanceIds)
        time.sleep(86400)

