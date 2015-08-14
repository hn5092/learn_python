import clr
clr.AddReferenceToFile('CsQuery.dll','Newtonsoft.Json.dll')
import Newtonsoft
import CsQuery 
import urllib2
import re,json


#<body>#
class PyCQ:
    __cq = CsQuery.CQ()
    def __init__(self,url='',html=''):
        CsQuery.Config.HtmlEncoder=CsQuery.Output.HtmlEncoderMinimum()
        if url:
            try:
                self.__cq = CsQuery.CQ.CreateFromUrl(url)
                return 
            except:
                raise Exception('url Error')
        elif html:
            try:
                self.__cq = CsQuery.CQ.Create(html)
            except:
                raise Exception('html Error')
    def render(self):
        return self.__cq.Render()
    def find(self,selector):
        if selector:
            htmlstr = self.__cq.Find(selector)
            return PyCQ(html=htmlstr)
        else:
            return self
    def  select(self,selector):
        if selector:
            htmlstr = self.__cq.Select(selector)
            return PyCQ(html=htmlstr)
        else:
            return self
    def __getitem__(self,key):
        return self.__cq[key]
    def eq(self,index=0):
        assert type(index) is int
        return PyCQ(html=self.__cq.Eq(index))
    def text(self):
        return self.__cq.Text()
    def html(self):
        '''return element content '''
        return self.__cq.Html()
    def removeClass(self,classname=''):
        '''delete the element class'''
        if classname:
            self.__cq.RemoveClass(classname)
        else:
            self.__cq.RemoveClass()
        return self
    def remove(self,selector):
        '''delete the mathed element '''
        self.__cq.Remove(selector)
        return self
    def selectList(self,selector):
        if selector:
            htmlstr = self.__cq.Select(selector)
            PyCQList=[]
            for str in htmlstr:
                PyCQList.Add(PyCQ(html=str))
            return PyCQList    
        else:
            return self

class GrabberRequestInfo:
    def __init__(self):
        self.status=""
        self.erronmassage=""
        self.errormassage=""
        self.header={}
        self.body=""
        self.article_properties={'title':'','author':'','source':'','summary':'','issuedate':''}
        self.content=""

    def toJsonString(self): 
        combines={
            "status":self.status,
            "errormassage":self.errormassage,
            "header":self.header,
            "body":self.body,
            "article_properties":self.article_properties,
            "content":self.content
            }
        return Newtonsoft.Json.JsonConvert.SerializeObject(combines) #json.dumps(combines);       


class HttpRequest(object):
    def getResponseStr(self,url='',ifmodifysince=''):
        info=GrabberRequestInfo()
        if url:
            try:
                headers={'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
                if ifmodifysince:
                    headers['If-Modified-Since']=ifmodifysince
                    
                req=urllib2.Request(url,headers=headers)
                response=urllib2.urlopen(req)
                info.body=response.read()
                info.status=str(response.getcode())
                info.header['IfModifiedSince']=''
                if response.info().has_key('Last-Modified'):
                    info.header['IfModifiedSince']=response.info()['Last-Modified']
                response.close()
            except urllib2.HTTPError as e:
                info.status=str(e.code)
                info.erronmassage=str(e)
                info.errormassage=info.erronmassage
            except Exception as ext:
                info.erronmassage=str(ext)
                info.errormassage=info.erronmassage
                          
        return info 


URL="http://auto.163.com/special/000836P0/auto-yc.html"

local={}
gl={"HttpRequest":HttpRequest,"GrabberRequestInfo":GrabberRequestInfo,"PyCQ":PyCQ,"re":re,"urllib2":urllib2,"CsQuery":CsQuery,"Newtonsoft":Newtonsoft,"URL":URL}

script="""
def getresult(url):    
    request=HttpRequest()
    responseInfo=request.getResponseStr(url=url,ifmodifysince='')
    cqhtml=PyCQ(html=responseInfo.body.decode("gb2312"))
    cqnews=cqhtml.select(".col-lm .bd")
    linkStr=cqnews.select("a").render()
    p=re.compile("href=(\S*?)[\s|>]")
    hrefs=set(p.findall(linkStr))   
    responseInfo.content="|".join([href.strip('"') for href in hrefs if href.find('http://auto.163.com/')>-1 and href.find('.html')>-1 and href.find('special/')==-1 and href.find('photoview/')==-1])
    return responseInfo

getresult(URL)

"""
#a=compile(script, '', 'exec')
#exec(a,gl,local)
result=execfile("d6591e4ac09ab111b5650a60f0678419.py", gl, local)
print result



