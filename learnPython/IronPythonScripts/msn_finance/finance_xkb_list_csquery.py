import sys
sys.path.append("modules")
from core.framework import *

#新快报
class XkbListAnalyst(PythonContentAnalyst):

    def setConfig(self,url):
        self.config.cfgUrl=url
        self.config.cfgCharset=self.enum.Charset.utf8
        self.config.cfgSelector=self.enum.Selector.csquery
        self.config.cfgTitle=[]
        self.config.cfgAuthor=[]
        self.config.cfgSummary=[]
        self.config.cfgSource=[]
        self.config.cfgIssuedate=[]
        self.config.cfgContent.Type=self.enum.ContentType.index
        self.config.cfgContent.Path=["div.xx ul > li > a"]                      
        self.config.cfgContent.Options.Excludes=[]     
        self.config.cfgContent.Options.Lamda=lambda *csblock:self.lamda(csblock[0])#客户端确定的链接块
        self.config.cfgContent.Pages=[] 
        self.config.cfgContent.Options.PageLamda=lambda *x:x[1]
        self.config.cfgContent.Options.PageNum=0
        self.config.cfgContent.Options.PageSimilarity=0.95
        return self.config  

    def csqueryPagination(self, csdom, pagesPath):
        return super(XkbListAnalyst, self).csqueryPagination(csdom, pagesPath)

    def lamda(self,csrow):
        text=csrow.Text()
        url=""
        if len(text)>4:
            href=csrow.Attr("href")
            base=FunctionHelper.urlSegments(self.config.cfgUrl)
            url=FunctionHelper.getUrl(base,href)
        return url

    def getresult(self,url=''): 
       contentAnalyst=self
       begtime=4
       endtime=11
       Debug=False
       now=time.localtime()#判断时间
       if now[3]>begtime and now[3]<endtime or Debug==True:
           proto, rest = urllib2.splittype(url)  
           host, rest = urllib2.splithost(rest)  
           paths=rest.lstrip("/").split("/")
           paths[2]="html"
           timespan = time.strftime('%Y-%m-%d',time.localtime(time.time())).split("-")
           paths.append(timespan[0]+"-"+timespan[1])
           paths.append(timespan[2])    
           urlPrefix=proto+"://"+host+"/"+"/".join(paths)
           url=urlPrefix+"/node_293.htm"           
           echo(url)        
           contentAnalyst.baseurl=urlPrefix
           contentAnalyst.execute(url);
           content=contentAnalyst.result.content
           echo(content)        
       else:
           contentAnalyst.result.status="304"
           contentAnalyst.result.errormassage="#新快报#更新时间为1:00-4:00，之外不再更新了。"
           contentAnalyst.result.content="|"
    
       return contentAnalyst.result.toJsonString()

def getresult(url=''):
    contentAnalyst=XkbListAnalyst()
    return contentAnalyst.getresult(url)
   

#getresult(URL)

####################### test case ######################
    
class XkbListAnalystTC(unittest.TestCase):
    def __init__(self, methodName = 'runTest'):
        super(XkbListAnalystTC, self).__init__(methodName)
        self.contentAnalyst=XkbListAnalyst()
       
    def testConfig(self):
        result=getresult("http://www.ycwb.com/ePaper/xkb/paperindex.htm")        
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




