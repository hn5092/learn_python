#coding=utf-8
'''
Created on 2015年7月21日

@author: Administrator
'''
def fun():
    yield 1
    yield 2
    yield 3
a = fun()
print a.next()
print a.next()
print a.next()
print a.next()