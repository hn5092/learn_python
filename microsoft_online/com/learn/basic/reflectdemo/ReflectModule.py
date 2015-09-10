#coding=utf-8
'''
Created on Aug 10, 2015

@author: imad
'''
import ReflectObject
# print ReflectObject.__name__
# print ReflectObject.__file__
# print ReflectObject.__dict__.items()[0]
path = "com.learn.basic.decoratordemo.multipleArgs"
module = __import__(path)
dirlist = path.split(".")
for x in dirlist :
    if x != dirlist[0]:
        module = getattr(module, x)
print dir(module)
eval("people")