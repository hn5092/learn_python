#coding=utf-8
'''
Created on Sep 17, 2015

@author: imad
'''
def role():
    def fu(method):
        def arg(args):
            pass
        return arg
    return fu
@role("root")
def task1():
    print "run task1"
@role("normal")
def task2():
    print "run task2"

