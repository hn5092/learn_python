#coding=utf-8
'''
Created on Sep 1, 2015

@author: imad
'''
import functools
#多参数情况下是先执行内部的再执行外部的
#每次修饰之后返回的是一个函数  再次修饰他的时候他整个整体是下一个函数的func 
def eat(param):
    print '学吃饭' + param
    def learneat(func):
        @functools.wraps(func)
        def who1(args):
            func(args)
            print "learning eat"
        return who1 
    return learneat

def sleep(param):
    print "学睡觉" + param
    def learnsleep(func):
        @functools.wraps(func)
        def who2(args):
            print "learning sleep"
            func(args) 
        return who2
    return learnsleep
@eat("1t")
@sleep("10h")
def people(name='xym'):
    print "%s 成功学会技能" % (name)

# people("xiaoming")
# 
# eval("people")(1)
vars()['people'](2)



@eat
class a():
    def b(self):
        print "b"
    def c(self):
        print "c"