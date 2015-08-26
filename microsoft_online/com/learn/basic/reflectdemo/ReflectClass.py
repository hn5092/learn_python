#coding=utf-8
'''
Created on Aug 10, 2015

@author: imad
'''
from com.learn.basic.reflectdemo.ReflectObject import Cat
print Cat.__doc__
print Cat.__class__
cat = Cat("blue")
cat.sayHi()
print cat.__class__.__name__
print cat.__class__.__module__
print Cat.__dict__

cat2 = globals()['Cat']("blue")
cat2.sayHi()
# cat3 = globals()['foo']("blue")
# cat3()
