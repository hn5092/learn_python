import CsQuery 
import clr
import re, json
import urllib2
clr.AddReferenceToFile('CsQuery.dll','Newtonsoft.Json.dll')
import Newtonsoft





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
            "body":"",
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

#<test># 
if __name__=="__main__":
 
    def removefomate(content):
    
        #去除display:none的标签 <([^\s]+).+?display:\s*?none[^>]+>[^<>]*(((?'Open'<(?<tag>[^>]*)>)[^<>]*)+((?'-Open'</\k<tag>>)[^<>]*)+)*(?(Open)(?!))</\1>
        #<([^\s]+).+?display:\s*?none[;]*[^>]+[\s\S]*>[\s\S]+?</\1>
        p1,number=re.subn('<([^\s]+).+?display:\s*?none[^>]+>[^<>]*(((?<Open><div[^>]*>)[^<>]*)+((?<-Open></div>)[^<>]*)+)*(?(Open)(?!))</\1>','',content)
        p2,number=re.subn('<script[^>]*?>[\s\S]*?<\/script>','',p1)

        p3,number=re.subn('style=[\"|\'][\\s\\S]*?[\"|\']','',p2)
        p4,number=re.subn('<(h1|h4|select|div)+[^>]*?>[\s\S]*?</(h1|h4|select|div)+>','',p3)
        p5,number=re.subn("<div  id=\"city\"[^>]*?>[\s\S]*?</div>", "",p4)
        p6,number=re.subn('<ul class=\"con_time\"[^>]*?>[\s\S]*?</ul>','',p5)
        p7,number=re.subn("<(p|div)+[^>]*>[\s]*</(p|div)*>", "",p6)
        p8,number=re.subn("<div id=\"proComments\"[^>]*?>[\s\S]*?</div>", "",p7)
        p9,number=re.subn("<div class=\"con_nav2\"[^>]*?>[\s\S]*?</div>", "",p8)
        p10,number=re.subn("<div class=\"the_pages\"[^>]*?>[\s\S]*?</div>", "",p9)
        p11,number=re.subn("<div class=\"listbox_con\"[^>]*?>[\s\S]*?</div>", "",p10)
        p12,number=re.subn("<div class=\"the_pages_keyboard\"[^>]*?>[\s\S]*?</div>", "",p11)
        p13,number=re.subn("<p class=\"article-information\"[^>]*?>[\s\S]*?</p>", "",p12)
        p14,number=re.subn("<div class=\"con_pagelist\"[^>]*?>[\s\S]*?</div>", "",p13)
        p15,number=re.subn('</?(a|div)[^<>]*>','',p14)
        p16,number=re.subn('<br>','',p15)
        p17,number=re.subn('class=[\"|\']?.*?[\"|\']','',p16)
        return p17
 
    def getresult(url=''):    
        request= HttpRequest()
        result=request.getResponseStr(url=url,ifmodifysince='')
#         result.body=result.body.decode('GB2312')
        print result.body.decode('utf-8')
        cqhtml= PyCQ(html=result.body)
        #allpapehtml=cqhtml.select('.content').render()
        #p=re.compile("href=(\S*?)[\s|>]")
        #if allpapehtml:
        #    allpageurl='http://finance.chinanews.com/'+p.findall(allpapehtml)[0].strip('"')
        #    newresult=request.getResponseStr(url=allpageurl,ifmodifysince='')
        #    newresult.body=newresult.body.decode('gb2312')
        #    if newresult.body:
        #        result=newresult
        #        cqhtml=PyCQ(html=result.body)
        cqcontent=cqhtml.select('.article_text').eq(0)
        #articleinfo=cqcontent.select('.article_text_title02')
        result.article_properties['title']=cqcontent.select('.article_text_title01').text().strip()
        summary=""
        str=cqcontent.select('.article_text_title02').select("span").eq(0).text()
        str=str[3:]
        result.article_properties['issuedate']=str
        #src=str[str.find("来源")+3:]
        result.article_properties['source']=cqcontent.select('.article_text_title02').select("span").eq(2).select("a").text() #split 默认按空格 不需要写成split(' ')

#         author=cqcontent.select('.article_text_title02').text()
#         author=author[author.index("作者")+3:]
#         result.article_properties['author']=author[0:author.index("分享至微博")]
        result.article_properties['summary']=cqhtml.select('.content').select('p').eq(0).text().strip()
        p1con=removefomate(cqcontent.html())
    
        #先判断是否有多页
        pflag=cqhtml.select(".yahoo2").select("a").eq(1).text() ; 
     
        if pflag !="" :
            #p6="有多页"+p6.strip()
            t=cqhtml.select(".yahoo2").select("a").render() 
            p=re.compile("href=(\S*?)[\s|>]")
            hrefs=p.findall(t)  
            #这样能保存数组里面的元素原来的位置 
            #hrefs=hrefs.pop()
            hrefs.pop()
       
            hrefs2 = list(set(hrefs))
            hrefs2.sort(key=hrefs.index)
            con=""
            if hrefs2:
                for ht in hrefs2: 
                    request=  HttpRequest()
                    result2=request.getResponseStr(url=ht.strip("\""),ifmodifysince='')
                    result2.body=result2.body.decode('GB2312')
                    cqhtml2=  PyCQ(html=result2.body)
                    con+="@@abcMSNPageMarkerabc@@"+removefomate(cqhtml2.select('.article_text').eq(0).html() )
                
            result.content=p1con +con
        else:
            result.content=p1con.strip()
        
          
        return result

    getresult("https://www.baidu.com/s?ie=UTF-8&wd=this+app+has+been+blocked+for+you+protection")


    