#coding=utf-8
'''
Created on 2015年7月13日

@author: Administrator
'''
import os

#获取文件列表
fileList = os.listdir('d:/fwdata')
#
for filename in fileList:
    for line in open('d:/fwdata/'+filename):
        pass
    else:
        print 'end'        
    