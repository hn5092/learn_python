#coding=utf-8
import clr
clr.AddReferenceToFile("CsQuery.dll")
clr.AddReferenceToFile("CSHelper.dll","HtmlAgilityPack.dll","Newtonsoft.Json.dll")
from CSHelper import *
from HtmlAgilityPack import *
import Newtonsoft
import CsQuery
import meta
import urllib2
import re
import string 
import gzip, cStringIO,traceback
import sys
import unittest
import time,copy
Debug=False


#<head>#
CsQuery=CsQuery
IronPythonMeta=meta
GrabberRequestInfo=IronPythonMeta.GrabberRequestInfo
ClientConfig=IronPythonMeta.ClientConfig
Enum=IronPythonMeta.Enum
FunctionHelper=IronPythonMeta.FunctionHelper
Debug=True


#<body>#
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

def echo(text):
    if Debug:
        print text
    return

def isEndSymbol(symbol,endSymbols=[]):
    if len(endSymbols)==0:
        endSymbols=["”",'"',"?","？","!","！","。"]
    for i,v in enumerate(endSymbols):  
        if symbol==v:
            return True
    return False
   

class HttpRequest2(object):

    def  __init__(self):
        self.responseText=""
        self.contentType=""
        self.lastModified=""
        self.cacheControl=""
        self.status="0"
        self.errormassage=""

    def get(self,url='',ifmodifysince=''):        
        if url:
            try:
                headers={'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
                if ifmodifysince:
                    headers['If-Modified-Since']=ifmodifysince
                    
                req=urllib2.Request(url,headers=headers)
                response=urllib2.urlopen(req,timeout=20)                
                self.responseText=response.read()
                print response.read() 
                #查询返回的状态吗
                self.status=str(response.getcode())
                headerinfo=response.info()
                header={}
                if headerinfo.has_key('Last-Modified'):
                    self.lastModified=headerinfo['Last-Modified']
                if headerinfo.has_key("Content-Type"):
                    self.contentType=headerinfo['Content-Type']
                if headerinfo.has_key("Cache-Control"):
                    self.cacheControl=headerinfo["Cache-Control"]                 
                response.close()
            except urllib2.HTTPError as e:
                self.status=str(e.code)
                self.errormassage=str(e)
            except Exception as ext:
                self.errormassage=str(ext)                          
        return self 

def RemoveDom(csdom,selector):
    """删除dom节点
    example:RemoveDom(csdom,["script","iframe"])
    """
    s=[]
    if type(selector)==list:
        s=selector
    elif type(selector):
        s.append(selector)

    for index,elem in enumerate(s):
        if elem=="class":
            csdom.Select("*").RemoveClass("")
        else:
            csdom.Select(elem).Remove()

    return csdom
    

def RemoveText(content,regx): 
    """      
      content,number=re.subn('<!--[^>]*?>','',content) 
      content,number=re.subn('(?<=style=["\'])[^"\']+','',content) 
    """
    regs=[]
    if type(regx)==str:
        regs.append(regx)
    elif type(regx)==list:
        regs=regx

    for index,r in enumerate(regs):       
        content,number=re.subn(r,'',content) 

    return content
    

def ReplaceText(content,old,new):
    """
      content,number=re.subn('<strong[^>]*?>','<span>',content)
      content,number=re.subn('</strong>','</span>',content)
    """
    content,number=re.subn(old,new,content)
    return content
    pass



class PythonContentAnalyst(object):         
    __responseText=""
    __lastModified=""
    __contentType=""
    __cacheControl=""
    __charset="" 
    __url=""  
               
    def __init__(self):
        self.result=GrabberRequestInfo()  
        self.config=ClientConfig()  
        self.enum=Enum()        
         
    def __getCharset(self):

        if self.__charset:
            return

        #get charset from html head
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

        #get charset from http headers
        if not self.__charset:
            begin=self.__contentType.find("charset=")
            if begin>-1:
                self.__charset=self.__contentType[begin+8:]
                
        if not self.__charset:
            self.__charset="utf-8" 

        if self.__charset.lower()=="gbk":
            self.__charset="gb2312" 

    def clearDom(self,dom):
        dom.Select('script').Remove()
        dom.Select('iframe').Remove()
        dom.Select("object").Remove()                       
        return dom

    def defaultReplace(self,content):        
        content,number=re.subn('<strong[^>]*?>','<span>',content)
        content,number=re.subn('</strong>','</span>',content)                
        return content

    def __xpathParser(self,xpathNode,configdata):
        for i in range(len(configdata)):
            dic=configdata[i]
            name=dic["key"]
            path=dic["path"]                     
            value=""
            if name=="content":
                pages=dic["pages"]
                cfgtype=dic["type"]
                if cfgtype=="text":
                    self.__xpathContent(xpathNode,name,pages,path)
                elif cfgtype=="index":
                    self.__xpathList(xpathNode,name,pages,path)
                else: 
                    raise KeyError,("type="+type+" do not support.")
                    pass
            else:
                for index,item in enumerate(path):
                    p=item
                    lamda=None
                    if type(item)==tuple:
                        p=item[0]
                        if len(item)==2:
                            lamda=item[1]
                        
                    value=CSXPathDocument.SelectSingleText(xpathNode, p)
                    if value:
                        if lamda:value=lamda(value)
                        print name
                        value=self.getProperties(name,value)
                        self.result.article_properties[name]=value
                        print self.result.article_properties[name]
                        break        
    #解析list页面   
    def __xpathList(self,xpathNode,name,pages,paths):
        contents=[]
        for index,item in enumerate(paths):
            if type(item)==tuple:#item=(xpath,selector)                    
                path=item[0]
                selector=item[1]           
                text=CSXPathDocument.SelectSingleHtml(xpathNode,path)                    
                if text:
                    node=(path,text,selector)
                    contents.append(node)
            else:
                #config.cfgContent.Path=[("//div[@class='layAB picList']/ul",".eTit>a")]
                raise NameError,("config.cfgContent.Path=(xpath,selector),but the input is "+item)


        #page info
        pagination=self.xpathPagination(xpathNode,pages)        
        if self.config.cfgContent.Options.PageNum==0:            
            pagination=list(pagination)[0:]            
        elif self.config.cfgContent.Options.PageNum>0:
            pagination=list(pagination)[0:self.config.cfgContent.Options.PageNum-1]
        else:
            raise NameError,("self.config.cfgContent.Options.PageNum="+str(cfgContent.Options.PageNum)+", PageNum in [0-n]")

        #page content
        page_contents=[]
        for index,item in enumerate(pagination):
            req=HttpRequest2()
            req.get(item)
            h2=req.responseText.decode(self.__charset)
            docNode2=CSXPathDocument.ConvertStringToHdoc(h2)
            for idx,content in enumerate(contents):
                path=content[0]
                selector=content[2]
                content=CSXPathDocument.SelectSingleHtml(docNode2, path)
                if content:
                    node=(path,content,selector)
                    page_contents.append(node)

        contents.extend(page_contents)

        csdompages=[]
        results=[]
        for index,content in enumerate(contents):            
            pageHtml="<html><body>"+content[1]+"</body></html>";  
            selector=content[2]    
            csdompage= CsQuery.CQ.Create(pageHtml)
            if type(self.config.cfgContent.Options.Excludes)==list and len(self.config.cfgContent.Options.Excludes)>0:
                RemoveDom(csdompage,self.config.cfgContent.Options.Excludes)
            cshypers=csdompage.Select(selector)
            lamda=self.config.cfgContent.Options.Lamda
            if lamda:                
                for idx,item in enumerate(cshypers):
                    csdoma=CsQuery.CQ.Create(item)                    
                    text=csdoma.Text()
                    result=lamda(csdoma,text)
                    if result:
                        results.append(result)
            else:
                csdompages.append(csdompage)

        if len(results)==0:
            results=self.xpathConents(csdompages)

        results=list(set(results))
        text="|".join(results)

        #print text
        self.result.content=text            
                    
    #
    def __xpathContent(self,xpathNode,name,pages,path):
        contents=[]
        for index,item in  enumerate(path):
            content=CSXPathDocument.SelectSingleHtml(xpathNode,item)
            currentPath=item
            if content:                
                contents.append(content) #
                break

        pagination=self.xpathPagination(xpathNode,pages)
        for index,item in enumerate(pagination):
            req=HttpRequest2()
            req.get(item)
            h2=req.responseText.decode(self.__charset)
            docNode2=CSXPathDocument.ConvertStringToHdoc(h2)
            cont=CSXPathDocument.SelectSingleHtml(docNode2, currentPath)
            contents.append(cont)
        
        paginations=[]
        for index,item in enumerate(contents):
            text=item #self.clearText(item)
            pageHtml="<html><body>"+text+"</body></html>";           
            csdompagination= CsQuery.CQ.Create(pageHtml)            
            paginations.append(csdompagination)

        lamda=self.config.cfgContent.Options.Lamda
        if lamda:
            lamda(paginations)
        else:
            cspages=self.xpathConents(paginations)
        results=[]
        for idx,cspage in enumerate(cspages):
            RemoveDom(cspage,["style","iframe","script","object","class","head"])
            if type(self.config.cfgContent.Options.Excludes)==list and len(self.config.cfgContent.Options.Excludes)>0:
                RemoveDom(cspage,self.config.cfgContent.Options.Excludes)   
            self.pageCsContentImage(cspage)              
            content=cspage.Select("body").Html()   
            #content=RemoveText(content,['<!--[^>]*?>','(?<=style=["\'])[^"\']+','(?<=onmouseover=["\'])[^"\']+'])
            #content=self.defaultReplace(content)
            content=self.pageContentText(content)
            #content=StringHelper.EscapeUnicode(content)            
            results.append(content)
        text="@@abcMSNPageMarkerabc@@".join(results) 
        #print text
        self.result.content=text

    #分页链接获取
    def xpathPagination(self,xpathNode,pagesPath):
        pages=[]
        for index,item in enumerate(pagesPath):
            xpath=item
            content=CSXPathDocument.SelectSingleHtml(xpathNode,xpath)
            if content:
                html="<html><body>"+content+"</body></html>"
                children=CsQuery.CQ.Create(html).Select("body").Find("a")                
                if children.Length>0:
                    for i in range(0,children.Length):
                        csdoma=CsQuery.CQ.Create(children[i])  
                        href=csdoma.Attr("href")   
                        text=csdoma.Text()
                        if self.config.cfgContent.Options.PageLamda :
                            str=self.config.cfgContent.Options.PageLamda(csdoma,href,text)
                            if not str:
                                continue
                            else:
                                href=str
                        
                        if href and href[0:1]=="/":
                            proto, rest = urllib2.splittype(url)  
                            host, rest = urllib2.splithost(rest)
                            href=proto+"://"+host+href
                                             
                        scale=self.config.cfgContent.Options.PageSimilarity
                        rate=0.0
                        simlilar=StringHelper.LevenshteinDistance(self.__url,href,rate)
                        if href and simlilar[1]>scale and simlilar[1]<1:
                            pages.append(href)                    
                if pages.Count>0:
                    func = lambda x,y:x if y in x else x + [y]
                    pages=reduce(func, [[], ] + pages)                                  
        return pages
           
    #客户端方法
    def xpathConents(self,csdompagination):
       """客户端方法"""
       return csdompagination       

   #客户端方法
    def setConfig(self):
        """客户端方法"""
        pass

    #客户端方法，废弃。[已经被lambda替代]
    def getProperties(self,name,value):
        """客户端方法，废弃。[已经被lambda替代]"""
        return value
    
    def execute(self,url):
        html=""
        print "im come"
        try:        
            self.setConfig(url)
            config=self.config.Resolve()
        
            if not self.config.cfgUrl:
                raise ValueError,("config.cfgUrl is empty.")
                
            self.__url=self.config.cfgUrl
            request=HttpRequest2()
            request.get(self.__url)
            
            self.__cacheControl=request.cacheControl
            self.__contentType=request.contentType
            self.__lastModified=request.lastModified
            self.__responseText=request.responseText
            self.result.erronmassage=request.errormassage
            self.result.errormassage=self.result.erronmassage
            self.result.status=request.status
            self.result.header['IfModifiedSince']=request.lastModified

            self.__charset=config["charset"]
            if not self.__charset:
                self.__getCharset()

            echo(self.__charset)
            html=self.__responseText.decode(self.__charset,"ignore")
            self.result.body=""
            

            selector=config["selector"]
            print "selector:%s" % (selector)
            if selector=="xpath":
                docNode=CSXPathDocument.ConvertStringToHdoc(html)
                for (k,v) in config:
                    print k,v
                self.__xpathParser(docNode,config["data"])
            elif selector=="csquery":
                csdom=CsQuery.CQ.Create(html)
                #echo(csdom.Html())               
                self.__csqueryParser(csdom,config["data"])
            else:
                pass
        except Exception as err:
            tp,val,td = sys.exc_info()
            tracestr=traceback.format_exc()            
            output=[tracestr,str(tp),str(val),str(td)]
            errMsg="Raise Message:"+"；".join(output)
            echo(errMsg)
            if self.result.status==200:
                 self.result.status=700
            self.result.erronmassage=self.result.erronmassage+";"+errMsg
            self.result.errormassage=self.result.erronmassage
            #raise RuntimeError,errMsg
        finally:
            html=""
            self.__cacheControl=""
            self.__contentType=""
            self.__lastModified=""
            self.__responseText=""            

    def __csqueryParser(self,csdom,data):
        for i in range(len(data)):
            dic=data[i]
            name=dic["key"]
            paths=dic["path"]            
            print name, paths
            value=""
            if name=="content":
                pages=dic["pages"]
                cfgtype=dic["type"]
                if cfgtype=="text":
                    self.__csqueryContent(csdom,name,pages,paths)#
                elif cfgtype=="index":
                    self.__csqueryList(csdom,name,pages,paths)#
                else:
                    raise ValueError,("csquery type="+type+" do not support.")
            else:
                for index,item in enumerate(paths):
                    pth=item
                    lamda=None
                    if type(item)==tuple:
                        pth=item[0]                        
                        if len(item)==2:
                            lamda=item[1]

                    echo("path="+pth)
                    dom=csdom.Select(pth);
                    if dom.Length>0:
                        value=dom.Text()                         
                        if lamda:value=lamda(value)
                        self.getProperties(name,value)
                        self.result.article_properties[name]=value
                        echo("csquery name="+name+";value="+value) 
                        break 

    def __csqueryList(self,csdom,name,pages,paths):
        contents=[]
        for index,item in enumerate(paths):
            if type(item)==tuple:
                nodeText=[]               
                for i in range(0,len(item)):
                    path=item[i]
                    dom=csdom.Select(path)                    
                    if len(contents)>0 or dom.Length>0:
                        currentPath=item
                        contents.append(dom)
                    else:
                        break #第一个节点没有找到值就立刻抛弃
            elif type(item)==str:
                path=item
                dom=csdom.Select(path)
                currentPath=item
                if dom.Length>0:
                    contents.append(dom)                     
                    break
        #page info
        pagination=self.csqueryPagination(csdom,pages)
        if self.config.cfgContent.Options.PageNum==0:
            pagination=list(pagination)[0:]            
        elif self.config.cfgContent.Options.PageNum>0:
            pagination=list(pagination)[0:self.config.cfgContent.Options.PageNum-1]
        else:
            raise NameError,("self.config.cfgContent.Options.PageNum="+str(cfgContent.Options.PageNum)+", PageNum in [0-n]")
    
        for index,item in enumerate(pagination):
            echo("request:"+item)
            req=HttpRequest2()
            req.get(item)
            htm2=req.responseText.decode(self.__charset,"ignore")
            cshtm2=CsQuery.CQ.Create(htm2)            
            if type(currentPath)==tuple:
                for idx,path in enumerate(currentPath):
                    contents.append(cshtm2.Select(path))
            elif type(currentPath)==str:
                contents.append(cshtm2.Select(currentPath))
            html2=""
        
        results=[]
        csdompages=[]        
        for index,cspage in enumerate(contents): 
            cshyperblocks=cspage
            if type(self.config.cfgContent.Options.Excludes)==list and len(self.config.cfgContent.Options.Excludes)>0:
                RemoveDom(cshyperblocks,self.config.cfgContent.Options.Excludes)
            
            lamda=self.config.cfgContent.Options.Lamda
            if lamda:
                for idx,item in enumerate(cshyperblocks):
                    csblock=CsQuery.CQ.Create(item)
                    text=csblock.Text()
                    result=lamda(csblock,text)                    
                    if result and type(result)==str:
                        echo(text+";result="+result)
                        results.append(result)
                    elif result and type(result)==list:
                        for i,v in enumerate(result):
                            results.append(v)
            else:
                csdompages.append(cshyperblocks)        

        if len(results)==0:
            results=self.csqueryConents(contents)
        
        results=list(set(results))
        brtext="\r\n".join(results) 

        text="|".join(results) 
        self.result.content=text

    def __csqueryContent(self,csdom,name,pages,paths):
        contents=[]
        for index,item in  enumerate(paths):
            dom=csdom.Select(item)                        
            currentPath=item
            echo("item="+item+";currentPath="+currentPath)
            if dom.Length>0:     
                contents.append(dom) 
                break

        pagination=self.csqueryPagination(csdom,pages)
        for index,item in enumerate(pagination):
            req=HttpRequest2()
            req.get(item)
            h2=req.responseText.decode(self.__charset)
            csHtmldom=CsQuery.CQ.Create(h2)
            domPage=csHtmldom.Select(currentPath)            
            contents.append(domPage)

        for index,cspage in enumerate(contents):
            RemoveDom(cspage,["style","iframe","script","object","head"])
            if type(self.config.cfgContent.Options.Excludes)==list and len(self.config.cfgContent.Options.Excludes)>0:
                RemoveDom(cspage,self.config.cfgContent.Options.Excludes)                 
        
        cspages=self.csqueryConents(contents)
        if len(cspages)>0:
            self.lastCsdomp(cspages[len(cspages)-1])
            self.firstCsdomp(cspages[0])
        results=[]        
        for idx,cspage in enumerate(cspages):
            RemoveDom(cspage,["class"])            
            self.pageCsContentImage(cspage)
            t=[]
            for i,d in enumerate(cspage):
                st=d.InnerHTML
                t.append(st)
            #content=cspage.Html()
            content="".join(t)
            content=self.pageContentText(content)                        
            results.append(content)
        text="@@abcMSNPageMarkerabc@@".join(results) 
        echo(text)
        self.result.content=text
          
    def lastCsdomp(self,lastcsdompage):
        """处理最后一个段落p"""
        cscontainer=lastcsdompage
        count=cscontainer.Children("p").Length
        if count==0:
            cscontainer=lastcsdompage.Find("p").First().Parent()
        text=cscontainer.Children("p").Last().Text()
        hasEndSymbol=False
        for i in range(len(text)-1,-1,-1):
            if isEndSymbol(text[i]):
                hasEndSymbol=True
                text=text[0:i+1]
                echo(text)
                cscontainer.Children("p").Last().Text(text)
                break
        if hasEndSymbol==False:
            cscontainer.Children("p").Last().Remove()            
        return    

    def firstCsdomp(self,firstcsdompage):
        """从第一个段落p中提取摘要"""
        if self.result.article_properties["summary"]=="":
            #cspparent=firstcsdompage.Find("p").First().Parent()
            csps=firstcsdompage.Find("p")            
            for index,value in enumerate(csps):
                hasEndSymbol=False
                csp=CsQuery.CQ.Create(value)
                text=csp.Text().strip()
                text,number=re.subn('[\n\t]','',text)
                if text=="" or len(text)<5:
                    continue
                for i in range(0,len(text),1):
                    if isEndSymbol(text[i],["?","？","!","！","。"]):
                        hasEndSymbol=True
                        summary=text[0:i]+" ..."
                        self.result.article_properties["summary"]=summary
                        return
        return

    def pageContentText(self,content):
        """提供客户端处理text方法""" 
        try:
            content=RemoveText(content,['<!--[^>]*?-->','(?<=style=["\'])[^"\']+','(?<=onmouseover=["\'])[^"\']+'])
            content=self.defaultReplace(content)
            content=StringHelper.EscapeUnicode(content)     
            echo(content)
        except Exception as err:
            pass
        finally:
            return content

    def pageCsContentImage(self,cspage):
        """本地img替换为完全img路径"""
        proto, rest = urllib2.splittype(self.config.cfgUrl)  
        host, rest = urllib2.splithost(rest)
        csimgs=cspage.Find("img")        
        for idx,itm in enumerate(csimgs):   
            src=itm.Attributes["src"]
            base=FunctionHelper.urlSegments(self.config.cfgUrl)
            url=FunctionHelper.getUrl(base,src)
            itm.Attributes["src"]=url
        return
        
    #客户端方法
    def csqueryConents(self,csdompagination):
        return csdompagination 
        
    def csqueryPagination(self,csdom,pagesPath):
        pages=[]
        for index,item in enumerate(pagesPath):
            csquery=item
            cspage=csdom.Select(csquery)           
            if cspage:                
                children=cspage.Find("a")                
                if children.Length>0:
                    for i in range(0,children.Length):
                        cshyper=CsQuery.CQ.Create(children[i])              
                        href=cshyper.Attr("href")
                        text=cshyper.Text()
                        pagelamda=self.config.cfgContent.Options.PageLamda
                        if pagelamda:
                            str=pagelamda(cshyper,href,text)
                            if str:
                                href=str
                            else:
                                continue

                        if href and href[0:1]=="/":
                            proto, rest = urllib2.splittype(self.config.cfgUrl)  
                            host, rest = urllib2.splithost(rest)
                            href=proto+"://"+host+href
                        elif href and href[0:1]=="?":                            
                            proto, rest = urllib2.splittype(self.config.cfgUrl)  
                            host, rest = urllib2.splithost(rest)
                            p=rest.split("?")
                            p[1]=href[1:]
                            href=proto+"://"+host+"?".join(p)
                        elif href.find("http")==-1:
                            proto, rest = urllib2.splittype(self.config.cfgUrl)  
                            host, rest = urllib2.splithost(rest)
                            p_rest=rest.split("/")
                            p_rest[len(p_rest)-1]=href
                            href=proto+"://"+host+"/".join(p_rest)
                            
                        scale=self.config.cfgContent.Options.PageSimilarity          
                        rate=0.0
                        simlilar=StringHelper.LevenshteinDistance(self.__url,href,rate)
                        if href and simlilar[1]>scale and simlilar[1]<1:
                            pages.append(href) 
                                            
                if pages.Count>0:                    
                    func = lambda x,y:x if y in x else x + [y]
                    pages=reduce(func, [[], ] + pages)                                 
        return pages


   
    
