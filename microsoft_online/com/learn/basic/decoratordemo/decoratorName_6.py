#coding=utf-8
'''
Created on Aug 26, 2015

@author: imad
'''
import time
import functools
 
def timeit(func):
    @functools.wraps(func)
    def wrapper():
        start = time.clock()
        func()
        end =time.clock()
        print 'used:', end - start
    return wrapper
 
@timeit
def foo():
    print 'in foo()'
 
foo()
print foo.__name__