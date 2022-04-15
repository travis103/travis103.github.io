#coding=utf-8
from django.http import HttpResponse
import json
import telnetConn
  
def Start(req):
    totalCounts = telnetConn.COUNT['total']
    match = telnetConn.COUNT['matched']
    notmatch = telnetConn.COUNT['notmatched']
    data = {}
    data['process'] = round(float(match+notmatch)/float(totalCounts),2)*100
    data['process'] = int(data['process'])
    data['match'] = match
    data['notMatch'] = notmatch
    data['total'] = totalCounts
    return HttpResponse(json.dumps(data, ensure_ascii=False))