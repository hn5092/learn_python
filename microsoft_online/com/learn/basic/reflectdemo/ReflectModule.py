#coding=utf-8
'''
Created on Aug 10, 2015

@author: imad
'''
import ReflectObject
# print ReflectObject.__name__
# print ReflectObject.__file__
# print ReflectObject.__dict__.items()[0]
module = __import__("ReflectObject")
theobj = getattr(module, "foo")
print theobj('xuym')