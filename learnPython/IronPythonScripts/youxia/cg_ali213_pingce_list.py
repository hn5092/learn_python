import sys
import unittest
import urllib2

from IronPythonScripts.build_result import echo, FunctionHelper
from IronPythonScripts.modules.core.framework import PythonContentAnalyst
from core.framework import *


sys.path.append("modules")

#list=cg_ali213_news_list
#Ali213NewsList=list.cg_ali213_news_list
#l=Ali213NewsList()
#l.execute("")

class cg_ali213_pingce_list(PythonContentAnalyst):
    """description of class"""
    def setConfig(self,url):
        self.config.cfgUrl=url
        self.config.cfgCharset=self.enum.Charset.utf8
        self.config.cfgSelector=self.enum.Selector.csquery
        self.config.cfgTitle=[]
        self.config.cfgAuthor=[]
        self.config.cfgSummary=[]
        self.config.cfgSource=[]
        self.config.cfgIssuedate=[]
        self.config.cfgContent.Type=self.enum.ContentType.index
        self.config.cfgContent.Pages=["div.liebyj_libiao3"]
        self.config.cfgContent.Path=["item url","h2 a"]        
        self.config.cfgContent.Options.Excludes=[]
        
        self.config.cfgContent.Options.Lamda=lambda *csblock:self.lamda(csblock)
        self.config.cfgContent.Options.PageLamda=lambda *x:x[1]
        self.config.cfgContent.Options.PageNum=2
        self.config.cfgContent.Options.PageSimilarity=0.95
        return self.config 
    
    def lamda(self,csblock):
        href=csblock[0].Attr("href") 
        if not href:
            href=csblock[1]
        if href:
            href=href.replace("\\","").replace("\"","")   
        if href and href[0:1]=="/":
            proto, rest = urllib2.splittype(self.config.cfgUrl)  
            host, rest = urllib2.splithost(rest)
            href=proto+"://"+host+href        
        return href 


def getresult(url):
    result=[]    
    contentAnalyst=cg_ali213_pingce_list()
    contentAnalyst.execute(url);
    content=contentAnalyst.result.content
    echo(content)
    echo(len(content.split("|")))
    return contentAnalyst.result

#getresult(URL)

class TC0(unittest.TestCase):
    def __init__(self, methodName = 'runTest'):
        super(TC0, self).__init__(methodName)
        self.contentAnalyst=cg_ali213_pingce_list()
       
    def testConfig(self):#2，3，4，5
        self.contentAnalyst.execute("http://api.ali213.net/shouyou/news.php?c=16")
        content=self.contentAnalyst.result.content
        print content,len(content.split("|"))
        self.assertGreater(len(content.split("|")),2)
        pass

        self.contentAnalyst.execute("http://m.ali213.net/api/preload.php?id=5&typeid=0&pt=pc")
        content=self.contentAnalyst.result.content
        print content,len(content.split("|"))
        self.assertGreater(len(content.split("|")),5)
        pass

        self.contentAnalyst.execute("http://m.ali213.net/pingce/")
        content=self.contentAnalyst.result.content
        print content,len(content.split("|"))
        self.assertGreater(len(content.split("|")),5)
        pass    


if __name__=="__main__":#sys.exit(0)         
    unittest.main()




