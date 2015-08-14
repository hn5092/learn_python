import sys
sys.path.append("modules")
from core.framework import *

class PeopleContentAnalyst(PythonContentAnalyst):

    def setConfig(self,url):
        self.config.cfgUrl=url
        self.config.cfgCharset=self.enum.Charset.gb2312
        self.config.cfgSelector=self.enum.Selector.csquery
        self.config.cfgTitle=[("h1#p_title",lambda x:x.strip())]
        self.config.cfgAuthor=[("p.author",lambda x:x.find("本报记者")>-1 and x[x.find("本报记者")+4:].strip() or x.strip())]
        self.config.cfgSource=[("span#p_origin a",lambda x:x.strip())]
        self.config.cfgSummary=[]
        self.config.cfgIssuedate=[("span#p_publishtime",lambda x:x.strip())]
        self.config.cfgContent.Pages=[""]
        self.config.cfgContent.Path=["div#p_content"]
        self.config.cfgContent.Type=self.enum.ContentType.text
        self.config.cfgContent.Options.Excludes=[]      
        self.config.cfgContent.Options.PageSimilarity=0.95
        self.config.cfgContent.Options.PageNum=0
        self.config.cfgContent.Options.PageLamda=lambda *x:x[1]
        self.config.cfgContent.Options.Lamda=lambda *x:x[1]        
        return self.config
    
    def csqueryPagination(self,csdom,pagesPaths):
        return super(PeopleContentAnalyst,self).csqueryPagination(csdom,pagesPaths)

    def csqueryConents(self,csdompagination):        
        results=[]
        for index,cspage in enumerate(csdompagination):            
            csbody=cspage
            csbody.Children("div.otitle").Remove()       
            csbody.Children("p:last-child").NextAll().Remove()
            csbody.Children('p span#paper_num').Remove()            
            results.append(csbody)
        return results


############################# test case#############################

def getresult(url=''):   
    contentAnalyst=PeopleContentAnalyst()
    contentAnalyst.execute(url);
    content=contentAnalyst.result.content
    echo(content) 
    return contentAnalyst.result.toJsonString()

class TC3(unittest.TestCase):
        def __init__(self, methodName = 'runTest'):
            super(TC3, self).__init__(methodName)
            self.contentAnalyst=PeopleContentAnalyst()
       
        def testConfig(self): 
            url="http://finance.people.com.cn/money/n/2014/0904/c388504-25603819.html"
            result=getresult(url)
            print result.article_properties
            self.assertEqual(result.article_properties["title"],'OECD:2015年经合组织成员国地区失业率或降至7.1%')
            #self.assertEqual(result.article_properties["author"],"")
            self.assertEqual(result.article_properties["source"],"")
            self.assertEqual(result.article_properties["summary"],"")
            self.assertEqual(result.article_properties["issuedate"],"2014年09月04日12:28")  
            #self.assertEqual(result.content.find("《 人民日报 》（ 2014年08月27日 10 版）"),-1)           
            pass

            
            url="http://finance.people.com.cn/insurance/n/2014/0827/c59941-25544813.html"
            result=getresult(url)
            print result.article_properties
            self.assertEqual(result.article_properties["title"],'保险法证券法等拟修改')
            #self.assertEqual(result.article_properties["author"],"彭 波 毛 磊")
            self.assertEqual(result.article_properties["source"],"人民网－人民日报")
            self.assertEqual(result.article_properties["summary"],"")
            self.assertEqual(result.article_properties["issuedate"],"2014年08月27日04:04")  
            self.assertEqual(result.content.find("《 人民日报 》（ 2014年08月27日 10 版）"),-1)           
            pass
              
            url="http://finance.people.com.cn/n/2014/0831/c1004-25573797.html"
            result=getresult(url)
            print result.article_properties
            self.assertGreater(result.article_properties["title"].find("伊利上半年营收274.71亿"),-1)#'招财宝“可变现融资”，噱头还是创新？
            self.assertEqual(result.article_properties["author"],"")
            self.assertEqual(result.article_properties["source"],"人民网-财经频道")
            self.assertEqual(result.article_properties["summary"],"")
            self.assertEqual(result.article_properties["issuedate"],"2014年08月31日14:55")            
            pass
                       
            url="http://finance.people.com.cn/n/2014/0903/c1004-25592024.html"
            result=getresult(url)
            print result.article_properties
            self.assertGreater(result.article_properties["title"].find("“中企500强”国企民营“六四开”"),-1)#'招财宝“可变现融资”，噱头还是创新？
            self.assertEqual(result.article_properties["author"],"梁薇薇")
            self.assertEqual(result.article_properties["source"],"新京报")
            self.assertEqual(result.article_properties["summary"],"")
            self.assertEqual(result.article_properties["issuedate"],"2014年09月03日07:22")
            #self.assertEqual(result.content.find("主政下吕梁的“红顶”与“黑金”"),-1) 
            pass                     


            url="http://finance.people.com.cn/n/2014/0901/c1004-25576197.html"
            result=getresult(url)
            print result.article_properties
            self.assertGreater(result.article_properties["title"].find("聂春玉被查或由邢利斌牵出"),-1)#'招财宝“可变现融资”，噱头还是创新？
            self.assertEqual(result.article_properties["author"],"周清树")
            self.assertEqual(result.article_properties["source"],"新京报")
            self.assertEqual(result.article_properties["summary"],"")
            self.assertEqual(result.article_properties["issuedate"],"2014年09月01日08:19")
            self.assertEqual(result.content.find("主政下吕梁的“红顶”与“黑金”"),-1) 
            pass

            url="http://finance.people.com.cn/n/2014/0827/c1004-25545432.html"
            result=getresult(url)
            print result.article_properties
            self.assertGreater(result.article_properties["title"].find("微软反垄断案涉浏览器播放器"),-1)#'微软反垄断案涉浏览器播放器 工商总局称正调查'
            self.assertEqual(result.article_properties["author"],"")
            self.assertEqual(result.article_properties["source"],"京华时报")
            self.assertEqual(result.article_properties["summary"],"")
            self.assertEqual(result.article_properties["issuedate"],"2014年08月27日07:19")
            self.assertEqual(result.content.find("记者顾梦琳韩旭"),-1) 
            pass

            url="http://finance.people.com.cn/n/2014/0901/c1004-25576217.html"
            result=getresult(url)
            print result.article_properties
            self.assertGreater(result.article_properties["title"].find("地方政府被指迷恋审批:地质公园立项盖近百公章"),-1)#'招财宝“可变现融资”，噱头还是创新？
            self.assertEqual(result.article_properties["author"],"储信艳")
            self.assertEqual(result.article_properties["source"],"新京报")
            self.assertEqual(result.article_properties["summary"],"")
            self.assertEqual(result.article_properties["issuedate"],"2014年09月01日08:20")
            self.assertEqual(result.content.find("记者 储信艳 实习生 赵欢"),-1) 
            pass 

            url="http://finance.people.com.cn/money/n/2014/0827/c218900-25544765.html"
            result=getresult(url)
            print result.article_properties
            self.assertGreater(result.article_properties["title"].find("噱头还是创新"),-1)#'招财宝“可变现融资”，噱头还是创新？
            self.assertEqual(result.article_properties["author"],"苏曼丽")
            self.assertEqual(result.article_properties["source"],"新京报")
            self.assertEqual(result.article_properties["summary"],"")
            self.assertEqual(result.article_properties["issuedate"],"2014年08月27日03:34")
            self.assertEqual(result.content.find("苏曼丽"),-1) 
            pass


if __name__=="__main__":#sys.exit(0)
    unittest.main()




