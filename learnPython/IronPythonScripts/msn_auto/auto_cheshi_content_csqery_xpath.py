import sys
sys.path.append("modules")
from core.framework import *

class CheshiContentAnalyst(PythonContentAnalyst):

    def setConfig(self,url): 
        self.config.cfgUrl=url
        self.config.cfgCharset=""
        self.config.cfgSelector=self.enum.Selector.xpath
        self.config.cfgTitle=["id('article_new')/div[1]/h1"]
        self.config.cfgAuthor=["id('author_baidu')/a"]
        self.config.cfgSource=["id('source_baidu')/a"]
        self.config.cfgSummary=[]
        self.config.cfgIssuedate=["id('pubtime_baidu')"]
        self.config.cfgContent.Type=self.enum.ContentType.text
        self.config.cfgContent.Pages=["id('article')/div[1]/p"]
        self.config.cfgContent.Path=["id('article')"] 
        self.config.cfgContent.Options.Excludes=["p:last-child","ul"] #text body,Filters=[] #index body        
        self.config.cfgContent.Options.PageSimilarity=0.95
        self.config.cfgContent.Options.PageNum=0
        self.config.cfgContent.Options.PageLamda=lambda *x:x[1]
        self.config.cfgContent.Options.Lamda=None #lambda x:x
        return self.config

    #
    def xpathPagination(self,xpathNode,pagesPath):
        return super(CheshiContentAnalyst,self).xpathPagination(xpathNode,pagesPath)
    
    #content dom
    def xpathConents(self,csdompagination):        
        results=[]
        for index,item in enumerate(csdompagination):            
            csbody=item.Select('body')            
            csbody.Children('p').Last().NextAll().Remove()
            csbody.Select("ul").Remove()                      
            results.append(csbody)
        return results
        

class CheshiCQContentAnalyst(PythonContentAnalyst):

    def setConfig(self,url):
        self.config.cfgUrl=url
        self.config.cfgCharset=""
        self.config.cfgSelector=self.enum.Selector.csquery
        self.config.cfgTitle=["#article_new div.summary_title > h1"]
        self.config.cfgAuthor=["#article_new div.summary_title span#author_baidu > a"]
        self.config.cfgSource=["#article_new div.summary_title span#source_baidu > a"]
        self.config.cfgSummary=[]
        self.config.cfgIssuedate=["#article div.summary_title span#pubtime_baidu"]
        self.config.cfgContent.Pages=["#article div.sum_page_box p"]
        self.config.cfgContent.Path=["#article"]
        self.config.cfgContent.Type=self.enum.ContentType.text
        self.config.cfgContent.Options.Excludes=[] #text body,Filters=[] #index body        
        self.config.cfgContent.Options.PageSimilarity=0.95
        self.config.cfgContent.Options.PageNum=0
        self.config.cfgContent.Options.PageLamda=lambda *x:x[1]
        self.config.cfgContent.Options.Lamda=lambda *x:x[1]
        
        return self.config

    
    def csqueryPagination(self,csdom,pagesPaths):
        return super(CheshiCQContentAnalyst,self).csqueryPagination(csdom,pagesPaths)
    
    
    def csqueryConents(self,csdompagination):        
        results=[]
        for index,cspage in enumerate(csdompagination):            
            csbody=cspage       
            print csbody.Html()    
            csbody.Children('p').Last().NextAll().Remove()
            csbody.Select("ul").Remove()                      
            results.append(csbody)
        return results


def getresult(url=''):   
    cscontentAnalyst=CheshiCQContentAnalyst()
    cscontentAnalyst.execute(url);
    result1=cscontentAnalyst.result

    xpathcontentAnalyst=CheshiContentAnalyst()
    xpathcontentAnalyst.execute(url);
    result2=xpathcontentAnalyst.result
    print result1.content==result2.content
    pass


if __name__=="__main__":
    url="http://news.cheshi.com/20140804/1453814.shtml"
    getresult(url)
    pass

