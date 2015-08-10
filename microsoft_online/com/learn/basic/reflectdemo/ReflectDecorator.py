#coding=utf-8
'''
Created on Aug 10, 2015

@author: imad
'''


connlist  = {"xym":11,"xym2":12}
def conn(func):
    def serve(*args):   
        print "begin"
        func(*args)
        print "end"
        return 1
    return serve
@conn
def reflcet(name):
    module = __import__("reflect")
    #处理请求
    func = getattr(module, name)
    return func()
# class Cat():
#     def __init__(self, name, age, info):
#         self.name = name 
#         self.age = age
#         self.info = info 
#     def conn(self,func):
#         print "begin"
#         func()
#         print "end"
#     @conn
#     def reflcet(self,name):
#         module = __import__("reflect")
#         #处理请求
#         func = getattr(module, name)
#         return func
# cat = Cat("go",11,"tobegin")    
# module = __import__("reflect")
#     #处理请求
# func = getattr(module, "xym")   
# func()
print reflcet("xym") 