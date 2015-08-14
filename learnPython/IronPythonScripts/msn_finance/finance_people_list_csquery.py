import sys
sys.path.append("modules")
from core.framework import *

class PeopleListAnalyst(PythonContentAnalyst):

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
        self.config.cfgContent.Pages=[".ej_page1"]
        self.config.cfgContent.Path=["ul.list_14 > li > a"]        
        self.config.cfgContent.Options.Excludes=[]       
        self.config.cfgContent.Options.Lamda=lambda *csblock:csblock[0].Attr("href")
        #self.config.cfgContent.Options.PageLamda=lambda *x:x[1]
        self.config.cfgContent.Options.PageNum=0
        self.config.cfgContent.Options.PageSimilarity=0.95
        return self.config  

    def csqueryPagination(self, csdom, pagesPath):
        results=[]
        pagePath=self.config.cfgContent.Pages[0]
        cspage=csdom.Select(pagePath)
        text=cspage.Text()
        s=text.find("共")
        e=text.find("页")
        count=string.atoi(text[s+1:e])+1
        self.config.cfgContent.Options.PageNum=count
        for i in range(2,count):
            url="http://finance.people.com.cn/GB/70846/index%d.html" % i
            results.append(url)
        return results

class TC4(unittest.TestCase):
    def __init__(self, methodName = 'runTest'):
        super(TC4, self).__init__(methodName)
        self.contentAnalyst=PeopleListAnalyst()
       
    def testConfig(self):
        self.contentAnalyst.execute("http://finance.people.com.cn/GB/70846/index1.html")
        content=self.contentAnalyst.result.content
        print content,len(content.split("|"))                   
            
        self.assertEqual((self.contentAnalyst.config.cfgContent.Options.PageNum+1)*50,len(content.split("|")))
        pass       

if __name__=="__main__":#sys.exit(0) 
    unittest.main()

    

