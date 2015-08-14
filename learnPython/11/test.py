#coding=utf-8
'''
Created on Aug 14, 2015

@author: imad
'''
#!/usr/bin/env python
#encoding: utf-8

import unittest
#!/usr/bin/env python
#encoding: utf-8

class myclass:
    def __init__(self):
        pass
    
    
    def sum(self, x, y):
        return x+y
    
    
    def sub(self, x, y):
        return x-y 
class mytest(unittest.TestCase):
    
    ##初始化工作
    def setUp(self):
        self.tclass = myclass()   ##实例化了被测试模块中的类
    
    #退出清理工作
    def tearDown(self):
        pass
    
    #具体的测试用例，一定要以test开头
    def test1(self):
        print "come"
        self.assertEqual(self.tclass.sum(1, 2), 3)
    def test2(self):    
        print 'haha '
        
if __name__ =='__main__':
    unittest.main()
