import sys
sys.path.append("modules")
from core.framework import *

class cbh21ContentAnalyst(PythonContentAnalyst):

    def setConfig(self,url):
        self.config.cfgUrl=url
        self.config.cfgCharset=self.enum.Charset.utf8
        self.config.cfgSelector=self.enum.Selector.csquery
        self.config.cfgTitle=["div.news_content h1:eq(1)"]
        self.config.cfgAuthor=["div.news_content div.news_author"]
        self.config.cfgSource=[]
        self.config.cfgSummary=[]
        self.config.cfgIssuedate=[("div.data",lambda x:x[0:x.find("日")+1].strip())]
        self.config.cfgContent.Type=self.enum.ContentType.text
        self.config.cfgContent.Options.Excludes=[]    
        self.config.cfgContent.Path=["div.news_content"]        
        self.config.cfgContent.Pages=[] 
        self.config.cfgContent.Options.PageNum=0 #0=限制 
        self.config.cfgContent.Options.PageLamda=lambda *x:x[1]
        self.config.cfgContent.Options.PageSimilarity=0.95 #相似度
        return self.config
    
   
    def csqueryPagination(self,csdom,pagesPaths):
        '''默认实现相似度计算，可识别路径/、？'''
        return super(cbh21ContentAnalyst,self).csqueryPagination(csdom,pagesPaths)

    def csqueryConents(self,csdompagination):        
        results=[]
        for index,cspage in enumerate(csdompagination):            
            csbody=cspage            
            csbody.Find("div.news_photo").PrevAll().Remove()
            csbody.Find("div.news_text").NextAll().Remove()                                  
            csbody.Find("input").Remove()  
            results.append(csbody)
        return results

    def lastCsdomp(self,lastcsdompage):
        '''最后一个段落<p>'''
        return super(cbh21ContentAnalyst,self).lastCsdomp(lastcsdompage)

    def pageContentText(self,content):
        """分页的内容清理，默认清空注释、style、onmouseover，粗体替换，unicode编码转汉字"""
        return super(cbh21ContentAnalyst,self).pageContentText(content)

    def pageCsContentImage(self,cspage):
        """<img/>路径识别，默认支持/路径转换"""        
        return  super(cbh21ContentAnalyst,self).pageCsContentImage(cspage)

def getresult(url=''):   
    contentAnalyst=cbh21ContentAnalyst()
    contentAnalyst.execute(url);
    content=contentAnalyst.result.content
    contentAnalyst.result.article_properties["source"]="21世纪经济报道"
    echo(content)
    print contentAnalyst.result.errormassage    
    return contentAnalyst.result.toJsonString()

#getresult(URL)

####################### test case ######################
    
class cbh21ContentAnalystTC(unittest.TestCase):
    def __init__(self, methodName = 'runTest'):
        super(cbh21ContentAnalystTC, self).__init__(methodName)
        self.contentAnalyst=cbh21ContentAnalyst()
       
    def testConfig(self):
        result=getresult("http://epaper.21cbh.com/html/2014-10/21/content_113828.htm?div=-1")
        result=FunctionHelper.string2object(result)
        self.assertGreater(result.article_properties["title"].find("十八届四中全会召开 专题研究全面推进依法治国"),-1  )
        self.assertEqual(result.article_properties["author"],"") 
        self.assertGreater(result.article_properties["summary"].find("根据中共中央政治局会议的决定"),-1)
        self.assertEqual(result.article_properties["source"],"21世纪经济报道")         
        self.assertEqual(result.article_properties["issuedate"],"2014年10月21日")
        self.assertGreater(result.content.find("展和改革中一件划时代的大事"),-1)
        
               
        result=getresult("http://epaper.21cbh.com/html/2014-10/20/content_113685.htm?div=-1")
        result=FunctionHelper.string2object(result)
        self.assertGreater(result.article_properties["title"].find("111款QDII月平均下跌5.03% 大宗商品投向最受伤"),-1  )
        self.assertEqual(result.article_properties["author"],"") 
        self.assertGreater(result.article_properties["summary"].find("受外围股市大跌影响，10月17日，上证指数开盘后一路向下俯冲，上午最大跌幅达到1.81%"),-1)
        self.assertEqual(result.article_properties["source"],"21世纪经济报道")         
        self.assertEqual(result.article_properties["issuedate"],"2014年10月20日")
        self.assertGreater(result.content.find("至于房地产方向的QDII，蒋锴认为投向房地产信托投资基金(REITs)的产品更值得关注"),-1)
                     
        result=getresult("http://epaper.21cbh.com/html/2014-09/22/content_111759.htm?div=-1")
        result=FunctionHelper.string2object(result)
        self.assertGreater(result.article_properties["title"].find("资讯"),-1  )
        self.assertEqual(result.article_properties["author"],"") 
        self.assertGreater(result.article_properties["summary"].find("美国纽约麦迪逊大道690-691号店"),-1)        
        self.assertEqual(result.article_properties["source"],"21世纪经济报道")       
        self.assertEqual(result.article_properties["issuedate"],"2014年09月22日")
        self.assertGreater(result.content.find("格纹再到经典的"),-1)
        

if __name__=="__main__":#sys.exit(0) 
    unittest.main()
