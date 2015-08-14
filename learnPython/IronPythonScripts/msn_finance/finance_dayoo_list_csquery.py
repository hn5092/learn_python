import sys
sys.path.append("modules")
from core.framework import *

#信息时报，原url：http://informationtimes.dayoo.com/
import json  
class DayooListAnalyst(PythonContentAnalyst):

    def setConfig(self,url):
        self.config.cfgUrl=url
        self.config.cfgCharset=self.enum.Charset.utf8
        self.config.cfgSelector=self.enum.Selector.csquery
        self.config.cfgTitle=[]
        self.config.cfgAuthor=[]
        self.config.cfgSource=[""]
        self.config.cfgSummary=[]
        self.config.cfgIssuedate=[""]
        self.config.cfgContent.Type=self.enum.ContentType.index
        self.config.cfgContent.Options.Excludes=[]    
        self.config.cfgContent.Path=["div.fixNav ul > li > a" ]
        self.config.cfgContent.Options.Lamda=lambda *csblock:self.lamda(csblock[0]) #没用到 
        self.config.cfgContent.Pages=[] 
        self.config.cfgContent.Options.PageNum=0 #0=限制 
        self.config.cfgContent.Options.PageLamda=lambda *x:x[1]
        self.config.cfgContent.Options.PageSimilarity=0.95 #相似度
        return self.config

    def csqueryPagination(self, csdom, pagesPath):
        return super(DayooListAnalyst, self).csqueryPagination(csdom, pagesPath)

    def csqueryConents(self,cshyperblocks):
        results=[]
        base=FunctionHelper.urlSegments(self.config.cfgUrl)
        timespan = time.strftime('%Y-%m-%d',time.localtime(time.time()))   
        contentUrl='http://epaper.xxsb.com/showColumnList.action?dateString=%s' % timespan
        req=HttpRequest2()
        req.get(contentUrl)
        jsonstring=req.responseText.decode(self.config.cfgCharset,"ignore")
        #target = json.JSONDecoder().decode(jsonstring)#Newtonsoft.Json.JsonConvert.SerializeObject(combines)
        target = Newtonsoft.Json.JsonConvert.DeserializeObject(jsonstring)
        list=target["xlpipcList"]
        for i,v in enumerate(list):
            info=v["pageInfo"]
            name=str(info["pagename"])            
            if name.find("广告")>-1 or name=="体育" or name=="竞彩专版" or name=="天天福彩" or name=="体彩闲情":
                continue
            pageArticleList=v["pageArticleList"]
            for i,v in enumerate(pageArticleList):
                title=v["title"]
                id=v["id"]                
                href="showNews/%s/%s.html" % (timespan,id)
                url=FunctionHelper.getUrl(base,href)
                results.append(url)
        return results


    def lamda(self,csrow):
        return ""    #没有找到json文件之前，使用下面的代码获取contenturl，速度太慢了,放弃         
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
        url="http://epaper.xxsb.com/showMainDZB.html"
        proto, rest = urllib2.splittype(url)  
        host, rest = urllib2.splithost(rest)  
        paths=rest.lstrip("/").split("/")    
        urlPrefix=proto+"://"+host+"/"  
        #信息时报
        timeBegin=1
        timeEnd=5
        if now[3]>timeBegin and now[3]<timeEnd or Debug==True:        
            echo(url)        
            contentAnalyst.baseurl=urlPrefix
            contentAnalyst.execute(url);
            content=contentAnalyst.result.content
            echo(content)        
        else:
            contentAnalyst.result.status="304"
            contentAnalyst.result.errormassage="#信息时报#更新时间为1:00-4:00，之外不再更新了。"
            contentAnalyst.result.content="|"
    
        return contentAnalyst.result.toJsonString()

   
def getresult(url=''): 
    try:
        contentAnalyst=DayooListAnalyst()        
        return contentAnalyst.getresult(url)
    except Exception as err:
        tp,val,td = sys.exc_info()
        tracestr=traceback.format_exc()            
        output=[tracestr,str(tp),str(val),str(td)]
        errMsg="Raise Message:"+"；".join(output)
        echo(errMsg)
        if contentAnalyst.result.status==200:
            contentAnalyst.result.status=20050
        contentAnalyst.result.erronmassage=contentAnalyst.result.erronmassage+";"+errMsg
        contentAnalyst.result.errormassage=contentAnalyst.result.erronmassage
        return contentAnalyst.result.toJsonString()

#getresult(URL)
####################### test case ######################
    
class DayooListAnalystTC(unittest.TestCase):
    def __init__(self, methodName = 'runTest'):
        super(DayooListAnalystTC, self).__init__(methodName)
        self.contentAnalyst=DayooListAnalyst()
       
    def testConfig(self):
        result=getresult("http://epaper.xxsb.com/showMainDZB.html")    
        result=FunctionHelper.string2object(result)
        str_u=result.content
        print str_u
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
     





