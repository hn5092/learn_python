#coding=utf-8
'''
Created on 2015年7月13日

@author: Administrator
'''
#------------------------------1---------------------------------------
#!/usr/local/bin/python
#coding=utf-8
 
# ip = '192.168.80.103'
# name = 'root'
# cmd = 'df'
# import os
# def runCmd(name,host,cmd):
#         print cmd
#         CMD = "ssh %s@%s %s" %(name, host,cmd)
#         os.system(CMD)
#         print '\033[7;33m执行完毕退出\033[0m'
# runCmd(name, ip, cmd)
#------------------------------2---------------------------------------
#更改
# runCmd(name, ip, raw_input('\033[7;32m请输入命令\033[0m'))
#------------------------------3---------------------------------------
#return 
#------------------------------4---------------------------------------
#默认参数 runCmd(name,host,cmd=''):
#------------------------------5---------------------------------------
#默认参数指向不可变的
# def add(L=[]):
#     L.append('end')
#     return L
# print(add([1, 2]))
# print(add([2, 2, 3 ]))
# print(add())
# print(add())


#修改 L=none
# def add(L=None):
#     if L == None:
#         L = []
#     L.append('end')
#     return L
# print(add([1, 2]))
# print(add([2, 2, 3 ]))
# print(add())
# print(add())
#------------------------------6---------------------------------------
# 可变参数
# def calc(*s):
#     print(type(s))
#     return sum(s)
# print calc(1, 2, 3)
# print calc(1, 2, 3,4,5,6)
# l = [2, 4, 5, 5, 6]
# print calc(*l)
#------------------------------7---------------------------------------
#关键字参数
# def info(**kw):
#     print type(kw)
#     print kw 
#     if 'name' in kw:
#         print 'hello,my name is %s,i,am %s,i,m from %s'%(kw['name'],kw['age'],kw['loc'])
#     else:
#         print 'hello,my name isi,am %s,i,m from %s'%(kw['age'],kw['loc'])
# info(age='21',loc = 'yunnan')
def info(**kw):
    print type(kw)
    print kw 
    try:
        print 'hello,my name is %s,am %s,i,m from %s'%(kw['name'],kw['age'],kw['loc'])
    except:
        print 'argument is worry'
info(age='21',loc = 'yunnan')