#coding=utf-8
'''
Created on 2015年7月6日

@author: Administrator
'''
class People(object):
    def __init__(self, data = 'xym'):
        self.data = data   
        
    def __iter__(self):
        return self
    
    
    def __next__(self):
        print("__next__ called")
        if len(self.data) > 10:
            raise StopIteration
        else:
            self.data += '1111'
            return self.data
for i in People():
    print(i)

