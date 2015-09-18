#coding=utf-8
'''
Created on Sep 17, 2015

@author: imad
'''

    
def b(func):
    def de():
        print "验证 "
        func()
    return de
@b
def a():
    print "网站操作 "
# a()
 #------------------
def b2(func):
    def de():
        print "验证 "
        def a2():
            print "网站操作 "
    return de
def a2():
    print "网站操作 "
a2()
