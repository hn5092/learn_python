import sys
import unittest
import urllib2

from IronPythonScripts.build_result import PythonContentAnalyst, echo
from core.framework import *


sys.path.append("modules")

class cg_ali213_strategy_list(PythonContentAnalyst):
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
        self.config.cfgContent.Path=["list > item"]        
        self.config.cfgContent.Options.Excludes=[]       
        self.config.cfgContent.Options.Lamda=lambda *csblock:self.lamda(csblock)
        self.config.cfgContent.Options.PageLamda=lambda *x:x[1]
        self.config.cfgContent.Options.PageNum=0
        self.config.cfgContent.Options.PageSimilarity=0.95
        return self.config

    def lamda(self,csblock):
        href=csblock[0].Select("url").Text()
        type=csblock[0].Select("tag").Text()
        try:            
            name=csblock[0].Find("name").Text().encode('utf8')
            time=csblock[0].Select("time").Text()
            host, rest = urllib2.splittype(href)
            filename= rest[rest.rindex("/")+1:]
            id=filename[:filename.rindex(".")]
            url="http://3g.ali213.net/gl/m/"+id+".html?d="+time+"&t="+type+"&n="+name
            return url
        except Exception as err:    
            return href
        

def getresult(url):
    contentAnalyst=cg_ali213_strategy_list()
    contentAnalyst.execute(url);
    content=contentAnalyst.result.content
    echo(content)
    echo(len(content.split("|")))
    return contentAnalyst.result

#getresult(URL)

class TC0(unittest.TestCase):
    def __init__(self, methodName = 'runTest'):
        super(TC0, self).__init__(methodName)
        self.contentAnalyst=cg_ali213_strategy_list()
       
    def testConfig(self):        
        self.contentAnalyst.execute("http://api.ali213.net/shouyou/game_gl.php?page=1")
        content=self.contentAnalyst.result.content
        print content,len(content.split("|"))
        self.assertGreater(len(content.split("|")),11)
        pass

        self.contentAnalyst.execute("http://api.ali213.net/shouyou/game_gl.php?page=2")
        content=self.contentAnalyst.result.content
        print content,len(content.split("|"))
        self.assertGreater(len(content.split("|")),14)
        pass

        self.contentAnalyst.execute("http://api.ali213.net/shouyou/game_gl.php?page=3")
        content=self.contentAnalyst.result.content
        print content,len(content.split("|"))
        self.assertGreater(len(content.split("|")),14)
        pass


    



if __name__=="__main__":#sys.exit(0)         
    unittest.main()
