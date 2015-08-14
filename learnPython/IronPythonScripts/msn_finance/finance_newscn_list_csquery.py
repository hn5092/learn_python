import sys
sys.path.append("modules")
from core.framework import *

class NewscnListAnalyst(PythonContentAnalyst):

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
        self.config.cfgContent.Pages=[".hei12"]
        self.config.cfgContent.Path=[".hei14 a"]        
        self.config.cfgContent.Options.Excludes=[]       
        self.config.cfgContent.Options.Lamda=lambda *csblock:csblock[0].Attr("href")
        self.config.cfgContent.Options.PageLamda=lambda *x:x[1]
        self.config.cfgContent.Options.PageNum=2
        self.config.cfgContent.Options.PageSimilarity=0.95
        return self.config   

def getresult(url):
    if url=="http://www.xinhuanet.com/fortune/gd.htm":
        url="http://search.news.cn/mb/xinhuanet/search/?pno=1&namespace=%2Fmb%2Fxinhuanet&nodeid=115033&styleurl=http%3A%2F%2Fwww.xinhuanet.com%2Foverseas%2Fstatic%2Fstyle%2Fcss_erji.css&nodetype=3"
    contentAnalyst=NewscnListAnalyst()
    contentAnalyst.execute(url);
    content=contentAnalyst.result.content
    echo(content)
    echo(len(content.split("|")))
    return contentAnalyst.result.toJsonString()

######################### test case #################################

class  NewscnListTC(unittest.TestCase):
    def __init__(self, methodName = 'runTest'):
        super(NewscnListTC, self).__init__(methodName)
        self.contentAnalyst=NewscnListAnalyst()
       
    def testConfig(self):
        self.contentAnalyst.execute("http://www.xinhuanet.com/fortune/gd.htm")
        content=self.contentAnalyst.result.content
        print content,len(content.split("|"))                   
            
        self.assertEqual(self.contentAnalyst.config.cfgContent.Options.PageNum*50,len(content.split("|")))
        pass

if __name__=="__main__":#sys.exit(0)
    unittest.main()
