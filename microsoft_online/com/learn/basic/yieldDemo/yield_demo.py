#coding=utf-8
'''
Created on 2015年7月21日

@author: Administrator
'''
def fab(max):
    a,b=0,1
    while a < max:
        print 'before a %d'%(a)
        yield a
        print 'begin a %d'%(a)
        a,b = b, a+b
        print 'end a %d'%(a)
a = fab(10)
print a.next()
print a.next()
print a.next()
print a.next()
# for i in fab(20):
#     print i