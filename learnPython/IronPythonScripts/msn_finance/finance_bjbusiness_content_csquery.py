import sys
sys.path.append("modules")
from core.framework import *

#北京商报
class BjbusinessContentAnalyst(PythonContentAnalyst):

    def setConfig(self,url):
        self.config.cfgUrl=url
        self.config.cfgCharset=self.enum.Charset.utf8
        self.config.cfgSelector=self.enum.Selector.csquery
        self.config.cfgTitle=["table#bmdhdw table strong"]
        self.config.cfgAuthor=["table#bmdhdw > tbody > tr > td:eq(1) > table:eq(2) span:eq(2)"]
        self.config.cfgSource=[]
        self.config.cfgSummary=[]
        self.config.cfgIssuedate=["td.daohang:eq(1)"]
        self.config.cfgContent.Type=self.enum.ContentType.text
        self.config.cfgContent.Options.Excludes=["a.preart","input"]    
        self.config.cfgContent.Path=["table#bmdhdw > tbody tr:eq(0) > td:eq(1) > table:eq(3)"]
        #self.config.cfgContent.Options.Lamda=lambda *x:x[1] #没用到 
        self.config.cfgContent.Pages=[] 
        self.config.cfgContent.Options.PageNum=0 #0=限制 
        self.config.cfgContent.Options.PageLamda=lambda *x:x[1]
        self.config.cfgContent.Options.PageSimilarity=0.95 #相似度
        return self.config
    
   
    def csqueryPagination(self,csdom,pagesPaths):
        '''默认实现相似度计算，可识别路径/、？'''
        return super(BjbusinessContentAnalyst,self).csqueryPagination(csdom,pagesPaths)

    def csqueryConents(self,csdompagination):        
         return super(BjbusinessContentAnalyst,self).csqueryConents(csdompagination)

    def lastCsdomp(self,lastcsdompage):
        '''最后一个段落<p>'''
        return super(BjbusinessContentAnalyst,self).lastCsdomp(lastcsdompage)

    def pageContentText(self,content):
        """分页的内容清理，默认清空注释、style、onmouseover，粗体替换，unicode编码转汉字"""
        content=RemoveText(content,['(?<=width)=["\'][^"\']+','(?<=bgcolor=["\'])[^"\']+','(?<=align=["\'])[^"\']+'])
        return super(BjbusinessContentAnalyst,self).pageContentText(content)

    def pageCsContentImage(self,cspage):
        """<img/>路径识别，默认支持/路径转换"""        
        return  super(BjbusinessContentAnalyst,self).pageCsContentImage(cspage)

def getresult(url=''):   
    contentAnalyst=BjbusinessContentAnalyst()
    contentAnalyst.execute(url)
    contentAnalyst.result.content='<table border="0px" cellpadding="0px" cellspacing="0px" width="100%">'+contentAnalyst.result.content+"</table>"
    content=contentAnalyst.result.content
    echo(content)
    contentAnalyst.result.article_properties["source"]="北京商报"
    return contentAnalyst.result.toJsonString()

#getresult(URL)

####################### test case ######################
    
class BjbusinessContentAnalystTC(unittest.TestCase):
    def __init__(self, methodName = 'runTest'):
        super(BjbusinessContentAnalystTC, self).__init__(methodName)
        self.contentAnalyst=BjbusinessContentAnalyst()
       
    def testConfig(self):
        
        result=getresult("http://www.bbtonline.com.cn/site1/bjsb/html/2014-09/29/content_271847.htm?div=0")
        result=FunctionHelper.string2object(result)
        content=result.content
        print content
        pass

        result=getresult("http://www.bbtonline.com.cn/site1/bjsb/html/2014-09/29/content_271923.htm?div=-1")
        result=FunctionHelper.string2object(result)
        content=result.content
        print content
        self.assertGreater(result.article_properties["title"].find("交易港股真得谨慎"),-1  )
        self.assertGreater(result.article_properties["author"].find("周科竞"),-1)        
        self.assertEqual(result.article_properties["issuedate"],"2014年09月29日") 
        self.assertEqual(result.article_properties["source"],"北京商报")        
        self.assertGreater(result.content.find("议投资者，在投资港股"),-1)
        pass

        result=getresult("http://www.bbtonline.com.cn/site1/bjsb/html/2014-09/29/content_271956.htm?div=-1")
        result=FunctionHelper.string2object(result)
        content=result.content
        print content
        self.assertGreater(result.article_properties["title"].find("盐业高铁领衔自贸区最强改革"),-1  )
        #self.assertGreater(result.article_properties["author"].find("北京商报"),-1)        
        self.assertEqual(result.article_properties["issuedate"],"2014年09月29日") 
        self.assertEqual(result.article_properties["source"],"北京商报")        
        self.assertGreater(result.content.find("过去管制过多、计划过多的现象，真正回归市场经济的本源"),-1)
        pass

        result=getresult("http://www.bbtonline.com.cn/site1/bjsb/html/2014-09/29/content_271955.htm?div=0")
        result=FunctionHelper.string2object(result)
        content=result.content
        print content
        self.assertGreater(result.article_properties["title"].find("连锁酒店巨头抵制OTA返现"),-1  )
        self.assertEqual(result.article_properties["author"],"")        
        self.assertEqual(result.article_properties["issuedate"],"2014年09月29日") 
        self.assertEqual(result.article_properties["source"],"北京商报")        
        self.assertGreater(result.content.find("OTA的佣金通常在15%左右，即45元。OTA以45元或更多作为预订酒店后的“返现”，将返还的现金打入OTA"),-1)
        pass        

    

if __name__=="__main__":#sys.exit(0) 
    unittest.main()
