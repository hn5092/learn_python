#coding=utf-8
'''
Created on 2015年7月21日

@author: Administrator
'''
class human():
    color = 'yellow'
    def __init__(self,eye,mouhth):
        self.eye = eye
        self.mouhth = mouhth
    def sayhi(self):
        print 'hello'

        
class doc(human):
    def __init__(self,age,eye,mouhth):
        human.__init__(self, eye, mouhth)
        self.age = age

    def d(self):
        print 'im a doc'
    def sayhi(self):    
        print 'hi'
        
# xiaoming = human()
# print xiaoming.eye
# print xiaoming.mouhth
# xiaodong = human('blue','small')
# # print xiaodong.eye
# # print  xiaodong.mouhth
# xiaodong.color
# xiaodong.sayhi()
xm = doc(11,'red','big')
xm.sayhi()
xm.d()
