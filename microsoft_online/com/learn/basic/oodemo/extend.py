#coding=utf-8
'''
Created on 2015年7月20日

@author: Administrator
'''
class Person:
    cas = 'ssss'
    def __init__(self,name,age):
        self.name = name
        self.age = age
    def sayhi(self):
        print 'iam %s ,im %s' %(self.name,self.age)
class Child(Person):
    def __init__(self, name, age,info):
        Person.__init__(self, name, age)
        self.info = info
    def sayhi(self):
        
        print 'iam %s ,im %s,info:%s' %(self.name,self.age,self.info)


xiaoming = Child('xiaom','22','chengxuyuan')
xiaoming.sayhi()
print xiaoming.cas