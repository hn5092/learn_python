#coding=utf-8
'''
Created on Sep 1, 2015

@author: imad
'''
def decorate(role):#修饰的是传入的参数
    def chose(method):#使用注解的第一个参数便是被修饰的原函数
        def fun():
            if role == "root":
                print "root user login"
                method()
            else:
                print "normal user login"
                method()
        return fun
    return chose
    

@decorate("root")
def prototype():
    print "i am prototype"

prototype()