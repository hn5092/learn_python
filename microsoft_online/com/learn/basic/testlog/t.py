#coding=utf-8
'''
Created on Sep 14, 2015

@author: imad
'''
f = open("G:\img\ex150912.log")
a = [1, 2]
for x in f.readlines():
#     print x
    b = x.split(" ")
#     print b.__len__()
    if b.__len__() == 12 :
        if b[10].startswith("2"):
            print x
def a(a,b,c):
    print a,b,c
def a(b,c):
    print b,c