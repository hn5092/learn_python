import copy
import sys
import unittest, urllib2, json, re
from IronPythonScripts.modules.core import framework1_0
#<head>#
GrabberRequestInfo=framework1_0.GrabberRequestInfo
#<body>#
class IromPythonMeta(object):
    """example"""
    pass

class EnumCharset(object):
    """enum charset"""
    def __init__(self):
        self.gb2312="gb2312"
        self.utf8="utf-8"
        self.gbk="gbk"

class EnumContentType(object):
    """enum charset"""
    def __init__(self):
        self.text="text"
        self.index="index"        
 
class EnumSelector(object):
    """enum selector"""
    def __init__(self):
        self.xpath="xpath"
        self.csquery="csquery" 

class Enum(object):
    def __init__(self):
        self.Selector=EnumSelector()
        self.Charset=EnumCharset()
        self.ContentType=EnumContentType()


class ClientContentOptions(object):
    def __init__(self):
        self.__pageNum=0
        self.__pageSimilarity=0.95        
        self.__excludes=[]

        #lambda *x(csdoma,text):x[1]，分页链接元素
        self.__pageLamda=None 
        
        #lambda *csblock(csdoma,text):x[1] ，text配置没有实现 
        self.__lamda=None    

    @property
    def PageNum(self):
        """获得读取分页的数量,0=不限制 1-n=限定的页面数"""
        return self.__pageNum

    @PageNum.setter
    def PageNum(self,value):
        """设置获得分页数的数量->int"""
        if type(value)==int:
            self.__pageNum=value
        else:
            raise ValueError,("ReadNum","require <int> type")

    @property
    def PageSimilarity(self):
        """获取链接相似度,defalut=0.95"""
        return self.__pageSimilarity

    @PageSimilarity.setter
    def PageSimilarity(self,value):
        """设置分页链接相似度->float"""
        if type(value)==float:
            self.__pageSimilarity=value
        else:
            raise ValueError,("PageSimilarity","require <float> type")

    @property
    def Excludes(self):
        """获取csquery确定被排除的节点"""
        return self.__excludes

    @Excludes.setter
    def Excludes(self,value):
        """设置csquery选择被排除的节点->list"""
        if type(value)==list:
            self.__excludes=value
        else:
            raise ValueError,("Excludes","require <list> type")

    @property
    def PageLamda(self):
        """
        获取文本处理表达式，index为逐行处理
        lambda(csdoma,href,text) return href
        """
        return self.__pageLamda

    @PageLamda.setter
    def PageLamda(self,value):
        """
        设置文本处理表达式，index为逐行处理->lamda
        lambda(csdoma,href,text) return href
        """
        if type(value)==type(lambda x:x):
            self.__pageLamda=value
        elif value==None:
            pass
        else:
            raise ValueError,("PageLamda","require <lamda function> type")

    @property
    def Lamda(self):
        """text未实现，index为遍历超链block"""
        return self.__lamda

    @Lamda.setter
    def Lamda(self,value):
        """设置文本处理表达式，index为逐行处理->lamda"""
        if type(value)==type(lambda x:x):
            self.__lamda=value
        elif value==None:
            pass
        else:
            raise ValueError,("Lamda","require <lamda function> type")

    def Resolve(self):
        """将字段解析为字典"""
        options={
            "pagenum":self.PageNum            
            ,"pagelamda":self.PageLamda
            ,"pagesimilarity":self.PageSimilarity 
            ,"lamda":self.Lamda
            ,"excludes":self.Excludes           
            }
        return options


class ClientContentConfig(object):    
    def __init__(self):
        self.__pages=[]
        self.__path=[]
        self.__type="text"
        self.__options=ClientContentOptions()       

    @property
    def Pages(self):
        """获取分页标识块"""
        return self.__pages

    @Pages.setter
    def Pages(self,value):
        """设置分页标识块->list"""
        if type(value)==list:
            self.__pages=value
        else:
            raise ValueError,("Page","require <list> type")

    @property
    def Path(self):
        """获取内容块的路径"""
        return self.__path

    @Path.setter
    def Path(self,value):
        """设置内容块路径->list"""
        if type(value)==list:
            self.__path=value
        else:
            raise ValueError,("Path","require <list> type")

    @property
    def Type(self):
        """get type"""
        return self.__type

    @Type.setter
    def Type(self,value):
        """set value->EnumContentType"""
        if type(value)==str:
            self.__type=value
        else:
            raise ValueError,("Type","require <EnumContentType> type")

    @property
    def Options(self):
        """get type"""
        return self.__options

    @Options.setter
    def Options(self,value):
        """set value->dic"""
        if type(value)==dict:
            self.__options=value
        else:
            raise ValueError,("Options","require <ClientContentOptions> type")

class ClientConfig(object):
    """
    config infomation
    """
    def __init__(self):
        self.__url=""
        self.__charset="utf-8"
        self.__selector="xpath"        
        self.__data=copy.deepcopy(GrabberRequestInfo().article_properties)
        for (k,v) in  self.__data.items(): 
            self.__data[k]=[]              
        self.__content=ClientContentConfig()
    
    @property
    def cfgUrl(self): 
        """get url"""        
        return self.__url

    @cfgUrl.setter
    def cfgUrl(self,value):
        '''set value:str'''
        if type(value)==str:
            self.__url=value
        else:
            raise ValueError,("Url","require <str> type")

    
    @property
    def cfgCharset(self):
        """get charset"""
        return self.__charset

    @cfgCharset.setter
    def cfgCharset(self,value):
        """set value: Enum.Charset"""
        if type(value)==str:
            self.__charset=value
        else:
            raise ValueError,("Charset","require <Enum.Charset> type")

    
    @property
    def cfgSelector(self):
        """get selector"""
        return self.__selector

    @cfgSelector.setter
    def cfgSelector(self,value):
        """set value: Enum.Selector"""
        if type(value)==str:
            self.__selector=value
        else:
            raise ValueError,("Selector","require <Enum.Selector> type")

   
    @property
    def cfgTitle(self): 
        """get title"""
        return self.__data["title"]

    @cfgTitle.setter
    def cfgTitle(self,value):
        """set value->list"""
        if type(value)==list:
            self.__data["title"]=value
        else:
            raise ValueError,("Title","require <list> type")
    
    @property
    def cfgAuthor(self):
        """get author"""
        return self.__data["author"]

    @cfgAuthor.setter
    def cfgAuthor(self,value):
        """set value->list"""
        if type(value)==list:
            self.__data["author"]=value
        else:
            raise ValueError,("Author","require <list> type")

    
    @property
    def cfgSource(self):
        """get source"""
        return self.__data["source"]

    @cfgSource.setter
    def cfgSource(self,value):
        """set value->list"""
        if type(value)==list:
            self.__data["source"]=value
        else:
            raise ValueError,("Source","require <list> type")

    
    @property
    def cfgSummary(self):
        """get summary"""
        return self.__data["summary"]

    @cfgSummary.setter
    def cfgSummary(self,value):
        """set value->list"""
        if type(value)==list:
            self.__data["summary"]=value
        else:
            raise ValueError,("Summary","require <list> type")
    
    @property
    def cfgIssuedate(self):
        """get issuedate"""
        return self.__data["issuedate"]

    @cfgIssuedate.setter
    def cfgIssuedate(self,value):
        """get value->list"""
        if type(value)==list:
            self.__data["issuedate"]=value
        else:
            raise ValueError,("Issuedate","require <list> type")
      
    @property
    def cfgContent(self):
        """get content"""
        return self.__content
    
    def Resolve(self):   
        '''convert object to dict'''     
        return {"url":self.__url
        ,"charset":self.__charset
        ,"selector":self.__selector
        ,"data":[{"key":"title","path":self.__data["title"]}
    ,{"key":"author","path":self.__data["author"]}
    ,{"key":"source","path":self.__data["source"]}
    ,{"key":"summary","path":self.__data["summary"]}
    ,{"key":"issuedate","path":self.__data["issuedate"]}
    ,{"key":"content"
      ,"type":self.cfgContent.Type
      ,"pages":self.cfgContent.Pages
      ,"path":self.cfgContent.Path
      ,"options":self.cfgContent.Options.Resolve()
      }
    ]}

class FunctionHelper(object):
    @staticmethod
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

    @staticmethod
    def getUrl(base,path):
        segments=copy.deepcopy(base)      
        if path.startswith("http"):
            return path
        elif path.startswith("/"):
            path=path.strip("/")
            segments["path"][1]=[path]
            segments["query"]=""
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
        return url

    @staticmethod
    def string2object(resultStr):
        jsondic=json.loads(resultStr)
        result=GrabberRequestInfo()
        result.article_properties=jsondic["article_properties"]
        result.content=jsondic["content"]
        return result
 
#<test>#       
if __name__=="__main__":

    pageLamda=lambda *x:x[0] #(csdoma,href,text)
    Lamda=lambda *x:x[1] #(csdoma,href,text)
    print "sss"
    class TC(unittest.TestCase):
        def __init__(self, methodName = 'runTest'):
            super(TC, self).__init__(methodName)
            self.config=ClientConfig()
       
        def testConfig(self):
            full="http://www.sohu.com/auto/2014/10-21/xyz.html?v=123"
            base=FunctionHelper.urlSegments(full)

            cur="/auto/pic.img"            
            url=FunctionHelper.getUrl(base,cur)
            self.assertEqual(url,"http://www.sohu.com/auto/pic.img")

            cur="auto/pic.img"
            url=FunctionHelper.getUrl(base,cur)
            self.assertEqual(url,"http://www.sohu.com/auto/2014/10-21/auto/pic.img")

    unittest.main()
    
    



