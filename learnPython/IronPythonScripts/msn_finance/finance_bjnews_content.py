import sys
sys.path.append("modules")
from core.framework import *

class BJNewsContentAnalyst(PythonContentAnalyst):

    def setConfig(self,url):
        self.config.cfgUrl=url
        self.config.cfgCharset=self.enum.Charset.utf8
        self.config.cfgSelector=self.enum.Selector.csquery
        self.config.cfgTitle=["div.rit h1"]
        self.config.cfgAuthor=[]
        self.config.cfgSource=[("div.rit dl.rdln dd",lambda x:x[x.find("星期")+4:])]
        self.config.cfgSummary=["div.rit p.fbiaot"]
        self.config.cfgIssuedate=[("div.rit dl.rdln dd",lambda x:x[0:x.find("星期")+3])]
        self.config.cfgContent.Type=self.enum.ContentType.text
        self.config.cfgContent.Options.Excludes=[]    
        self.config.cfgContent.Path=["div.rit"]
        #self.config.cfgContent.Options.Lamda=lambda *x:x[1] #没用到 
        self.config.cfgContent.Pages=[] 
        self.config.cfgContent.Options.PageNum=0 #0=限制 
        self.config.cfgContent.Options.PageLamda=lambda *x:x[1]
        self.config.cfgContent.Options.PageSimilarity=0.95 #相似度
        return self.config
    
   
    def csqueryPagination(self,csdom,pagesPaths):
        '''默认实现相似度计算，可识别路径/、？'''
        return super(BJNewsContentAnalyst,self).csqueryPagination(csdom,pagesPaths)

    def csqueryConents(self,csdompagination):        
        results=[]
        for index,cspage in enumerate(csdompagination):            
            csbody=cspage     
            #注释部分需要调整，否则丢失图片，例如：http://www.chinanews.com/yl/2014/09-12/6587254.shtml            
            csbody.Find("div.tpnr").PrevAll().Remove()
            csbody.Find("div.contnt").NextAll().Remove() 
            csbody.Find("p.ckgd").Remove() 
            csbody.Find("input").Remove()  
            results.append(csbody)
        return results 

    def lastCsdomp(self,lastcsdompage):
        '''最后一个段落<p>'''
        return super(BJNewsContentAnalyst,self).lastCsdomp(lastcsdompage)

    def pageContentText(self,content):
        """提供客户端处理text方法"""
        content=RemoveText(content,['(?<=style=["\'])[^"\']+','(?<=onmouseover=["\'])[^"\']+'])
        content=self.defaultReplace(content)
        content=StringHelper.EscapeUnicode(content) 
        return content

    def pageCsContentImage(self,cspage):
        """<img/>路径识别，默认支持/路径转换"""        
        return  super(BJNewsContentAnalyst,self).pageCsContentImage(cspage)

def getresult(url=''):   
    contentAnalyst=BJNewsContentAnalyst()
    contentAnalyst.execute(url);
    content=contentAnalyst.result.content
    echo(content)
    return contentAnalyst.result.toJsonString()

#getresult(URL)

####################### test case ######################
    
class BJNewsContentAnalystTC(unittest.TestCase):
    def __init__(self, methodName = 'runTest'):
        super(BJNewsContentAnalystTC, self).__init__(methodName)
        self.contentAnalyst=BJNewsContentAnalyst()
       
    def testConfig(self):        
        result=getresult("http://epaper.bjnews.com.cn/html/2014-10/14/content_540421.htm?div=-1")
        result=FunctionHelper.string2object(result)
        content=result.content
        print content
        self.assertGreater(result.article_properties["title"].find("11个督察组明察暗访政策落实"),-1  )
        self.assertEqual(result.article_properties["source"],"新京报")        
        self.assertEqual(result.article_properties["issuedate"],"2014年10月14日 星期二")
        self.assertGreater(result.article_properties["summary"].find("督察重点集中在民生领域"),-1)
        self.assertGreaterEqual(result.content.find("告制度，下级政府和有关部门要按规定时限报告重大决策部署的贯彻落实情况。同时，还将建立多元评"),-1)
        

        result=getresult("http://epaper.bjnews.com.cn/html/2014-10/11/content_539845.htm?div=-1")
        result=FunctionHelper.string2object(result)
        content=result.content
        print content
        self.assertGreater(result.article_properties["title"].find("纪念金正恩"),-1  )
        self.assertEqual(result.article_properties["source"],"新京报")        
        self.assertEqual(result.article_properties["issuedate"],"2014年10月11日 星期六")
        self.assertGreater(result.article_properties["summary"].find("出现，未拜谒锦绣山太阳宫"),-1)
        self.assertGreaterEqual(result.content.find("统一部发言人林丙哲当天在例行记者会上表示，此前朝鲜高层代表团访问韩国期间，金正恩通过政治局局长黄炳誓"),-1)
        
        result=getresult("http://epaper.bjnews.com.cn/html/2014-10/11/content_539756.htm?div=-1")
        result=FunctionHelper.string2object(result)
        content=result.content
        print content
        self.assertGreater(result.article_properties["title"].find("折利率难觅"),-1  )
        self.assertEqual(result.article_properties["source"],"新京报")        
        self.assertEqual(result.article_properties["issuedate"],"2014年10月11日 星期六")
        self.assertGreater(result.article_properties["summary"].find("多家银行执行“贷清不认房”，对7折利率均“没有细则"),-1)
        self.assertGreater(result.content.find("查数据显示，在中国城镇地区，68.9%的家庭拥有一套住房。这些家庭中，有19.7%既没有负债，同时也计划在未来五年购房。中国家庭金融调查与研究中心主任甘犁近日表示，央行房贷新政策在短期"),-1)
       
        

if __name__=="__main__":#sys.exit(0) 
    unittest.main()
