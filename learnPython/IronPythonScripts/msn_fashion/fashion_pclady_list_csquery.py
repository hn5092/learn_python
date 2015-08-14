import sys
sys.path.append("modules")
from core.framework import *


class CSFashionPcladyListAnalyst(PythonContentAnalyst):

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
        self.config.cfgContent.Pages=[".pclady_page"]
        self.config.cfgContent.Path=[".content > .layAB > ul > li .eTit > a"]        
        self.config.cfgContent.Options.Excludes=[]       
        #self.config.cfgContent.Options.Lamda=lambda *csblock:len(csblock[0].Text())>0 and csblock[0].Attr("href") or ""
        self.config.cfgContent.Options.PageLamda=lambda *x:x[1]
        self.config.cfgContent.Options.PageNum=3
        self.config.cfgContent.Options.PageSimilarity=0.95
        return self.config
    
    #index dom
    def csqueryConents(self,csdompages):
        results=[]
        for index,cspage in enumerate(csdompages):
            for idx,hyperblock in enumerate(cspage):
                cshyper=CsQuery.CQ.Create(hyperblock)
                text=cshyper.Text()
                if len(text)>0:
                    results.append(cshyper.Attr("href")) 
                
        text="<br/>".join(results)       
        print text
        return results

if __name__=="__main__":
    contentAnalyst=CSFashionPcladyListAnalyst()
    contentAnalyst.execute("http://dress.pclady.com.cn/fashion/index.html");
    result=contentAnalyst.result
    pass
