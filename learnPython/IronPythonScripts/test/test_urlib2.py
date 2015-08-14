#coding=utf-8
'''
Created on Aug 14, 2015

@author: imad
'''
import sys
import urllib2


req=urllib2.Request("http://www.ali213.net/news/listhtml/list_1_1.html",headers={'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'})
response=urllib2.urlopen(req,timeout=20) 
print response.getcode()
# print response.read().decode("utf-8")
print response.info()