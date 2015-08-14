import sys
sys.path.append("modules")
from core.framework import *

class cbh21ListAnalyst(PythonContentAnalyst):

    def setConfig(self,url):
        self.config.cfgUrl=url
        self.config.cfgCharset=self.enum.Charset.utf8
        self.config.cfgSelector=self.enum.Selector.csquery        
        self.config.cfgContent.Type=self.enum.ContentType.index
        self.config.cfgTitle=[]
        self.config.cfgAuthor=[]
        self.config.cfgSummary=[]
        self.config.cfgSource=[]
        self.config.cfgIssuedate=[]
        self.config.cfgContent.Path=["div.news_list ul>li a"]                      
        self.config.cfgContent.Options.Excludes=[]     
        self.config.cfgContent.Options.Lamda=lambda *csblock:self.baseurl+"/"+csblock[0].Attr("href")#客户端确定的链接块
        self.config.cfgContent.Pages=[] 
        self.config.cfgContent.Options.PageLamda=lambda *x:x[1]
        self.config.cfgContent.Options.PageNum=0
        self.config.cfgContent.Options.PageSimilarity=0.95
        return self.config  

    def csqueryPagination(self, csdom, pagesPath):
        return super(cbh21ListAnalyst, self).csqueryPagination(csdom, pagesPath)    

   
def getresult(url=''):  
    proto, rest = urllib2.splittype(url)  
    host, rest = urllib2.splithost(rest)  
    paths=rest.lstrip("/").split("/")
    paths[0]="html"
    timespan = time.strftime('%Y-%m-%d',time.localtime(time.time())).split("-")
    paths.append(timespan[0]+"-"+timespan[1])
    paths.append(timespan[2])    
    urlPrefix=proto+"://"+host+"/"+"/".join(paths)
    url=urlPrefix+"/node_1.htm"
    echo(url)
    contentAnalyst=cbh21ListAnalyst()
    contentAnalyst.baseurl=urlPrefix
    contentAnalyst.execute(url);
    content=contentAnalyst.result.content
    echo(content)
    return contentAnalyst.result.toJsonString()

####################### test case ######################
    
class cbh21ListAnalystTC(unittest.TestCase):
    def __init__(self, methodName = 'runTest'):
        super(cbh21ListAnalystTC, self).__init__(methodName)
        self.contentAnalyst=cbh21ListAnalyst()
       
    def testConfig(self):
        result=getresult("http://epaper.21cbh.com/")
        result=FunctionHelper.string2object(result)
        print result.content
        count=len(result.content.split("|"))
        self.assertGreater(count,20)
        pass
        

if __name__=="__main__":#sys.exit(0) 
    unittest.main()     




