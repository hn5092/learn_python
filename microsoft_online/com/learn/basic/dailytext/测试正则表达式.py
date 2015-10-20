#coding=utf-8
'''
Created on Sep 28, 2015

@author: imad
'''
import re
a = "edasdasdwsww.baidu.com.cn.1213123!@31$!231@#!@#!!@#12#!@#!@#"
b = re.compile("www.baidu.com");
if b.findall(a) :
    print " i have"