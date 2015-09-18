#coding=utf-8
'''
Created on Sep 1, 2015

@author: imad
'''
def eat(func):
#     print '学吃饭'
    def learneat(arg):
        print "learning eat"
        func(arg) 
        print "eat end"
    return learneat
    
def sleep(func):
#     print "学睡觉"
    def learnsleep(arg):
        print "learning sleep"
        func(arg) 
        print "学会睡觉"
    return learnsleep
@eat
@sleep
def people(name='xym'):
    print "%s 成功学会技能" % (name)
@eat
@sleep
def dog(name='xym'):
    print "%s 成功学会技能" % (name)   

def all():
    print "learning eat"
    print "learning sleep"
    print "%s 成功学会技能" % ('xym')
    print "学会睡觉" 
    print "eat end"
people("xym")