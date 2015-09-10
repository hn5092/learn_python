#coding=utf-8
'''
Created on Aug 10, 2015

@author: imad
'''
module = __import__("multipleArgs")
print module.__str__()
theobj = getattr(module, "people")
print theobj.__name__
