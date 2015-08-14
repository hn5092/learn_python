import sys
import unittest
import urllib2

from IronPythonScripts.modules.core.framework import PythonContentAnalyst, echo
from core.framework import *


sys.path.append("modules")

class cg_ali213_xinyou_list(PythonContentAnalyst):
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
        self.config.cfgContent.Pages=[]
        self.config.cfgContent.Path=["div.win_body_type_left_top_con:eq(0) div.win_body_type_left_top_con_info a","div.andriod_gametj_left_con:eq(0) div.andriod_gametj_left_con_pic a","div.iphone_gametj_right_con:eq(0) div.iphone_gametj_right_con_pic a"]        
        self.config.cfgContent.Options.Excludes=[]       
        self.config.cfgContent.Options.Lamda=lambda *csblock:self.lamda(csblock)
        self.config.cfgContent.Options.PageLamda=lambda *x:x[1]
        self.config.cfgContent.Options.PageNum=0
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
    contentAnalyst=cg_ali213_xinyou_list()
    contentAnalyst.execute(url);
    content=contentAnalyst.result.content
    echo(content)
    echo(len(content.split("|")))
    return contentAnalyst.result

#getresult(URL)

class TC0(unittest.TestCase):
    def __init__(self, methodName = 'runTest'):
        super(TC0, self).__init__(methodName)
        self.contentAnalyst=cg_ali213_xinyou_list()
       
    def testConfig(self):
        self.contentAnalyst.execute("http://m.ali213.net/ios/?x")
        content=self.contentAnalyst.result.content
        print content,len(content.split("|"))
        self.assertGreater(len(content.split("|")),11)
        pass

        self.contentAnalyst.execute("http://m.ali213.net/wp/?x")
        content=self.contentAnalyst.result.content
        print content,len(content.split("|"))
        self.assertGreater(len(content.split("|")),14)
        pass

        self.contentAnalyst.execute("http://m.ali213.net/android/?x")
        content=self.contentAnalyst.result.content
        print content,len(content.split("|"))
        self.assertGreater(len(content.split("|")),27)
        pass


if __name__=="__main__":#sys.exit(0)         
    unittest.main()


