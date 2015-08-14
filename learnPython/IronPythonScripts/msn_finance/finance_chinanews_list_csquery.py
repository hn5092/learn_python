import unittest
import sys
sys.path.append("modules")
from core.framework import *

class ChinanewsListAnalyst(PythonContentAnalyst):

    def setConfig(self,url):
        self.config.cfgUrl=url
        self.config.cfgCharset=self.enum.Charset.gb2312
        self.config.cfgSelector=self.enum.Selector.csquery
        self.config.cfgTitle=[]
        self.config.cfgAuthor=[]
        self.config.cfgSummary=[]
        self.config.cfgSource=[]
        self.config.cfgIssuedate=[]
        self.config.cfgContent.Type=self.enum.ContentType.index
        self.config.cfgContent.Pages=["div.pagebox"]
        self.config.cfgContent.Path=[".content_list li"]        
        self.config.cfgContent.Options.Excludes=[]       
        self.config.cfgContent.Options.Lamda=lambda *csblock:self.lamda(csblock)
        self.config.cfgContent.Options.PageLamda=lambda *x:x[1]
        self.config.cfgContent.Options.PageNum=3
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
    contentAnalyst=ChinanewsListAnalyst()
    contentAnalyst.execute(url);
    content=contentAnalyst.result.content
    echo(content)
    echo(len(content.split("|")))
    return contentAnalyst.result

class TC0(unittest.TestCase):
    def __init__(self, methodName = 'runTest'):
        super(TC0, self).__init__(methodName)
        self.contentAnalyst=ChinanewsListAnalyst()
       
    def testConfig(self):
        self.contentAnalyst.execute("http://www.chinanews.com/scroll-news/news1.html")
        content=self.contentAnalyst.result.content
        print content,len(content.split("|"))
        self.assertGreater(len(content.split("|")),300)
        pass



if __name__=="__main__":#sys.exit(0)         
    unittest.main()
