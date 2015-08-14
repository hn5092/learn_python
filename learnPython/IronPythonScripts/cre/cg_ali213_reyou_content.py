import sys
import unittest

from IronPythonScripts.modules.core.framework import PythonContentAnalyst, echo
from IronPythonScripts.modules.core.meta import FunctionHelper


sys.path.append("modules")

class ali213ReyouContentAnalyst(PythonContentAnalyst):

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
        return super(ali213ReyouContentAnalyst,self).csqueryPagination(csdom,pagesPaths)

    def csqueryConents(self,csdompagination):
        return super(ali213ReyouContentAnalyst,self).csqueryConents(csdompagination)

    def lastCsdomp(self,lastcsdompage):
        '''最后一个段落<p>'''
        return super(ali213ReyouContentAnalyst,self).lastCsdomp(lastcsdompage)

    def pageContentText(self,content):
        """分页的内容清理，默认清空注释、style、onmouseover，粗体替换，unicode编码转汉字"""
        return super(ali213ReyouContentAnalyst,self).pageContentText(content)

    def pageCsContentImage(self,cspage):
        """<img/>路径识别，默认支持/路径转换"""        
        super(ali213ReyouContentAnalyst,self).pageCsContentImage(cspage)          
        cspage.Find("#bigimg").Find("img").Wrap("<p></p>")
        cspage.Find("#smallimg").Find("img").Wrap("<p></p>")
        return

def getresult(url=''):   
    contentAnalyst=ali213ReyouContentAnalyst()
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
    source="热游:"+",".join(split[1:2])
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
        self.contentAnalyst=ali213ReyouContentAnalyst()
       
    def testConfig(self):
        result=getresult("http://m.ali213.net/android/102317.html")
        result=FunctionHelper.string2object(result)              
        pass

        
        result=getresult("http://m.ali213.net/ios/23881.html")
        result=FunctionHelper.string2object(result)
        self.assertGreater(result.article_properties["title"].find("混沌与秩序之英雄战歌"),-1)       
        self.assertGreater(result.article_properties["summary"].find("亲测可用啊"),-1)
        #self.assertGreater(result.article_properties["source"].find("ali213"),-1)         
        self.assertEqual(result.article_properties["issuedate"],"2015-04-28")
        self.assertGreater(result.content.find("混沌与秩序之英雄战歌截图"),-1)        
        pass
         
        result=getresult("http://m.ali213.net/wp/81752.html")
        result=FunctionHelper.string2object(result)
        self.assertGreater(result.article_properties["title"].find("脑波攻击"),-1)       
        self.assertGreater(result.article_properties["summary"].find("乐高的忠实fans应该会很开心"),-1)
        self.assertGreater(result.article_properties["source"].find("ali213"),-1)         
        self.assertEqual(result.article_properties["issuedate"],"2013-10-10")
        self.assertGreater(result.content.find("脑波攻击游戏截图"),-1)        
        pass

        result=getresult("http://m.ali213.net/android/109249.html")
        result=FunctionHelper.string2object(result)
        self.assertGreater(result.article_properties["title"].find("邪雨"),-1)       
        self.assertGreater(result.article_properties["summary"].find("有点无厘头"),-1)
        self.assertGreater(result.article_properties["source"].find("ali213"),-1)         
        self.assertEqual(result.article_properties["issuedate"],"2015-05-18")
        self.assertGreater(result.content.find("等待提示安装完成后即可到手机里游玩游戏"),-1)        
        pass
      

    


if __name__=="__main__":#sys.exit(0) 
    unittest.main()
    sys.exit(0)


