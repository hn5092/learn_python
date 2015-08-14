#coding=utf-8
import sys
import unittest

from IronPythonScripts.modules.core.framework import PythonContentAnalyst, echo


sys.path.append("modules")

class cg_ali213_news_list(PythonContentAnalyst):
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
        self.config.cfgContent.Path=["div.liebyj_lei11 div.liebyj_lei3 a"]        
        self.config.cfgContent.Options.Excludes=[]       
        self.config.cfgContent.Options.Lamda=lambda *csblock:csblock[0].Attr("href")
        self.config.cfgContent.Options.PageLamda=lambda *x:x[1]
        self.config.cfgContent.Options.PageNum=2
        self.config.cfgContent.Options.PageSimilarity=0.95
        return self.config
    
    def lamda(self,csblock):
        cshyperblock=csblock[0]
        text=cshyperblock.Text()
        lm=cshyperblock.Find(".dd_lm").Text()
        title=cshyperblock.Find(".dd_bt > a").Text()
        href=cshyperblock.Find(".dd_bt > a").Attr("href")
        if len(text)>0 and lm.find("视频")==-1 and lm.find("I  T")==-1:
            echo(title)
            return href
        else:
            return ""

def getresult(url):
    contentAnalyst=cg_ali213_news_list()
    contentAnalyst.execute(url);
    content=contentAnalyst.result.content
    echo(content)
    echo(len(content.split("|")))
    return contentAnalyst.result

class TC0(unittest.TestCase):
    def __init__(self, methodName = 'runTest'):
        super(TC0, self).__init__(methodName)
        self.contentAnalyst=cg_ali213_news_list()
       
    def testConfig(self):
        self.contentAnalyst.execute("http://www.ali213.net/news/listhtml/list_1_1.html")
        content=self.contentAnalyst.result.content
        print content,len(content.split("|"))
        self.assertGreater(len(content.split("|")),30)
        pass
    
    

if __name__=="__main__":#sys.exit(0)         
    unittest.main()


