#coding=utf-8
'''
Created on 2015年7月16日

@author: Administrator
'''
# 类的初始化
# __init__初始化(私有函数)
# from os.path import join
# class FileObject:
#     '''给文件对象进行包装从而确认在删除时文件流关闭'''
# 
# def __init__(self,filepath='~',filename='sample.txt'):
#     #读写模式打开一个文件
#     self.file=open(join(filepath,filename),'r+')
# 
# def __del__(self):#解构器
#     self.file.close()
#     del self.file
# 
# 
# 
# __init__初始化
# 对实体进行初始化
# class Dog:
#     def __init__(self,name):
#         self.DogName = name #必须赋值self，否则类中其他函数无法调用
#     def bark(self):
#         print "Wang!"
# D = Dog('Sam')
# D.bark()
# 
# 
# 
# 
# 类的绑定
# class Person:
#     def __init__(self,Type,Sex,Age,Name):
#         self.race = Type
#         self.sex = Sex
#         self.age = Age
#         self.name = Name
#     def talk(self,msg=0):
#         self.msg = msg
#         if self.msg != 0:
#             print self.name,'Saying:',self.msg
# P = Person('Black','Female','24','Susan')
# P.talk('Hello,my name is %s'%P,name)
# 
# 
# 类的继承
# 为什么要使用类的继承？
# class Person:#父类
#     def __init__(self,Type,Sex,Age,Name):
#         self.race = Type
#         self.sex = Sex
#         self.age = Age
#         self.name = Name
#     def talk(self,msg=0):
#         self.msg = msg
#         if self.msg != 0:
#             print self.name,'Saying:',self.msg
# 
# class person_info(Person):#子类
#     def __init__(self,Type,Sex,Age,Name,nation,work,salary):
#         Person.__init__(self,Type,Sex,Age,Name)
#         self.country = nation
#         self.job = work
#         self.salary = salary
#     def tell(self,msg):
#         print '''%s's personal information:
#             Name : %s
#             Age : %s
#             Nation : %s
#             Work : %s
#             '''(self.name,self.name,self.age,self.country,self.job)




