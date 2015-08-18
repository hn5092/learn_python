#coding=utf-8
'''
Created on Aug 14, 2015

@author: imad
'''
from CSHelper import CSXPathDocument
import CsQuery
import clr
import sys
import urllib2
from nt import remove
from IronPythonScripts.modules.core.framework import RemoveDom



clr.AddReferenceToFile("CSHelper.dll","HtmlAgilityPack.dll","Newtonsoft.Json.dll")

# req=urllib2.Request("http://www.ali213.net/news/listhtml/list_1_1.html",headers={'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'})
# 
# response=urllib2.urlopen(req,timeout=20) 
# # print response.getcode()
# # print response.read().decode("utf-8")
# # 
# # print response.info()
# #通过创建CQ 来创建一个  网页dom
# dom = CsQuery.CQ.Create(response.read().decode("utf-8"))
# html = dom.Render()
# #获取A标签
# sdom = dom.Select('div.liebyj_lei11 div.liebyj_lei3 a')
# # sdom = sdom.Render()
# #得到A标签的内容
# print sdom.Text()
# Lamda = lambda *csblock:csblock[0].Attr("href")
# result = Lamda(sdom,sdom.Text()) 
# result = sdom.Attr("href")


#---------------------测试内容的--------------------------------------------------------------------------------
req = urllib2.Request("http://www.ali213.net/news/html/2015-6/162867.html",headers={'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'})
response = urllib2.urlopen(req,timeout=20) 
dom = CsQuery.CQ.Create(response.read().decode("utf-8"))
Path=["div.new_ddlei1","div#Content"]
# print dom.Render()
RemoveDom(dom,"script")
# print dom.Render()
sdom = dom.Find("li")
for i in sdom:
    s = CsQuery.CQ.Create(i)
    print s.Text()
