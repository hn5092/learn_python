#coding=utf-8
'''
Created on 2015年7月10日

@author: Administrator
'''
import re
f = open('E:/fwdata/1.po','rb')
r = open('E:/fwdata/clear2','w')
t = f.readline()
t = t.decode('utf-8')
t = t.split(',')
for v,k in enumerate(t) :
    print(v,k)
for line in f:
    line = line.decode('utf-8')
    patten = re.compile('\"(.*?)\"')
    l1 = patten.findall(line)
    if l1[14] != '':
        l1=l1[0:-1]
        r.write(str(l1)+'\n')
    print(l1)
    print(len(l1))
