#coding=utf-8
'''
Created on Aug 10, 2015

@author: imad
'''
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
    print cat.__class__;
    print dir(cat)
    print hasattr(cat, "name")
    print cat.name
    print setattr(cat, "name", "grep")
    print getattr(cat, "name")
    if hasattr(cat, "name"):
        print "cat hava name attr"
        setattr(cat, "name", "grep")
    print getattr(cat, "name")
    getattr(cat, "sayHi")()


