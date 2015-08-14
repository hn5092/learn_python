import sys
sys.path.append("modules")
from core.framework import *

class XkbContentAnalyst(PythonContentAnalyst):

    def setConfig(self,url):
        self.config.cfgUrl=url
        self.config.cfgCharset=self.enum.Charset.utf8
        self.config.cfgSelector=self.enum.Selector.csquery
        self.config.cfgTitle=["div.conBox h1"]
        self.config.cfgAuthor=["div#ozoom > p:eq(0)"]
        self.config.cfgSource=[]
        self.config.cfgSummary=["div.conBox > div:eq(3)"]
        self.config.cfgIssuedate=[("div.time span.date",lambda x:x.replace("\r","").replace("\t","").replace("\n",""))]
        self.config.cfgContent.Type=self.enum.ContentType.text
        self.config.cfgContent.Options.Excludes=[]    
        self.config.cfgContent.Path=["div#ozoom > founder-content"]
        #self.config.cfgContent.Options.Lamda=lambda *x:x[1] #没用到 
        self.config.cfgContent.Pages=[] 
        self.config.cfgContent.Options.PageNum=0 #0=限制 
        self.config.cfgContent.Options.PageLamda=lambda *x:x[1]
        self.config.cfgContent.Options.PageSimilarity=0.95 #相似度
        return self.config
    
   
    def csqueryPagination(self,csdom,pagesPaths):
        '''默认实现相似度计算，可识别路径/、？'''
        return super(XkbContentAnalyst,self).csqueryPagination(csdom,pagesPaths)

    def csqueryConents(self,csdompagination):        
         return super(XkbContentAnalyst,self).csqueryConents(csdompagination)

    def lastCsdomp(self,lastcsdompage):
        '''最后一个段落<p>'''
        return super(XkbContentAnalyst,self).lastCsdomp(lastcsdompage)

    def pageContentText(self,content):
        """分页的内容清理，默认清空注释、style、onmouseover，粗体替换，unicode编码转汉字"""
        return super(XkbContentAnalyst,self).pageContentText(content)

    def pageCsContentImage(self,cspage):
        """<img/>路径识别，默认支持/路径转换"""        
        return  super(XkbContentAnalyst,self).pageCsContentImage(cspage)

def getresult(url=''):   
    contentAnalyst=XkbContentAnalyst()
    contentAnalyst.execute(url)
    contentAnalyst.result.article_properties["source"]="新快报"
    content=contentAnalyst.result.content
    echo(content)
    return contentAnalyst.result.toJsonString()

#getresult(URL)

####################### test case ######################
    
class XkbContentAnalystTC(unittest.TestCase):
    def __init__(self, methodName = 'runTest'):
        super(XkbContentAnalystTC, self).__init__(methodName)
        self.contentAnalyst=XkbContentAnalyst()
       
    def testConfig(self):
        result=getresult("http://www.ycwb.com/ePaper/xkb/html/2014-10/14/content_556628.htm?div=-1")
        result=FunctionHelper.string2object(result)
        content=result.content
        print content
        self.assertGreater(result.article_properties["title"].find("政府“聘用”子女养老实是变相购买公共服务"),-1  )
        self.assertEqual(result.article_properties["author"],"吴龙贵")        
        self.assertGreater(result.article_properties["issuedate"].find("星期二"),-1)
        self.assertGreater(result.article_properties["summary"].find("据报道，日前，记者从南京市民政局主办的2014年全市居家养老服务组织负责人培训班上获悉"),-1)
        self.assertGreater(result.content.find("从具体操作看，“家属照料型”"),-1)

        result=getresult("http://www.ycwb.com/ePaper/xkb/html/2014-10/14/content_556632.htm?div=-1")
        result=FunctionHelper.string2object(result)
        content=result.content
        print content
        self.assertGreater(result.article_properties["title"].find("全面“禁电”背后有多少民生考量"),-1  )
        self.assertEqual(result.article_properties["author"],"")        
        self.assertGreater(result.article_properties["issuedate"].find("星期二"),-1)        
        self.assertGreater(result.article_properties["summary"].find("据《新快报》报道，广州拟针对非机动车和摩托车做出"),-1)
        self.assertGreater(result.content.find("动自行车在法理层面存在的缺漏，早有论者论述。对于政府，法无授权不可为；对于市场，法无禁止即可为，这是最基本的道理。作为上位法的道路交通安全法并没有禁止电动自行车出行，地方岂能私设障碍"),-1)

        result=getresult("http://www.ycwb.com/ePaper/xkb/html/2014-10/14/content_556820.htm?div=-1")
        result=FunctionHelper.string2object(result)
        content=result.content
        print content
        self.assertGreater(result.article_properties["title"].find("“双十一”又要来了天猫今年大玩"),-1)
        self.assertEqual(result.article_properties["author"],"陈庆麟")        
        self.assertGreater(result.article_properties["issuedate"].find("星期二"),-1)
        self.assertGreater(result.article_properties["summary"].find("去年天猫“双十一”曾创造了单日成交额350亿元的惊人成绩"),-1)
        self.assertGreater(result.content.find("天猫手机客户端可以提"),-1)       
        

if __name__=="__main__":#sys.exit(0) 
    unittest.main()
