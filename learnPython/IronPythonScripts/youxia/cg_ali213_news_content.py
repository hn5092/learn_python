﻿#coding=utf-8
import sys
import unittest

from IronPythonScripts.build_result import echo, FunctionHelper
from IronPythonScripts.modules.core.framework import PythonContentAnalyst


sys.path.append("modules")

class ali213NewsContentAnalyst(PythonContentAnalyst):

    def setConfig(self,url):
        self.config.cfgUrl=url
        self.config.cfgCharset=self.enum.Charset.utf8
        self.config.cfgSelector=self.enum.Selector.csquery
        self.config.cfgTitle=["h1"] 
        self.config.cfgAuthor=[("div.new_sl",lambda x:getAuthor(x))] #("p.pleft > span:eq(1)",lambda x:x[3:])
        self.config.cfgSource=[("div.new_sl",lambda x:getSource(x))]
        self.config.cfgIssuedate=[("div.new_sl",lambda x:getDate(x))]
        self.config.cfgSummary=["div.new_ddlei h2"]        
        self.config.cfgContent.Type=self.enum.ContentType.text
        self.config.cfgContent.Options.Excludes=["div.page_fenye","embed"]    
        self.config.cfgContent.Path=["div.new_ddlei1","div#Content"]
        #self.config.cfgContent.Options.Lamda=lambda *x:x[1] #没用到 
        self.config.cfgContent.Pages=["div.page_fenye"] 
        self.config.cfgContent.Options.PageNum=0 #0=无限制 
        self.config.cfgContent.Options.PageLamda=lambda *x:x[1]
        self.config.cfgContent.Options.PageSimilarity=0.95 #相似度
        return self.config
    
   
    def csqueryPagination(self,csdom,pagesPaths):
        '''默认实现相似度计算，可识别路径/、？'''
        return super(ali213NewsContentAnalyst,self).csqueryPagination(csdom,pagesPaths)

    def csqueryConents(self,csdompagination):
        return super(ali213NewsContentAnalyst,self).csqueryConents(csdompagination)

    def lastCsdomp(self,lastcsdompage):
        '''最后一个段落<p>'''
        return super(ali213NewsContentAnalyst,self).lastCsdomp(lastcsdompage)

    def pageContentText(self,content):
        """分页的内容清理，默认清空注释、style、onmouseover，粗体替换，unicode编码转汉字"""
        return super(ali213NewsContentAnalyst,self).pageContentText(content)

    def pageCsContentImage(self,cspage):
        """<img/>路径识别，默认支持/路径转换"""        
        return  super(ali213NewsContentAnalyst,self).pageCsContentImage(cspage)

def getresult(url=''):   
    contentAnalyst=ali213NewsContentAnalyst()
    contentAnalyst.execute(url);
    content=contentAnalyst.result.content
    title=contentAnalyst.result.article_properties["title"]
    source=contentAnalyst.result.article_properties["source"]
    contentAnalyst.result.article_properties["title"]=title+" [@@资讯:"+source+"]"
    echo(content)
    return contentAnalyst.result.toJsonString()

def getAuthor(str): 
    import re 
    p=re.compile('\s+') 
    str=re.sub(p,',',str) 
    arr=str.split(",")     
    if(str.find("编辑")>-1):        
        start=arr[3].find("编辑")
        str=arr[3][start+3:]
        return str
    else: 
        return ""
    

def getSource(str):
    import re 
    p=re.compile('\s+') 
    str=re.sub(p,',',str) 
    arr=str.split(",")     
    if(str.find("来源")>-1):        
        start=arr[2].find("来源")
        str=arr[2][start+3:]
        return str
    else: 
        return "游侠网"

def getDate(str):
    try:
        trimstr=str.strip()
        trimstr=trimstr[0:19]
        return trimstr;
    except Exception as err:    
        return ""

#getresult(URL)

####################### test case ######################
    
class auto163ContentAnalystTC(unittest.TestCase):
    def __init__(self, methodName = 'runTest'):
        super(auto163ContentAnalystTC, self).__init__(methodName)
        self.contentAnalyst=ali213NewsContentAnalyst()
       
    def testConfig(self): 
        result=getresult("http://www.ali213.net/news/html/2015-6/162867.html")
        print "-----------------------------------------------------------------------------"
        print result
       


        result=getresult("http://www.ali213.net/news/html/2015-6/160667.html")
        result=FunctionHelper.string2object(result)
        self.assertGreater(result.article_properties["title"].find("支线任务不再浪费时间"),-1)       
        self.assertGreater(result.article_properties["summary"].find("根据Xbox官方杂志最新报道"),-1)
        self.assertGreater(result.article_properties["source"].find("互联网"),-1)         
        self.assertEqual(result.article_properties["issuedate"],"2015-06-08 17:41:06")
        self.assertGreater(result.content.find("一触即燃"),-1)
        #self.assertGreater(result.article_properties["author"].find("费希"),-1) 
        pass

        result=getresult("http://www.ali213.net/news/html/2015-6/160503.html")
        result=FunctionHelper.string2object(result)
        print self.assertGreater(result.article_properties["title"].find("河南大学生拍"),-1)       
        print self.assertGreater(result.article_properties["summary"].find("的一群毕业生玩起"),-1)
        #self.assertGreater(result.article_properties["source"].find("互联网"),-1)         
        print self.assertEqual(result.article_properties["issuedate"],"2015-06-07 17:22:49")
        print self.assertGreater(result.content.find("http://img2.ali213.net/picfile/News/2015/06/07/584_2015060752059634.jpg"),-1)       
        pass
        

if __name__=="__main__":#sys.exit(0) 
    unittest.main()
    sys.exit(0)