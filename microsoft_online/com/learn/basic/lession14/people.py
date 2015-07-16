#coding=utf-8
'''
Created on 2015年7月6日

@author: Administrator
'''


class Hi(object):
    def __init__(self, name = ''):
        self.name = name
    def sayhi(self):
        print('hello%s'%(self.name))
    def __iter__(self):
        return self
    
    def __next__(self):
        print("__next__ called")
        if len(self.name) > 5:
            raise StopIteration
        else:
            self.name += str(len(self.name))
            return self.name
   

h =Hi('xym')
h.sayhi()
for i in h:
    print(i)