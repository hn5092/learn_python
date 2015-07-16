#coding=utf-8
'''
Created on 2015年7月13日

@author: Administrator
'''
from datetime import timedelta
import datetime
import time
import urllib
import code
while True :
    endDate =  time.strftime("%Y-%m-%d %H:%M")
    startDate = datetime.datetime.now()  +timedelta(minutes=-15)
    webCode = ['138383', '138384', '2010072']
    for code in webCode:
        url = 'http://dfeed.networkbench.com/rpc-export/exportTxt.po?authkey=SDZS0tGY02&taskId=%s&by=error&startDate=%s&endDate=%s&taskType=1'%(code,startDate,endDate)
        print(url)
        f = urllib.urlopen(url).read()
        filename = 'D:/fwdata/%s'%(time.strftime("%Y-%m-%d-%H-%M-")+code)
        d = open(filename,'w')
        d.write(f)
    else:
        time.sleep(900)
        