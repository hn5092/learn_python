import sys
sys.path.append("modules")
from core.framework import *

class feelcarsContentAnalyst(PythonContentAnalyst):

    def setConfig(self,url):
        self.config.cfgUrl=url
        self.config.cfgCharset=self.enum.Charset.gb2312
        self.config.cfgSelector=self.enum.Selector.csquery
        self.config.cfgTitle=["div.article_text > div.article_text_title01","div.cs_lefttxt h2"]
        self.config.cfgAuthor=[("div.article_text > div.article_text_title02",lambda x:self.lambda_author(x)),("div.cs_lefttxt h5",lambda x:self.lambda_author(x))]
        self.config.cfgSource=["div.article_text > div.article_text_title02 > span:eq(2) > a","div.cs_lefttxt h5 a.media"]
        self.config.cfgSummary=[]
        self.config.cfgIssuedate=[("div.article_text > div.article_text_title02 > span:eq(0)",lambda x:self.lambda_date(x)),("div.cs_lefttxt h5",lambda x:self.lambda_date(x))]
        self.config.cfgContent.Type=self.enum.ContentType.text
        self.config.cfgContent.Options.Excludes=[]    
        self.config.cfgContent.Path=["div.article_text","div.cs_lefttxt"]
        #self.config.cfgContent.Options.Lamda=lambda *x:x[1] #没用到 
        self.config.cfgContent.Pages=["div.yahoo2"] 
        self.config.cfgContent.Options.PageNum=0 #0=限制 
        self.config.cfgContent.Options.PageLamda=lambda *x:x[1]
        self.config.cfgContent.Options.PageSimilarity=0.95 #相似度
        return self.config
    
    def lambda_date(self,value):
        start=value.find("时间：")+3
        value,number=re.subn('\s',' ',value)
        end=value.find(" ",start)
        if end==-1:
            date=value[start:]
        else:
            date=value[start:end]
        return date


    def lambda_author(self,value):
        value=value.strip()
        value,number=re.subn('\s',' ',value)
        start=value.find("作者")+3
        end=value.find(" ",start)
        if end==-1:
            author=value[value.find("作者")+3:]
        else:
            author=value[value.find("作者")+3:end]
        author=author.replace("&nbsp;","")
        return author

    def csqueryPagination(self,csdom,pagesPaths):
        '''默认实现相似度计算，可识别路径/、？'''
        return super(feelcarsContentAnalyst,self).csqueryPagination(csdom,pagesPaths)

    def csqueryConents(self,csdompagination):        
        results=[]
        for index,cspage in enumerate(csdompagination):            
            csbody=cspage            
            csbody.Find("p:eq(0)").PrevAll().Remove()  
            csbody.Find("div.yahoo2").NextAll().Remove()
            csbody.Find("div.yahoo2").Remove()                            
            csbody.Find("input").Remove() 
            csbody.Find("select").Remove()           
            results.append(csbody)
        return results

    def lastCsdomp(self,lastcsdompage):
        '''最后一个段落<p>'''
        return super(feelcarsContentAnalyst,self).lastCsdomp(lastcsdompage)

    def pageContentText(self,content):
        """分页的内容清理，默认清空注释、style、onmouseover，粗体替换，unicode编码转汉字"""
        return super(feelcarsContentAnalyst,self).pageContentText(content)

    def pageCsContentImage(self,cspage):
        """<img/>路径识别，默认支持/路径转换"""        
        return  super(feelcarsContentAnalyst,self).pageCsContentImage(cspage)

def getresult(url=''):   
    contentAnalyst=feelcarsContentAnalyst()
    contentAnalyst.execute(url);
    content=contentAnalyst.result.content
    echo(content)
    return contentAnalyst.result.toJsonString()

####################### test case ######################
    
class feelcarsTC(unittest.TestCase):
    def __init__(self, methodName = 'runTest'):
        super(feelcarsTC, self).__init__(methodName)
        self.contentAnalyst=feelcarsContentAnalyst()
       
    def testConfig(self):        
        result=getresult("http://www.feelcars.com/20140923/c201356612_1.shtml")
        result=FunctionHelper.string2object(result)
        self.assertGreater(result.article_properties["title"].find("呆萌小子! 汽车探索专业评测雪佛兰创酷"),-1  )
        self.assertEqual(result.article_properties["author"],"芦洪亚") 
        self.assertGreater(result.article_properties["summary"].find("创酷的内饰遵循了目前主流的简约而不简单的设计风格"),-1)
        self.assertEqual(result.article_properties["source"],"汽车探索")         
        self.assertEqual(result.article_properties["issuedate"],"2014年09月23日08:48")
        self.assertGreater(result.content.find("风口的开闭及方向，很有新意"),-1)
        pass

        result=getresult("http://www.feelcars.com/20140905/c201348845.shtml")
        result=FunctionHelper.string2object(result)
        self.assertGreater(result.article_properties["title"].find("奥迪公布新款A6全系官图 采用新LED大灯"),-1  )
        self.assertEqual(result.article_properties["author"],"Sofia") 
        self.assertGreater(result.article_properties["summary"].find("汽车探索讯】奥迪公布了新款A6/S6/RS6以及A6 allroad的"),-1)
        self.assertEqual(result.article_properties["source"],"汽车探索")         
        self.assertEqual(result.article_properties["issuedate"],"2014年09月05日08:00")
        self.assertGreater(result.content.find("S6/S6旅行版的最大"),-1)
        pass
        
        result=getresult("http://www.feelcars.com/20140916/c201353218.shtml")
        result=FunctionHelper.string2object(result)
        self.assertGreater(result.article_properties["title"].find("长安铃木启悦内饰官图发布！或11月上市"),-1  )
        self.assertEqual(result.article_properties["author"],"齐超") 
        self.assertGreater(result.article_properties["summary"].find("长安铃木再次发布了全新紧凑型车启悦的内饰官方图片"),-1)
        self.assertEqual(result.article_properties["source"],"汽车探索")         
        self.assertEqual(result.article_properties["issuedate"],"2014年09月16日11:41")
        self.assertGreater(result.content.find("该车还配备了轻量化高刚性的车体和低滚动阻力轮胎等组合"),-1)
        pass
    
        

if __name__=="__main__":#sys.exit(0) 
    unittest.main()
