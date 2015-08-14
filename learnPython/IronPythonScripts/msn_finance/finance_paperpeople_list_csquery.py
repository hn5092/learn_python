import sys
sys.path.append("modules")
from core.framework import *

import time
class PaperPeopleListAnalyst(PythonContentAnalyst):     

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
        self.config.cfgContent.Path=["div#titleList li > a"]                      
        self.config.cfgContent.Options.Excludes=[]     
        self.config.cfgContent.Options.Lamda=lambda *csblock:self.getHref(csblock) #客户端确定的链接块
        self.config.cfgContent.Pages=["div#pageList"] 
        self.config.cfgContent.Options.PageLamda=lambda *x:self.hyperFilter(x[2]) and self.urlPrefix+"/"+x[1].lstrip(".")
        self.config.cfgContent.Options.PageNum=0
        self.config.cfgContent.Options.PageSimilarity=0.95
        return self.config  

    def getHref(self,csblock):        
        href=csblock[0].Attr("href")
        if href.startswith("http"):
            return href
        else:
            return  self.urlPrefix+"/"+href

    def csqueryPagination(self, csdom, pagesPath):
        return super(PaperPeopleListAnalyst, self).csqueryPagination(csdom, pagesPath)

    def hyperFilter(self,text):
        if text.find("要闻")>-1 or text.find("综合")>-1  or text.find("经济")>-1 :#or text.find("经济周刊")>-1 or text.find("财经纵横")>-1 or text.find("产经广场")>-1:
            return True
        else:
            return False

   
def getresult(url=''): 
    proto, rest = urllib2.splittype(url)  
    host, rest = urllib2.splithost(rest)  
    paths=rest.lstrip("/").split("/")
    paths[1]="html"
    timespan = time.strftime('%Y-%m-%d',time.localtime(time.time())).split("-")
    paths.append(timespan[0]+"-"+timespan[1])
    paths.append(timespan[2])    
    urlPrefix=proto+"://"+host+"/"+"/".join(paths)
    url=urlPrefix+"/nbs.D110000renmrb_01.htm"
    echo(url)
    contentAnalyst=PaperPeopleListAnalyst()
    contentAnalyst.urlPrefix=urlPrefix
    contentAnalyst.execute(url);
    content=contentAnalyst.result.content
    echo(content)
    return contentAnalyst.result




####################### test case ######################
    
class PaperPeopleListAnalystTC(unittest.TestCase):
    def __init__(self, methodName = 'runTest'):
        super(PaperPeopleListAnalystTC, self).__init__(methodName)
        self.contentAnalyst=PaperPeopleListAnalyst()
       
    def testConfig(self):
        url="http://paper.people.com.cn/rmrb/index.html"
        result=getresult(url)
        print result.content,len(result.content.split("|"))
        self.assertGreater(len(result.content.split("|")),10)
        pass
        

if __name__=="__main__":#sys.exit(0) 
    #unittest.main()     
    def urlSegments(baseindex):
        result={
            "proto":"",
            "host":"",
            "path":[],
            "query":""
            }
        proto, rest = urllib2.splittype(baseindex)  
        host, rest = urllib2.splithost(rest) 
        result["proto"]=proto
        result["host"]=host
        path=rest             
        if rest.find("?")>-1:
            res=rest.split("?")
            path=res[0]
            query=res[1]  
            result["query"]=query

        result["path"].append(path)
        result["path"].append(path.lstrip("/").split("/"))
        print result
        return result

    import copy
    #new_list = copy.deepcopy(old_list)
    def getUrl(base,path):
        segments=copy.deepcopy(base)      
        if path.startswith("http"):
            return path
        elif path.startswith("../"):
            repath,number=re.subn("\.\./","",path)            
            spath=segments["path"][1]
            if number+1>len(spath):
                raise KeyError,("路径错误，path="+path)

            rest=spath[0:len(spath)-number-1]
            if len(rest)==0:
                rest=[]
            rest.append(repath)
            segments["path"][0]=path            
            segments["path"][1]=rest
            segments["query"]=""

        elif path.startswith("?"):
            segments["query"]=path.lstrip("?")

        elif path.startswith("./"):
            path=path.lstrip(".").lstrip("/")
            filepath=segments["path"][1]
            filepath[len(filepath)-1]=path
            segments["query"]=""

        else:
            path=path.lstrip(".").lstrip("/")
            filepath=segments["path"][1]
            filepath[len(filepath)-1]=path
            segments["query"]=""

        if len(segments["query"])>0:
            segments["query"]="?"+segments["query"]

        url="%s://%s/%s%s" % (segments["proto"],segments["host"],"/".join(segments["path"][1]),segments["query"])
        echo(url)
        return url

    base=urlSegments("http://www.sohu.com/html/index?abc=1")
    getUrl(base,"content");
    getUrl(base,"./content");
    getUrl(base,"./content/aaa")
    getUrl(base,"./content/aaa?abc=2")
    getUrl(base,"../xml/content?abc=2")
    getUrl(base,"?wc=456")
    pass



