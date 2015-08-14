#coding=utf-8
from CSHelper import StringHelper
import CsQuery
import sys
import time
import unittest
import urllib

from IronPythonScripts.build_result import FunctionHelper, PythonContentAnalyst, \
    echo


sys.path.append("modules")

class ali213NewsContentAnalyst(PythonContentAnalyst):

    def setConfig(self,url):
        self.config.cfgUrl=url
        self.config.cfgCharset=self.enum.Charset.utf8
        self.config.cfgSelector=self.enum.Selector.csquery
        self.config.cfgTitle=["h1"] 
        self.config.cfgAuthor=[] #("p.pleft > span:eq(1)",lambda x:x[3:])
        self.config.cfgSource=[("meta",lambda x:self.getSource(x))]
        self.config.cfgIssuedate=[("meta",lambda x:self.getDate(x))]
        self.config.cfgSummary=["p:eq(0)"]        
        self.config.cfgContent.Type=self.enum.ContentType.text
        self.config.cfgContent.Options.Excludes=["div.common-3g-bottom"]    
        self.config.cfgContent.Path=["div.detail_content p","div.content","div.content p"]
        #self.config.cfgContent.Options.Lamda=lambda *x:x[1] #没用到 
        self.config.cfgContent.Pages=[] 
        self.config.cfgContent.Options.PageNum=0 #0=无限制 
        self.config.cfgContent.Options.PageLamda=lambda *x:x[1]
        self.config.cfgContent.Options.PageSimilarity=0.95 #相似度
        return self.config
    
   
    def csqueryPagination(self,csdom,pagesPaths):
        '''默认实现相似度计算，可识别路径/、？'''
        return super(ali213NewsContentAnalyst,self).csqueryPagination(csdom,pagesPaths)

    def csqueryConents(self,csdompagination):
        return super(ali213NewsContentAnalyst,self).csqueryConents(csdompagination)

    def lastCsdomp(self,lastcsdompage):
        '''最后一个段落<p>'''
        return super(ali213NewsContentAnalyst,self).lastCsdomp(lastcsdompage)

    def pageContentText(self,content):
        """分页的内容清理，默认清空注释、style、onmouseover，粗体替换，unicode编码转汉字"""
        return super(ali213NewsContentAnalyst,self).pageContentText(content)

    def pageCsContentImage(self,cspage):
        """<img/>路径识别，默认支持/路径转换"""    
        cspage.Find("img").Wrap("<p></p>")  
        return  super(ali213NewsContentAnalyst,self).pageCsContentImage(cspage)


    def getDate(self,str):
        url=self.config.cfgUrl
        str=url[url.find('=')+1:url.find('&')]
        return str

    def getSource(self,str):
        url=self.config.cfgUrl
        name=url[url.rfind('=')+1:]
        name=name.decode('utf8')
        type=url[url.find('t=')+2:url.rfind('&')]        
        return "攻略:"+name+"["+type+"]"

def getresult(url=''):   
    contentAnalyst=ali213NewsContentAnalyst()
    contentAnalyst.execute(url);
    content=contentAnalyst.result.content
    title=contentAnalyst.result.article_properties["title"]
    source=contentAnalyst.result.article_properties["source"]
    contentAnalyst.result.article_properties["title"]=title+" [@@攻略:"+source.replace("攻略:","")+"]"
    echo(content)
    cscontent=CsQuery.CQ.Create("<div>"+content+"</div>")
    cselem=cscontent.Children()
    group=[]
    groups=[]
    for idx,item in enumerate(cselem):
        nodename=item.NodeName
        if nodename=="P" or nodename=="DIV":
            csitem=CsQuery.CQ.Create(item)
            text=csitem.Text()
            html=csitem.Html()
            if csitem.Find("img").Length>0:               
                group.append(html)               
            elif len(text)>0:                                   
                group.append("<p>"+html+"</p>")
            else:
                groupstr="".join(group)
                groups.append(groupstr)
                group=[]
        else:
            continue
    if len(group)>0:
        str="".join(group)
        groups.append(str)

    text="@@abcMSNPageMarkerabc@@".join(groups) 
    text=StringHelper.EscapeUnicode(text)
    contentAnalyst.result.content=text
    return contentAnalyst.result.toJsonString()

def getAuthor(str): 
    return ""
    

def getSource(str):
    str=str.split('_')
    if(len(str)>1):
        str=str[1][0:str.find('-')-1]
        return str[1]
    else:
        str=str[0][0:str[0].find(' ')]
        return str



#getresult(URL)

####################### test case ######################
    
class auto163ContentAnalystTC(unittest.TestCase):
    def __init__(self, methodName = 'runTest'):
        super(auto163ContentAnalystTC, self).__init__(methodName)
        self.contentAnalyst=ali213NewsContentAnalyst()
       
    def testConfig(self):
        result=getresult("http://3g.ali213.net/gl/m/169769.html?d=2015-06-02&t=new&n=??-%C3%A8??%C3%A8??%C3%A9??3D")
        result=FunctionHelper.string2object(result)  
        print result           
        pass 

        name=u"命运之神".encode('utf8')        
        result=getresult("http://3g.ali213.net/gl/m/48312.html?d=2014-09-09&t=new&n="+name)
        result=FunctionHelper.string2object(result)
        self.assertGreater(result.article_properties["title"].find("《命运之神》副本怎么玩"),-1)       
        self.assertGreater(result.article_properties["summary"].find("啥名次也木有、各种蛋疼"),-1)
        self.assertGreater(result.article_properties["source"].find("命运之神"),-1)         
        self.assertEqual(result.article_properties["issuedate"],"2014-09-09")
        self.assertGreater(result.content.find("浪费那么多体力去换那点经验级"),-1)        
        pass

        name=u"绝地战警".encode('utf8')        
        result=getresult("http://3g.ali213.net/gl/m/114223.html?d=2014-09-11&t=hot&n="+name)
        result=FunctionHelper.string2object(result)
        self.assertGreater(result.article_properties["title"].find("绝地战警修改攻略"),-1)       
        self.assertGreater(result.article_properties["summary"].find("玩家只要仔细看完攻略"),-1)
        self.assertGreater(result.article_properties["source"].find("绝地战警"),-1)         
        self.assertEqual(result.article_properties["issuedate"],"2014-09-11")
        self.assertGreater(result.content.find("花一点钱或者进入一点钱就能正常显示了"),-1)        
        pass 

if __name__=="__main__":#sys.exit(0) 
    unittest.main()
    sys.exit(0)

