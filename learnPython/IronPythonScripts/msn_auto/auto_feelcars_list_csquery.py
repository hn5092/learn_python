import sys
sys.path.append("modules")
from core.framework import *

#汽车探索
class feelcarsListAnalyst(PythonContentAnalyst):

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
        self.config.cfgContent.Path=["div.news_more_left li > a"]                      
        self.config.cfgContent.Options.Excludes=[]     
        self.config.cfgContent.Options.Lamda=lambda *csblock:csblock[0].Attr("href")#客户端确定的链接块
        self.config.cfgContent.Pages=[] 
        self.config.cfgContent.Options.PageLamda=lambda *x:x[1]
        self.config.cfgContent.Options.PageNum=1
        self.config.cfgContent.Options.PageSimilarity=0.95
        return self.config  

    def csqueryPagination(self, csdom, pagesPath):
        return super(feelcarsListAnalyst, self).csqueryPagination(csdom, pagesPath)

   
def getresult(url=''):   
    contentAnalyst=feelcarsListAnalyst()
    contentAnalyst.execute(url);
    content=contentAnalyst.result.content
    echo(content)
    return contentAnalyst.result.toJsonString()

#getresult(URL)

####################### test case ######################
    
class feelcarsListAnalystTC(unittest.TestCase):
    def __init__(self, methodName = 'runTest'):
        super(feelcarsListAnalystTC, self).__init__(methodName)
        self.contentAnalyst=feelcarsListAnalyst()
       
    def testConfig(self):
        result=getresult("http://www.feelcars.com/zhuanzai/index.shtml")        
        result=FunctionHelper.string2object(result)
        count=len(result.content.split("|"))
        self.assertGreater(count,50)
        

if __name__=="__main__":#sys.exit(0) 
    unittest.main()     




