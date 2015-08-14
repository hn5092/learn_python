import sys
sys.path.append("modules")
from core.framework import *

#京华时报
class JinghuaContentAnalyst(PythonContentAnalyst):

    def setConfig(self,url):
        self.config.cfgUrl=url
        self.config.cfgCharset=self.enum.Charset.utf8
        self.config.cfgSelector=self.enum.Selector.csquery
        self.config.cfgTitle=["div#content_header h1"]
        self.config.cfgAuthor=[]
        self.config.cfgSource=["ul#title_di li.time:eq(1) a"]
        self.config.cfgSummary=[]
        self.config.cfgIssuedate=["ul#title_di li.time:eq(0)"]
        self.config.cfgContent.Type=self.enum.ContentType.text
        self.config.cfgContent.Options.Excludes=[]    
        self.config.cfgContent.Path=["div#container"]
        #self.config.cfgContent.Options.Lamda=lambda *x:x[1] #没用到 
        self.config.cfgContent.Pages=[] 
        self.config.cfgContent.Options.PageNum=0 #0=限制 
        self.config.cfgContent.Options.PageLamda=lambda *x:x[1]
        self.config.cfgContent.Options.PageSimilarity=0.95 #相似度
        return self.config
    
   
    def csqueryPagination(self,csdom,pagesPaths):
        '''默认实现相似度计算，可识别路径/、？'''
        return super(JinghuaContentAnalyst,self).csqueryPagination(csdom,pagesPaths)

    def csqueryConents(self,csdompagination):        
        results=[]
        for index,cspage in enumerate(csdompagination):            
            csbody=cspage
            csbody.Find("dl:eq(0)").PrevAll().Remove()
            csbody.Find("p:last").NextAll().Remove()            
            csbody.Find("input").Remove()  
            results.append(csbody)
        return results 

    def lastCsdomp(self,lastcsdompage):
        '''最后一个段落<p>'''
        return super(JinghuaContentAnalyst,self).lastCsdomp(lastcsdompage)

    def pageContentText(self,content):
        """分页的内容清理，默认清空注释、style、onmouseover，粗体替换，unicode编码转汉字"""
        return super(JinghuaContentAnalyst,self).pageContentText(content)

    def pageCsContentImage(self,cspage):
        """<img/>路径识别，默认支持/路径转换"""        
        return  super(JinghuaContentAnalyst,self).pageCsContentImage(cspage)

def getresult(url=''):   
    contentAnalyst=JinghuaContentAnalyst()
    contentAnalyst.execute(url);
    content=contentAnalyst.result.content
    echo(content)
    return contentAnalyst.result.toJsonString()

#getresult(URL)

####################### test case ######################
    
class JinghuaContentAnalystTC(unittest.TestCase):
    def __init__(self, methodName = 'runTest'):
        super(JinghuaContentAnalystTC, self).__init__(methodName)
        self.contentAnalyst=JinghuaContentAnalyst()
       
    def testConfig(self):        
        result=getresult("http://epaper.jinghua.cn/html/2014-10/23/content_136457.htm")
        result=FunctionHelper.string2object(result)
        content=result.content
        print result.article_properties["author"]
        self.assertGreater(result.article_properties["title"].find("新浪网总编辑陈彤离职"),-1  )
        self.assertGreater(result.article_properties["source"].find("京华时报"),-1)        
        self.assertEqual(result.article_properties["issuedate"],"2014年10月23日")        
        self.assertGreater(result.content.find("大佬离职潮起。国内知名门户网站新浪网总编辑陈彤"),-1)
        self.assertGreater(result.content.find('<img src="http://epaper.jinghua.cn/images/2014-10/23/034/p2E_b.jpg">'),-1)
        pass        

        result=getresult("http://epaper.jinghua.cn/html/2014-10/11/content_133588.htm")
        result=FunctionHelper.string2object(result)
        content=result.content
        print content
        self.assertGreater(result.article_properties["title"].find("故宫清门户"),-1  )
        self.assertGreater(result.article_properties["source"].find("京华时报"),-1)        
        self.assertEqual(result.article_properties["issuedate"],"2014年10月11日")        
        self.assertGreater(result.content.find("故宫餐厅”牌匾撤"),-1)
        pass        
        

if __name__=="__main__":#sys.exit(0) 
    unittest.main()
