import sys
sys.path.append("modules")
from core.framework import *

#信息时报
def csLastP(csparent):
    text=csparent.Children("p").Last().Text()
    hasEndSymbol=False
    for i in range(len(text)-1,-1,-1):
        if isEndSymbol(text[i]):
            hasEndSymbol=True
            text=text[0:i+1]
            echo(text)
            csparent.Children("p").Last().Text(text)
            break

    if hasEndSymbol==False:
        csparent.Children("p").Last().Remove()
    
    return

class DayooContentAnalyst(PythonContentAnalyst):

    def setConfig(self,url):
        self.config.cfgUrl=url
        self.config.cfgCharset=self.enum.Charset.utf8
        self.config.cfgSelector=self.enum.Selector.csquery
        self.config.cfgTitle=["p.lh30 strong"]
        self.config.cfgAuthor=[]
        self.config.cfgSource=["ul#nav li:eq(2) a"]
        self.config.cfgSummary=[]
        self.config.cfgIssuedate=[("div.info div.mt5 p:eq(3) > a:eq(0)",lambda x:x.replace("\n","").replace("\t",""))]
        self.config.cfgContent.Type=self.enum.ContentType.text
        self.config.cfgContent.Options.Excludes=[]    
        self.config.cfgContent.Path=["div.infoMain"]
        #self.config.cfgContent.Options.Lamda=lambda *x:x[1] #没用到 
        self.config.cfgContent.Pages=[] 
        self.config.cfgContent.Options.PageNum=0 #0=限制 
        self.config.cfgContent.Options.PageLamda=lambda *x:x[1]
        self.config.cfgContent.Options.PageSimilarity=0.95 #相似度
        return self.config
    
   
    def csqueryPagination(self,csdom,pagesPaths):
        '''默认实现相似度计算，可识别路径/、？'''
        return super(DayooContentAnalyst,self).csqueryPagination(csdom,pagesPaths)

    def csqueryConents(self,csdompagination):        
        results=[]
        for index,cspage in enumerate(csdompagination):            
            csbody=cspage
            csbody.Find("div.article").NextAll().Remove()            
            csLastP(csbody.Find("div.article").Children("founder-content"))
            results.append(csbody)
        return results 

    def lastCsdomp(self,lastcsdompage):
        '''最后一个段落<p>'''
        return lastcsdompage #super(DayooContentAnalyst,self).lastCsdomp(lastcsdompage)

    def pageContentText(self,content):
        """分页的内容清理，默认清空注释、style、onmouseover，粗体替换，unicode编码转汉字"""
        return super(DayooContentAnalyst,self).pageContentText(content)

    def pageCsContentImage(self,cspage):
        """本地img替换为完全img路径"""
        self.contentImages=[]
        try:
            proto, rest = urllib2.splittype(self.config.cfgUrl)  
            host, rest = urllib2.splithost(rest)
            cs_img_container=CsQuery.CQ.Create(cspage.Find("img").Parent())
            cs_input=CsQuery.CQ.Create(cspage.Find("input"))
            value=cs_input.Attr("value") #itm.Attributes["src"]
            els=value.split("&#&")
            base=FunctionHelper.urlSegments(self.config.cfgUrl)
            for i,value in enumerate(els):
                src,alt=value.split("*@*")
                url=FunctionHelper.getUrl(base,src)
                img='<img src="%s" alt="%s" style="display:block"/>' % (url,alt)
                self.contentImages.append(img)
            cspage.Find("input").Remove()                          
        except Exception as err:
            tp,val,td = sys.exc_info()
            tracestr=traceback.format_exc()            
            output=[tracestr,str(tp),str(val),str(td)]
            errMsg="Raise Message:"+"；".join(output)
            echo(errMsg)

def getresult(url=''): 
    try:  
        contentAnalyst=DayooContentAnalyst()        
        contentAnalyst.execute(url);
        content=contentAnalyst.result.content
        if contentAnalyst.contentImages and len(contentAnalyst.contentImages)>0:
            content,number=re.subn('<input[^>]*?>',"".join(contentAnalyst.contentImages),content)
            content,number=re.subn('<img[^>]*?>',"".join(contentAnalyst.contentImages),content)
        contentAnalyst.result.content=content
        echo(content)        
        return contentAnalyst.result.toJsonString()
    except Exception as err:
        tp,val,td = sys.exc_info()
        tracestr=traceback.format_exc()            
        output=[tracestr,str(tp),str(val),str(td)]
        errMsg="Raise Message:"+"；".join(output)
        echo(errMsg)
        if contentAnalyst.result.status==200:
            contentAnalyst.result.status=20051
        contentAnalyst.result.erronmassage=contentAnalyst.result.erronmassage+";"+errMsg
        contentAnalyst.result.errormassage=contentAnalyst.result.erronmassage
        return contentAnalyst.result.toJsonString()


#getresult(URL)

####################### test case ######################
    
class DayooContentAnalystTC(unittest.TestCase):
    def __init__(self, methodName = 'runTest'):
        super(DayooContentAnalystTC, self).__init__(methodName)
        self.contentAnalyst=DayooContentAnalyst()
       
    def testConfig(self):
        result=getresult("http://epaper.xxsb.com/showNews/2014-10-13/177603.html")
        result=FunctionHelper.string2object(result)
        content=result.content
        print content
        self.assertGreater(result.article_properties["title"].find("明星们真的要被玩坏"),-1  )
        self.assertGreater(result.article_properties["source"].find("信息时报"),-1)        
        self.assertGreater(result.article_properties["issuedate"].find("2014-10-13"),-1)        
        self.assertGreater(len(result.content),200)
        pass
            
        result=getresult("http://epaper.xxsb.com/showNews/2014-10-15/177991.html")
        result=FunctionHelper.string2object(result)
        content=result.content
        print content
        self.assertGreater(result.article_properties["title"].find("我的地铁时间轴"),-1  )
        self.assertGreater(result.article_properties["source"].find("信息时报"),-1)        
        self.assertGreater(result.article_properties["issuedate"].find("2014-10-15"),-1)        
        self.assertGreater(len(result.content),200)
        pass

        result=getresult("http://epaper.xxsb.com/showNews/2014-10-13/177649.html")
        result=FunctionHelper.string2object(result)
        content=result.content
        print content
        self.assertGreater(result.article_properties["title"].find("上证指数上涨15.4% 三季度A股领"),-1  )
        self.assertGreater(result.article_properties["source"].find("信息时报"),-1)        
        self.assertGreater(result.article_properties["issuedate"].find("2014-10-13"),-1)        
        self.assertGreater(len(result.content),200)
        pass       


        result=getresult("http://epaper.xxsb.com/showNews/2014-10-13/177565.html")
        result=FunctionHelper.string2object(result)
        content=result.content
        print content
        self.assertGreater(result.article_properties["title"].find("节发大奖 多少非凡建"),-1  )
        self.assertGreater(result.article_properties["source"].find("信息时报"),-1)        
        self.assertGreater(result.article_properties["issuedate"].find("2014-10-13"),-1)        
        self.assertGreater(len(result.content),200)
        pass
    


        

if __name__=="__main__":#sys.exit(0) 
    unittest.main()
