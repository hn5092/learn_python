import sys
sys.path.append("modules")
from core.framework import *


timeBegin=4
timeEnd=11

#京华时报
class JinghuaListAnalyst(PythonContentAnalyst):

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
        self.config.cfgContent.Path=["div#page-wrap div.info-col dl dt a"]                      
        self.config.cfgContent.Options.Excludes=[]     
        self.config.cfgContent.Options.Lamda=lambda *csblock:self.lamda(csblock[0])#客户端确定的链接块
        self.config.cfgContent.Pages=[] 
        self.config.cfgContent.Options.PageLamda=lambda *x:x[1]
        self.config.cfgContent.Options.PageNum=0
        self.config.cfgContent.Options.PageSimilarity=0.95
        return self.config  

    def csqueryPagination(self, csdom, pagesPath):
        return super(JinghuaListAnalyst, self).csqueryPagination(csdom, pagesPath)

    def lamda(self,csrow):               
        href=csrow.Attr("href")
        if not href:
            return ""
        base=FunctionHelper.urlSegments(self.config.cfgUrl)
        url=FunctionHelper.getUrl(base,href);
        req=HttpRequest2()
        req.get(url)
        htm=req.responseText.decode(self.config.cfgCharset,"ignore")
        cshtm=CsQuery.CQ.Create(htm)
        cdareas=cshtm.Select("area")
        results=[]
        for i,v in enumerate(cdareas):
            csdom=CsQuery.CQ.Create(v)
            href=csdom.Attr("href")
            url=FunctionHelper.getUrl(base,href)
            results.append(url)
            
        return results  

    def getresult(self,url=''):
        contentAnalyst=self
        now=time.localtime()#判断时间
        Debug=False
        if now[3]>timeBegin and now[3]<timeEnd or Debug==True:
            proto, rest = urllib2.splittype(url)  
            host, rest = urllib2.splithost(rest)  
            paths=rest.lstrip("/").split("/")
            paths[0]="html"
            timespan = time.strftime('%Y-%m-%d',time.localtime(time.time())).split("-")
            paths.append(timespan[0]+"-"+timespan[1])
            paths.append(timespan[2])    
            urlPrefix=proto+"://"+host+"/"+"/".join(paths)
            url=urlPrefix+"/node_100.htm"
            echo(url)        
            contentAnalyst.baseurl=urlPrefix
            contentAnalyst.execute(url);
            content=contentAnalyst.result.content
            echo(content)        
        else:
            contentAnalyst.result.status="304"
            contentAnalyst.result.errormassage="#京华时报#更新时间为4:00-11:00，之外不再更新了。"
            contentAnalyst.result.content="|"
    
        return contentAnalyst.result.toJsonString()

   
def getresult(url=''):   
    contentAnalyst=JinghuaListAnalyst()
    return contentAnalyst.getresult(url)

#getresult(URL)

####################### test case ######################
    
class JinghuaListAnalystTC(unittest.TestCase):
    def __init__(self, methodName = 'runTest'):
        super(JinghuaListAnalystTC, self).__init__(methodName)
        self.contentAnalyst=JinghuaListAnalyst()
       
    def testConfig(self):
        result=getresult("http://epaper.jinghua.cn/")        
        result=FunctionHelper.string2object(result)
        count=len(result.content.split("|"))
        now=time.localtime()#判断时间
        if Debug==True:
            self.assertGreater(count,50) 
        elif (now[3]<timeBegin or now[3]>timeEnd) :
            self.assertEqual(count,2)
        else:
            self.assertGreater(count,50)
        pass        

if __name__=="__main__":#sys.exit(0) 
    unittest.main()     




