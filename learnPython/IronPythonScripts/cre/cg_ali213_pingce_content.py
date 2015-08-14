import sys
import unittest

from IronPythonScripts.build_result import echo, FunctionHelper
from IronPythonScripts.modules.core.framework import PythonContentAnalyst


sys.path.append("modules")

class ali213PingceContentAnalyst(PythonContentAnalyst):

    def setConfig(self,url):
        self.config.cfgUrl=url
        self.config.cfgCharset=self.enum.Charset.utf8
        self.config.cfgSelector=self.enum.Selector.csquery
        self.config.cfgTitle=["h1"] 
        self.config.cfgAuthor=[] #("p.pleft > span:eq(1)",lambda x:x[3:])
        self.config.cfgSource=[("div.detail_mobile_title",lambda x:getSource(x))]
        self.config.cfgIssuedate=[("div.detail_mobile_left_center_time",lambda x:getDate(x))]
        self.config.cfgSummary=["h2.detail_mobile_left_center_daodu_con"]        
        self.config.cfgContent.Type=self.enum.ContentType.text
        self.config.cfgContent.Options.Excludes=["h1","div.detail_mobile_left_center_time","div.detail_mobile_left_center_daodu","div.detail_showpic","div.detail_tjtxt","div.detail_tjpic"]    
        self.config.cfgContent.Path=["div.detail_mobile_left_center"]
        #self.config.cfgContent.Options.Lamda=lambda *x:x[1] #没用到 
        self.config.cfgContent.Pages=["div.detail_mobile_page"] 
        self.config.cfgContent.Options.PageNum=0 #0=无限制 
        self.config.cfgContent.Options.PageLamda=lambda *x:x[1]
        self.config.cfgContent.Options.PageSimilarity=0.95 #相似度
        return self.config
    
   
    def csqueryPagination(self,csdom,pagesPaths):
        '''默认实现相似度计算，可识别路径/、？'''
        return super(ali213PingceContentAnalyst,self).csqueryPagination(csdom,pagesPaths)

    def csqueryConents(self,csdompagination):
        return super(ali213PingceContentAnalyst,self).csqueryConents(csdompagination)

    def lastCsdomp(self,lastcsdompage):
        '''最后一个段落<p>'''
        return super(ali213PingceContentAnalyst,self).lastCsdomp(lastcsdompage)

    def pageContentText(self,content):
        """分页的内容清理，默认清空注释、style、onmouseover，粗体替换，unicode编码转汉字"""
        return super(ali213PingceContentAnalyst,self).pageContentText(content)

    def pageCsContentImage(self,cspage):
        """<img/>路径识别，默认支持/路径转换"""  
        super(ali213PingceContentAnalyst,self).pageCsContentImage(cspage)
        csdiv=cspage.Find("div img")   
        if(csdiv.Length>0):
            cspage.Find("div img").Wrap("<p></p>")          
        return      
        

def getresult(url=''):   
    contentAnalyst=ali213PingceContentAnalyst()
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
        source="评测:"+",".join(split[1:2])
        return source
    

def getDate(str):
    start=str.find("时间")
    if(start>-1):
        str=str[start+3:start+3+19]
    return str

#getresult(URL)

####################### test case ######################
    
class auto163ContentAnalystTC(unittest.TestCase):
    def __init__(self, methodName = 'runTest'):
        super(auto163ContentAnalystTC, self).__init__(methodName)
        self.contentAnalyst=ali213PingceContentAnalyst()
       
    def testConfig(self): 
        result=getresult("http://m.ali213.net/news/150617/30275.html")
        result=FunctionHelper.string2object(result)
        self.assertGreater(result.article_properties["title"].find("全民爱主公"),-1)       
        self.assertGreater(result.article_properties["summary"].find("是拇指游玩2015年出品的一款全新三国题材手游"),-1)
        #self.assertGreater(result.article_properties["source"].find("ali213"),-1)         
        self.assertEqual(result.article_properties["issuedate"],"2015-06-17 16:04:30")
        self.assertGreater(result.content.find("就连人物表情也有十分细致的刻画"),-1)
        #self.assertGreater(result.article_properties["author"].find("费希"),-1) 
        pass


        result=getresult("http://m.ali213.net/news/141229/20089.html")
        result=FunctionHelper.string2object(result)
        self.assertGreater(result.article_properties["title"].find("团PVP火热来袭"),-1)       
        self.assertGreater(result.article_properties["summary"].find("量模型和特效支持下达到了大片级别"),-1)
        #self.assertGreater(result.article_properties["source"].find("ali213"),-1)         
        self.assertEqual(result.article_properties["issuedate"],"2014-12-29 10:59:48")
        self.assertGreater(result.content.find("一定会给玩家制造一个又一个的惊喜"),-1)
        #self.assertGreater(result.article_properties["author"].find("费希"),-1) 
        pass

        result=getresult("http://m.ali213.net/news/131203/3779.html")
        result=FunctionHelper.string2object(result)
        self.assertGreater(result.article_properties["title"].find("安卓版登场"),-1)       
        self.assertGreater(result.article_properties["summary"].find("安卓平台的玩家倒是可以去体验一番"),-1)
        #self.assertGreater(result.article_properties["source"].find("ali213"),-1)         
        self.assertEqual(result.article_properties["issuedate"],"2013-12-03 13:21:11")
        #self.assertGreater(result.content.find("就有点无缘相见的感觉了"),-1)
        #self.assertGreater(result.article_properties["author"].find("费希"),-1) 
        pass

        result=getresult("http://m.ali213.net/news/150515/27677.html")
        result=FunctionHelper.string2object(result)
        self.assertGreater(result.article_properties["title"].find("全平台攻势《太极熊猫》WP版本即将上线"),-1)       
        self.assertGreater(result.article_properties["summary"].find("近期上线Windows Phone商"),-1)
        #self.assertGreater(result.article_properties["source"].find("ali213"),-1)         
        self.assertEqual(result.article_properties["issuedate"],"2015-05-15 13:50:52")
        self.assertGreater(result.content.find("都可以畅享《太极熊猫》带来的乐趣"),-1)
        #self.assertGreater(result.article_properties["author"].find("费希"),-1) 
        pass
      
        result=getresult("http://m.ali213.net/news/150429/26623.html")
        result=FunctionHelper.string2object(result)
        self.assertGreater(result.article_properties["title"].find("SC收购WP渠道"),-1)       
        self.assertGreater(result.article_properties["summary"].find("同时借微疯客平台代理中国手游进行全球发行"),-1)
        #self.assertGreater(result.article_properties["source"].find("ali213"),-1)         
        self.assertEqual(result.article_properties["issuedate"],"2015-04-29 11:24:20")
        self.assertGreater(result.content.find("部分单品获得200万美元以上的月流水"),-1)
        #self.assertGreater(result.article_properties["author"].find("费希"),-1) 
        pass


if __name__=="__main__":#sys.exit(0) 
    unittest.main()
    sys.exit(0)


