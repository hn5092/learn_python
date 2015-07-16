#coding=utf-8
'''
Created on 2015年6月22日

@author: Administrator
'''
import sys
x = 1;y = 2
print x, y
sys.stdout.write(str(x)+' '+str(y)+'\n')
print >>open('c:\log','w'), x, y
open('c:\log2','w').write(str(x)+' '+str(y)+'\n')
print open('c:\log','r').read()
print open('c:\log2','r').read()
