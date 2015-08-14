import sys
sys.path.append("modules")
from core.framework import *


class FashionPcladyListAnalyst(PythonContentAnalyst):

    def setConfig(self,url):   
                
        self.config.cfgUrl=url
        self.config.cfgCharset=self.enum.Charset.gb2312
        self.config.cfgSelector=self.enum.Selector.xpath
        self.config.cfgTitle=["//div[@class='guide']/a[1]"]
        self.config.cfgAuthor=["//div[@class='guide']/a[2]"]
        self.config.cfgSummary=[]
        self.config.cfgSource=["id('source_baidu')/a"]
        self.config.cfgIssuedate=["id('pubtime_baidu')"]
        self.config.cfgContent.Pages=["//div[@class='pclady_page']"]
        self.config.cfgContent.Path=[("//div[@class='layAB picList']/ul",".eTit>a")]  
        self.config.cfgContent.Type=self.enum.ContentType.index
        self.config.cfgContent.Options.Excludes=[".eTime",".iPic",".sDes",".sLab"]
        self.config.cfgContent.Options.Lamda=lambda *csblock:len(csblock[0].Text())>0 and csblock[0].Attr("href") or ""
        self.config.cfgContent.Options.PageLamda=lambda *x:x[1]
        self.config.cfgContent.Options.PageNum=3
        self.config.cfgContent.Options.PageSimilarity=0.95
        return self.config
    
    #index dom
    def xpathConents(self,csdompages):
        results=[]
        for index,item in enumerate(csdompages):            
            csdom=item.Select('body').Select("em > a")
            for idx,itm in enumerate(csdom): 
                csa=CsQuery.CQ.Create(itm)     
                results.append(csa.Attr("href"))
        text="<br/>".join(results)       
        print text
        return results

if __name__=="__main__":
    contentAnalyst=FashionPcladyListAnalyst()
    contentAnalyst.execute("http://dress.pclady.com.cn/fashion/index.html");
    result=contentAnalyst.result

pass



