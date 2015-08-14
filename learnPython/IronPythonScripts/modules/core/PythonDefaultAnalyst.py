#coding:utf-8

from __future__ import division  
import clr
clr.AddReferenceToFile("CsQuery.dll")
clr.AddReferenceToFile("commandLine.dll")
from commandLine import *
import CsQuery 
import urllib2
import re
import string 
import framework

PythonCore=framework

class PythonDefaultAnalyst(object):
    result=PythonCore.GrabberRequestInfo()    
    __responseText=""
    __lastModified=""
    __contentType=""
    __cacheControl=""
    __charset=""
    __CsTextDivs=[]
    __CsTextTopOne=None

    def __getCharset(self):
        if self.__charset:
            return

        #文档中的charset优先
        if not self.__charset:
            m=re.search(r'<meta.+?charset=[^\s/]+',self.__responseText)            
            if m:
                m2=re.search(r'charset=[^\s/]+',self.__responseText)
                if m2:
                    charset=m2.group(0).split("=")[1]
                    charset,num=re.subn(r'[\'"]','',charset)
                    self.__charset=charset
            else:
                pass

        #head中的charset
        if not self.__charset:
            begin=self.__contentType.find("charset=")
            if begin>-1:
                self.__charset=self.__contentType[begin+8:]
                
        if not self.__charset:
            self.__charset="utf-8" 

    def __del__(self):
        self.__responseText=None
        self.__lastModified=None
        self.__contentType=None
        self.__cacheControl=None
        self.__charset=None
        self.__CsTextDivs=None
        self.__CsTextTopOne=None

    def execute(self,url=""):
        if not url:
            return
        print "ic,"
        pages_url=[]
        pages=[] #分页变量
        results=[]
        html=""

        req=PythonCore.HttpRequest2()        
        req.get(url)

        self.__cacheControl=req.cacheControl
        self.__contentType=req.contentType
        self.__lastModified=req.lastModified
        self.__responseText=req.responseText
        self.result.status=req.status        
        self.result.errormassage=req.errormassage
                
        if not self.__charset:
            self.__getCharset()

        charset=self.__charset.lower()
        if charset=="gbk":
            self.__charset="gb2312"
            html=self.__responseText.decode("gb2312","ignore")
        else:
            html=self.__responseText.decode(charset)

        html=self.replaceHtmlText(html)
        csdom=CsQuery.CQ.Create(html)
        csbody = csdom.Select("body")
        pages.append(csbody)

        #查询分页链接
        cssuperlinks=csdom.Select("a")        
        for index,elem in enumerate(cssuperlinks):
            href=elem.Attributes["href"]
            if href and href[0:1]=="/":
                 proto, rest = urllib2.splittype(url)  
                 host, rest = urllib2.splithost(rest)
                 href=proto+"://"+host+href
                 print href

            text=CsQuery.CQ.Create(elem).Text().strip()#链接文本的长度
            if href==None:
                continue
            simlilar=0.0
            rate=FunctionHelper.LevenshteinDistance(url, href,simlilar);
            if rate[1]>0.95 and rate[1]<1 and len(text)<4 and len(text)>0:#文本长度[1-3]，对应页码"1"，"第一页"等。
                pages_url.append(href)

        #删除重复的url
        pages_url.sort()
        pages_url= set(pages_url)
        
                
        for idx,href in enumerate(pages_url):
            req_page=PythonCore.HttpRequest2()        
            req_page.get(href)
            page_html=html=req_page.responseText.decode(self.__charset) 
            page_html=self.replaceHtmlText(page_html)
            cs_page_dom=CsQuery.CQ.Create(page_html)
            pages.append(cs_page_dom.Select("body"))

        for idx,csbody in enumerate(pages):
            self.__CsTextTopOne=None #每次循环要清空临时变量

            csdiv = csbody.Children("div")
            for i,div in enumerate(csdiv):
                nodeName=div.NodeName
                csdiv=CsQuery.CQ.Create(div)
                p=csdiv.Find("p")
                br=csdiv.Find("br")
                if p.Length+br.Length==0:#没有p和br的div节点直接抛弃
                    continue

                factor = self.GetDivFactor(div)  
                if factor["type"]=="unknow"  or factor["type"]=="text":        
                    self.TopToDown(factor)

            #找到文本块之后
            cstarget=self.__CsTextTopOne["csdom"] #获取返回的正文部分
            if cstarget==None:
                continue

            parags=cstarget.Children("p")
            if parags.Length==0:#如果文本块不存在直接p节点，说明是个多div块
                isAfter=False#是否为文本块(p)之后,初始为false
                children=cstarget.Children()
                for idx,elem in enumerate(children):
                    dom=CsQuery.CQ.Create(elem) 
                    length=dom.Find("p").Length
                    if isAfter==False and length>0:#从前向后，没有找到含p块
                        isAfter=True 
                    elif isAfter==True and length>0:#含p块已经找到，但本块依然有p，放过
                        continue                      
                    elif isAfter==True and length==0:#含p块已经找到，且本块没有p，删除
                        elem.Remove()
                           
            children=cstarget.Select("p").NextAll()  #对正文(p区)部分再次清理，主要是清理链接块                   
            for index,elem in enumerate(children):
                nodename=elem.NodeName
                if nodename!="P" and nodename!="TABLE":#保留table和p
                    csdiv=CsQuery.CQ.Create(elem)                   
                    factor=self.GetDivFactor(elem)
                    type=factor["type"]
                    if type!="text":                    
                        elem.Remove()
            
            #对dom和html调用通用清理脚本
            self.removeDom(cstarget)
            result=cstarget.Html()           
            print result
            results.append(result)

        content= "@@abcMSNPageMarkerabc@@".join(results)

        pages_url=None
        pages=None #分页变量
        results=None
        html=None

        return content

    def GetDivFactor(self,div): 
        csdiv=CsQuery.CQ.Create(div) 
        self.removeDom(csdiv) 
        
        text=csdiv.Text()
        print text

        text=self.removeNoteText(csdiv.Text())
        realTextLength=text.Length
        innerTextLength=realTextLength        
        hyperTextLength=0            
        pureTextLength=0
        imageTextLength=0        

        csdiv.Select("a img").Remove()
        elems=csdiv.Select("a")
        for index,elem in enumerate(elems):              
            if elem.NodeName=="A":
                cselem=CsQuery.CQ.Create(elem) 
                count=cselem.Text().Length
                if count==0:
                   title=cselem.Attr("title")
                   if title:
                       count=len(title)
                   else:
                       count=2 #链接中没有文字，可能是图片链接，默认至少添加2个字
                hyperTextLength+=count
        
        elems=csdiv.Select("img")
        for index,elem in enumerate(elems):
            if elem.NodeName=="IMG":
                cselem=CsQuery.CQ.Create(elem)
                alt=cselem.Attr("alt")
                if alt:
                    imageTextLength+=len(alt)
                else:
                    continue

        pureTextLength=innerTextLength+imageTextLength-hyperTextLength
        if pureTextLength>900:
            pureTextLength=900

        type="unknow"
        if innerTextLength>hyperTextLength and innerTextLength>0 and hyperTextLength/innerTextLength<0.5:
            type="text"
        elif innerTextLength>0 and hyperTextLength>=innerTextLength and hyperTextLength/innerTextLength>0.73:
            type="hyper"
        elif innerTextLength==0:
            type="none"            

        return {"csdom":csdiv
                ,"realTextLength":realTextLength
                ,"innerTextLength":innerTextLength
                ,"hyperTextLength":hyperTextLength
                ,"imageTextLength":imageTextLength
                ,"pureTextLength":pureTextLength
                ,"type":type}          
    
    #判断最后一个div
    def isLastDiv(self,csdiv):
        dl=csdiv.Find("div").Length;
        hl = csdiv.Find("H1").Length;    
        if dl+hl>0:
            return False
        else:            
            return True 

    #删除注释文字
    def removeNoteText(self,text):
        text,number=re.subn("\s","",text)
        text,number=re.subn("<!--[^>]*?>",'',text)
        return text

         #文字替换
    def replaceHtmlText(self,text):        
        text,number=re.subn("<!--[^>]*?>",'',text)
        text,number=re.subn('<strong[^>]*?>','<span>',text)
        text,number=re.subn('</strong>','</span>',text)
        text,number=re.subn('<article>','<div>',text)
        text,number=re.subn('</article>','</div>',text)
        return text

    #移除dom
    def removeDom(self,csdom):
        csdom.Select("style").Remove()
        csdom.Select("script").Remove()
        csdom.Select("iframe").Remove()
        csdom.Select("object").Remove() 
        csdom.Select("textarea").Remove()         
        csdom.Select("!--").Remove()

    #计算最大文本块
    def setDivTopOne(self,factor):
        csdom=factor["csdom"]
        if factor["type"]=="text":                 
            if self.__CsTextTopOne==None:
                self.__CsTextTopOne=factor
            else:
                topOne=self.__CsTextTopOne
                topLength=topOne["pureTextLength"]
                topreal=topOne["realTextLength"]
                currentLength=factor["pureTextLength"]                
                currentReal=factor["realTextLength"]
                if currentLength>topLength:
                    self.__CsTextTopOne=factor 
                elif currentLength==topLength and currentReal>topreal:
                    self.__CsTextTopOne=factor 

    #自定向下开始遍历div
    def TopToDown(self,factor):
        csdiv=factor["csdom"]
        if  self.isLastDiv(csdiv):
            p = csdiv.Find("p")  
            if p.Length>0:# 完全没有p的div抛弃
                self.setDivTopOne(factor)
        else:         
            
            attr=csdiv.Attr("class")
            if attr=="article-contents" :
                pass
                           
            p_find=csdiv.Find("p")  #完全没有p的div，直接抛弃掉  
            div_children=csdiv.Children("div")
            p = csdiv.Children("p") 
            br = csdiv.Children("br")
            if factor["type"] == "text" and p.Length+br.Length > 0:
                 self.setDivTopOne(factor)                 
            elif factor["type"] == "text" and p.Length+br.Length == 0 and p_find.Length>0 and div_children.Length>1:#针对sohu取不到图片做的优化，
                children = csdiv.Children("div")
                all_text=True
                for index,div in enumerate(children):
                     f0=self.GetDivFactor(div)  
                     if f0["type"]!="text":
                         all_text=False
                         break
                if all_text:
                    self.setDivTopOne(factor)
                else:
                    children = csdiv.Children("div")
                    for index,div in enumerate(children):
                        f1=self.GetDivFactor(div)  
                        if f1["type"]=="unknow"  or f1["type"]=="text":    
                            self.TopToDown(f1)    
            else:
                attr=csdiv.Attr("class")
                if attr=="article-contents" :
                    pass
                children = csdiv.Children("div")
                for index,div in enumerate(children):                    
                    factor=self.GetDivFactor(div)  
                    if factor["type"]=="unknow"  or factor["type"]=="text":    
                        self.TopToDown(factor)         
                    

default=PythonDefaultAnalyst()  
#content=default.execute("http://finance.sina.com.cn/china/dfjj/20141024/141320633437.shtml"); 
#content=default.execute("http://business.sohu.com/20141024/n405414835.shtml")
content=default.execute("http://money.163.com/14/1024/02/A99P5UTE00253B0H.html")


print content
pass   
#http://news.cheshi.com/20140804/14
#http://news.bitauto.com/duoche/20140803/1306471717.html538 多页
#http://www.autohome.com.cn/news/201408/832295.html14.shtml
#http://news.cheshi.com/20140804/1453814.shtml
#http://money.163.com/14/0811/18/A3CUP5H300254TFQ.html
#http://news.cheshi.com/20140804/1453814.shtml            
#http://business.sohu.com/20140811/n403310330.shtml 丢图片
#http://finance.qq.com/original/caijingguancha/f1238.html 分页获取的不准确
