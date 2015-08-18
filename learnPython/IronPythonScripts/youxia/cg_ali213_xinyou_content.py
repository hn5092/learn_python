import sys
import unittest

from IronPythonScripts.build_result import echo, FunctionHelper
from IronPythonScripts.modules.core.framework import PythonContentAnalyst
from core.framework import *


sys.path.append("modules")
class ali213XinyouContentAnalyst(PythonContentAnalyst):

    def setConfig(self,url):
        self.config.cfgUrl=url
        self.config.cfgCharset=self.enum.Charset.utf8
        self.config.cfgSelector=self.enum.Selector.csquery
        self.config.cfgTitle=["h1.iphone_con_right_des_top_left_title"] 
        self.config.cfgAuthor=[] #("p.pleft > span:eq(1)",lambda x:x[3:])
        self.config.cfgSource=[("div.iphone_con_title",lambda x:getSource(x))]
        self.config.cfgIssuedate=[("div.iphone_con_right_des_top_left ul li:eq(4)",lambda x:getDate(x))]
        self.config.cfgSummary=["h2.iphone_con_right_des_bottom_con_con"]        
        self.config.cfgContent.Type=self.enum.ContentType.text
        self.config.cfgContent.Options.Excludes=["div.iphone_con_right_comment"]    
        self.config.cfgContent.Path=["div.iphone_con_right"]
        #self.config.cfgContent.Options.Lamda=lambda *x:x[1] #没用到 
        self.config.cfgContent.Pages=[] 
        self.config.cfgContent.Options.PageNum=0 #0=无限制 
        self.config.cfgContent.Options.PageLamda=lambda *x:x[1]
        self.config.cfgContent.Options.PageSimilarity=0.95 #相似度
        return self.config
    
   
    def csqueryPagination(self,csdom,pagesPaths):
        '''默认实现相似度计算，可识别路径/、？'''
        return super(ali213XinyouContentAnalyst,self).csqueryPagination(csdom,pagesPaths)

    def csqueryConents(self,csdompagination):
        return super(ali213XinyouContentAnalyst,self).csqueryConents(csdompagination)

    def lastCsdomp(self,lastcsdompage):
        '''最后一个段落<p>'''
        return super(ali213XinyouContentAnalyst,self).lastCsdomp(lastcsdompage)

    def pageContentText(self,content):
        """分页的内容清理，默认清空注释、style、onmouseover，粗体替换，unicode编码转汉字"""
        return super(ali213XinyouContentAnalyst,self).pageContentText(content)

    def pageCsContentImage(self,cspage):
        """<img/>路径识别，默认支持/路径转换"""        
        super(ali213XinyouContentAnalyst,self).pageCsContentImage(cspage)
        cspage.Find("#bigimg").Find("img").Wrap("<p></p>")
        cspage.Find("#smallimg").Find("img").Wrap("<p></p>")
        return

        

def getresult(url=''):   
    contentAnalyst=ali213XinyouContentAnalyst()
    contentAnalyst.execute(url);
    content=contentAnalyst.result.content
    title=contentAnalyst.result.article_properties["title"]
    source=contentAnalyst.result.article_properties["source"]
    contentAnalyst.result.article_properties["title"]=title+" [@@"+source+"]"
    echo(content)
    return contentAnalyst.result.toJsonString()

def getSource(str):
    str=str[str.find("位置")+3:]
    split=str.split(">")
    source="新游:"+",".join(split[1:2])
    return source

def getDate(str):
    start=str.find("日期")
    if(start>-1):
        str=str[start+3:start+3+10]
    return str

#getresult(URL)

####################### test case ######################
    
class auto163ContentAnalystTC(unittest.TestCase):
    def __init__(self, methodName = 'runTest'):
        super(auto163ContentAnalystTC, self).__init__(methodName)
        self.contentAnalyst=ali213XinyouContentAnalyst()
       
    def testConfig(self): 
        result=getresult("http://m.ali213.net/wp/43799.html")
        result=FunctionHelper.string2object(result)
        self.assertGreater(result.article_properties["title"].find("一起高尔夫2中文版"),-1)       
        self.assertGreater(result.article_properties["summary"].find("LetsGolf2:相信对于Ga"),-1)
        self.assertGreater(result.article_properties["source"].find("WP游戏下载"),-1)         
        self.assertEqual(result.article_properties["issuedate"],"2013-12-05")
        self.assertGreater(result.content.find("版截图"),-1)        
        pass

        result=getresult("http://m.ali213.net/wp/43389.html")
        result=FunctionHelper.string2object(result)
        self.assertGreater(result.article_properties["title"].find("枪火兄弟连"),-1)       
        self.assertGreater(result.article_properties["summary"].find("非常有大作风范哦"),-1)
        self.assertGreater(result.article_properties["source"].find("WP游戏下载"),-1)         
        self.assertEqual(result.article_properties["issuedate"],"2013-12-05")
        self.assertGreater(result.content.find("枪火兄弟连截图"),-1)        
        pass
      


if __name__=="__main__":#sys.exit(0) 
    unittest.main()
    sys.exit(0)

