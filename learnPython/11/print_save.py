#coding=utf-8
'''
Created on 2015年6月22日

@author: Administrator
'''
import sys
temp = sys.stdout
sys.stdout = open('c:\log','a')
print('spam')
print(1,2,3)
sys.stdout.close()
sys.stdout = temp
print ('iamback')