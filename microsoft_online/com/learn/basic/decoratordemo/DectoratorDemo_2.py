#coding=utf-8
'''
Created on Aug 10, 2015

@author: imad
'''
# 
# 
# def f1(a):
#     print "f1 %s" %(a)
#     return a
# @f1
# def f2(x = ""):
#     print "f2"
#     return 1
# print "start"
# f2("1")
#print f2("1") 出错
#print f1(None)
    
    
def a():
    print "iam a "



def b(func):
    def decorate():
        print "在A方法执行之前添加一些功能"
        func() #执行A方法
        print "这里可以在A方法执行之后添加一些功能"
    return decorate
    
@b    
def c():
    a()
c()