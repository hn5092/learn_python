'''
Created on 2015年7月6日

@author: Administrator
'''
f  = open('d:\data.txt')
m = open('d:\data.txt')

print(f.__next__())
print(f.__next__())

print(next(m))
print(next(m))
next(m)             #迭代停止