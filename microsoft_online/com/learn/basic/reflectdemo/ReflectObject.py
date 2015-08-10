#coding=utf-8
'''
Created on Aug 10, 2015

@author: imad
'''
import sys
import inspect
from ecdsa.ecdsa import __main__
def foo(name):
    print name+"呵呵"

class Cat(object):
    def __init__(self, name):
        self.name = name
        
    def sayHi(self):
        print "hello!"



if __name__ == "__main__":
    cat  = Cat("bule")
    cat.sayHi()
    print dir(cat)
    if hasattr(cat, "name"):
        print "cat hava name attr"
        setattr(cat, "name", "grep")
    print getattr(cat, "name")
    getattr(cat, "sayHi")()


