import sys
sys.path.append("modules")
from core.framework import *



class FashionIfengContentAnalyst(PythonContentAnalyst):

    def setConfig(self,url):
        
        self.config.cfgUrl=url
        self.config.cfgCharset=self.enum.Charset.utf8
        self.config.cfgSelector=self.enum.Selector.xpath
        self.config.cfgTitle=["id('artical_topic')"]
        self.config.cfgAuthor=["id('artical_sth')/p/span[4]/span"]
        self.config.cfgSource=["id('artical_sth')/p/span[3]/span"]
        self.config.cfgSummary=["id('main_content')/p[1]"]
        self.config.cfgIssuedate=["id('artical_sth')/p/span[1]"]
        self.config.cfgContent.Pages=["//div[@class='pageNum ss_none ipad_block']"]
        self.config.cfgContent.Path=["id('main_content')"]
        self.config.cfgContent.Type=self.enum.ContentType.text
        self.config.cfgContent.Options.Excludes=["#embed_hzh_div","p:last-child > span"]
        self.config.cfgContent.Options.PageNum=0
        self.config.cfgContent.Options.PageSimilarity=0.95
        #config.cfgContent.Options.Lamda=lamdba *x:x[1]
        
        return self.config
        
    def xpathPagination(self,xpathNode,pagesPath):
        return super(FashionIfengContentAnalyst,self).xpathPagination(xpathNode,pagesPath)
        
        
    def xpathConents(self,csdompagination):
        return csdompagination


if __name__=="__main__":
    contentAnalyst=FashionIfengContentAnalyst()
    contentAnalyst.execute("http://fashion.ifeng.com/a/20140819/40035171_0.shtml");
    result=contentAnalyst.result
    pass


