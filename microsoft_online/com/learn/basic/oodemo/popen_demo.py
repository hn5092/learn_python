#coding=utf-8
'''
Created on 2015年7月25日

@author: Administrator
'''
import os
cmd = os.popen('ipconfig').read()
cmd = cmd.decode('gbk')
l = cmd.split(u'适配器')
print l[1]


