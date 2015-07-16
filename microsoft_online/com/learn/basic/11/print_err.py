#coding=utf-8
'''
Created on 2015年6月22日

@author: Administrator
'''
import sys
sys.stderr.write("str")
print >>sys.stderr,'Bad!' * 8
l = [1,2,3]
l.