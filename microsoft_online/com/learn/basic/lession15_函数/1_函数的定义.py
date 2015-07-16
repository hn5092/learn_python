#coding=utf-8
'''
Created on 2015年7月7日

@author: Administrator
'''
#def语句是实时执行的

#1.函数是一个对象
#定义一个对象
# def test(money,b):
#     
#     return money+b
# 
# result = test(150,10)
# print(result)




#2.函数完全可以嵌套在一个if语句中定义
# test = 1
# if test :
#     def func():
#         return 11
# else:
#     def func():
#         return 12               
# print(func())
#  
# other = func
# print(other())

#调用函数
def find(s1, s2):
    res = [] #m,
    for c in s1:
        if c in s2:
            res.append(c)
    return res
l = find('myname', 'name')
print(l)
# x=10


def find2(s1,s2):
    l =  [x for x in s1 if x in s2]
    return l
print(find2('myname', 'name'))


