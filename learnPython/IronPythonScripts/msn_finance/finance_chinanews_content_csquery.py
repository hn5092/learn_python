import unittest
import sys
sys.path.append("modules")
from core.framework import *

class ChinanewsContentAnalyst(PythonContentAnalyst):

    def setConfig(self,url):
        self.config.cfgUrl=url
        self.config.cfgCharset=""
        self.config.cfgSelector=self.enum.Selector.csquery
        self.config.cfgTitle=[("div#cont_1_1_2 > h1",lambda x:x.strip())]
        self.config.cfgAuthor=[]
        self.config.cfgSource=[("div#cont_1_1_2 div.left-t",lambda x:x[x.find("来源")+3:x.find("参与互动")-1])]
        self.config.cfgSummary=["div.left_pt"]
        self.config.cfgIssuedate=[("div#cont_1_1_2 div.left-t",lambda x:x[0:x.find("来源")-1])]
        self.config.cfgContent.Pages=[""]
        self.config.cfgContent.Path=["div#cont_1_1_2"]
        self.config.cfgContent.Type=self.enum.ContentType.text
        self.config.cfgContent.Options.Excludes=["div.left_zw table:eq(0)"]      
        self.config.cfgContent.Options.PageSimilarity=0.95
        self.config.cfgContent.Options.PageNum=0
        self.config.cfgContent.Options.PageLamda=lambda *x:x[1]
        #self.config.cfgContent.Options.Lamda=lambda *x:x[1]        
        return self.config

    
    def csqueryPagination(self,csdom,pagesPaths):
        return super(ChinanewsContentAnalyst,self).csqueryPagination(csdom,pagesPaths)
    
    
    def csqueryConents(self,csdompagination):        
        results=[]
        for index,cspage in enumerate(csdompagination):            
            csbody=cspage     
            #注释部分需要调整，否则丢失图片，例如：http://www.chinanews.com/yl/2014/09-12/6587254.shtml            
            csbody.Children('div.left_ph').PrevAll().Remove()
            csbody.Children('#tupian_div').PrevAll().Remove()            
            csbody.Children('div.left_zw').NextAll().Remove()            
            results.append(csbody)
        return results

    def firstCsdomp(self,firstcsdompage):
        """从第一个段落p中提取摘要"""        
        if self.result.article_properties["summary"]=="":
            selectors=["p:eq(0)","p:eq(1)","p:eq(2)","p:eq(3)"]
            for index,sel in enumerate(selectors):        
                domp=firstcsdompage.Find(sel)
                csp=CsQuery.CQ.Create(domp)
                text=csp.Text().strip()
                text,number=re.subn('[\n\t]','',text)
                if text=="" or len(text)<5:
                    continue              
                hasEndSymbol=False 
                sumary=""               
                for i in range(0,len(text),1):
                    if isEndSymbol(text[i],["?","？","!","！","。"]):
                        hasEndSymbol=True
                        summary=text[0:i]+" ..." 
                        self.result.article_properties["summary"]=summary                   
                        return
        return

def getresult(url=''):   
    contentAnalyst=ChinanewsContentAnalyst()
    contentAnalyst.execute(url);
    content=contentAnalyst.result.content
    echoStr=content.replace("\n","").replace("\t","")
    echo(echoStr)
    return contentAnalyst.result.toJsonString()

#getresult(URL)
#############################测试用例#############################

class TC1(unittest.TestCase):
    def __init__(self, methodName = 'runTest'):
        super(TC1, self).__init__(methodName)
        self.contentAnalyst=ChinanewsContentAnalyst()
       
    def testConfig(self):
        result=getresult("http://finance.chinanews.com/fortune/2014/10-21/6700351.shtml")        
        result=FunctionHelper.string2object(result)
        self.assertGreater(result.article_properties["title"].find("央行开展200亿正回购操作 银行体系流动性充裕"),-1  )
        self.assertEqual(result.article_properties["author"],"")
        self.assertEqual(result.article_properties["source"],"中国经济网")
        self.assertGreater(result.article_properties["summary"].find("中国经济网北京10月21日讯 据央行网站消息"),-1)        
        self.assertGreater(result.content.find("续更多的定向宽松政策值得期待，形式或较为多样。"),-1) 
        self.assertEqual(result.article_properties["issuedate"]," 2014年10月21日 11:50")
        pass

        result=getresult("http://www.chinanews.com/gn/2014/09-15/6590236.shtml")        
        result=FunctionHelper.string2object(result)
        self.assertGreater(result.article_properties["title"].find("上海合作组织秘书长：组织内部协作达到新水平"),-1  )
        self.assertEqual(result.article_properties["author"],"")
        self.assertEqual(result.article_properties["source"],"人民日报")
        self.assertGreater(result.article_properties["summary"].find("上海合作组织历次峰会的“公文包”里，总有重要决议，标志着上合组织内部协作达到新水平"),-1)        
        self.assertGreater(result.content.find("上海合作组织的优良传统，在今年9月12日的杜尚别峰会上再次得到证实"),-1) 
        self.assertEqual(result.article_properties["issuedate"]," 2014年09月15日 09:49")
        pass
            
        result=getresult("http://finance.chinanews.com/stock/2014/10-21/6700349.shtml")        
        result=FunctionHelper.string2object(result)
        self.assertGreater(result.article_properties["title"].find("两市冷对宏观数据 三因素致市场陷僵局"),-1  )
        self.assertEqual(result.article_properties["author"],"")
        self.assertEqual(result.article_properties["source"],"中国经济网 ")
        self.assertGreater(result.article_properties["summary"].find("A股早盘低开后震荡向上，上证综指率先翻红"),-1)
        self.assertGreater(result.content.find("击了多方人气；最后，本轮行情明显带"),-1)
        self.assertEqual(result.article_properties["issuedate"]," 2014年10月21日 11:49")         
        pass
         
        result=getresult("http://www.chinanews.com/tw/2014/09-15/6590235.shtml")        
        result=FunctionHelper.string2object(result)
        self.assertGreater(result.article_properties["title"].find("台湾老农揭发馊油险遭挟持"),-1  )
        self.assertEqual(result.article_properties["author"],"")
        self.assertEqual(result.article_properties["source"],"中国新闻网")
        self.assertGreater(result.article_properties["summary"].find("台中警方曾躲在屏东竹田乡郭烈成地下工厂旁的鸽舍搜证"),-1)
        self.assertGreater(result.content.find("屏县警局长陈国进昨表示，已指示辖区潮州警方"),-1)
        self.assertEqual(result.article_properties["issuedate"]," 2014年09月15日 09:49")         
        pass  

    

if __name__=="__main__":#sys.exit(0)      
    unittest.main()