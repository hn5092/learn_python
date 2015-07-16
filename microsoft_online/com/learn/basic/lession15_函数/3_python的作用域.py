#coding=utf-8
'''
Created on 2015年7月8日

@author: Administrator
'''
# 1.每个模块都是一个全局作用域
#  from pip._vendor.distlib.compat import raw_input
# x = 10
# def test():
#     global x
#     x=5
#     print('函数内的'+str(x))
# test()
# print(x)
#2全局作用域的作用范围仅限于单个文件
# from _ast import Nonlocal

#3.赋值的变量名除非声明为全局变量 不然都是本地变量

#4.每次函数调用都是创建一个本地的作用域

#LEGB原则
#1.变量名的范围是先搜索本地(L) 然后是函数内(E),之后全局(G),最后是内置(B)
#2.默认情况下变量名的赋值要么创建一个变量 要么改变一个变量

#在有些情况下会覆盖原著阿公
# def open():
#     print('open')
# open()
# import builtins




#global
# x=10
# def test1():
#     x=5
#     print(x)
#     global y
#     y=11
# test1()
# print(x)
# print(y)




#嵌套作用域

# def f1():
#     x = 88
#     def f2():
#         print(x)
#     f2()
# f1()

# 嵌套作用域
# def f3():
#     val = 88
#     def f4():
#         print(val)
#     return f4
# name = f3()
# name()

#工厂函数
# def f(n):
#     def acla(x):
#         print(x ** n)
#     return acla
# function = f(2)
# print(function)
# function(2)

# def func():
#     list1 = []
#     for i in range(5):
#         list1.append(lambda x,i=i: i ** x)
#     return list1
# act = func()
# print (act[4](2))

#Nonlocal 可以改变

# def f1(x):
#     state = x
#     def f2(a):
#         nonlocal state
# #         state = 1
#         print(state)
#         state += 1
#     return f2
# test = f1(2)
# test(4)
# test(5)

#python 2.7中可以达到这个效果
def f1(x):
    global state
    state = x
    def f2(a):
        global state
#         state = 1
        print(state)
        state += 1
    return f2
test = f1(2)
test(4)
test(5)

