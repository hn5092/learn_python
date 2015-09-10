#coding=utf-8
'''
Created on Sep 1, 2015

@author: imad
'''
def eat(func):
    print '学吃饭'
    def learneat(arg):
        print "learning eat"
        func(arg) 
    return learneat

def sleep(func):
    print "学睡觉"
    def learnsleep(arg):
        print "learning sleep"
        func(arg) 
    return learnsleep
@sleep
@eat
def people(name='xym'):
    print "%s 成功学会技能" % (name)

people("xiaoming")