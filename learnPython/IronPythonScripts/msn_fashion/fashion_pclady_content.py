import sys
sys.path.append("modules")
from core.framework import *


class FashionPcladyContentAnalyst(PythonContentAnalyst):

    def setConfig(self,url):   
                
        self.config.cfgUrl=url
        self.config.cfgCharset=self.enum.Charset.gb2312
        self.config.cfgSelector=self.enum.Selector.xpath
        self.config.cfgTitle=["id('artMain')/div/h1"]
        self.config.cfgAuthor=[("id('author_baidu')",lambda value:value[3:])]
        self.config.cfgSummary=[]
        self.config.cfgSource=["id('source_baidu')/a"]
        self.config.cfgIssuedate=["id('pubtime_baidu')"]
        self.config.cfgContent.Pages=["//div[@class='pclady_page']"]
        self.config.cfgContent.Path=["id('artText')"]        
        return
    
    #content dom
    def xpathConents(self,domPages):
        result=[]
        for index,item in enumerate(domPages):            
            csbody=item.Select('body')
            content=csbody.Html()            
            result.append(content)
        text="@@abcMSNPageMarkerabc@@".join(result) 
        self.result.content=text
        print text


contentAnalyst=FashionPcladyContentAnalyst()
contentAnalyst.execute("http://dress.pclady.com.cn/119/1191845.html");
result=contentAnalyst.result
pass
