import sys
sys.path.append("modules")
from core.framework import *

class NewscnContentAnalyst(PythonContentAnalyst):

    def setConfig(self,url):
        self.config.cfgUrl=url
        self.config.cfgCharset=""
        self.config.cfgSelector=self.enum.Selector.csquery
        self.config.cfgTitle=[("h1#title",lambda x:x.strip())]
        self.config.cfgAuthor=[]
        self.config.cfgSource=[("span#source",lambda x:x[4:].strip())]
        self.config.cfgSummary=[]
        self.config.cfgIssuedate=[("span#pubtime",lambda x:x.strip())]
        self.config.cfgContent.Pages=[""]
        self.config.cfgContent.Path=["div#content"]
        self.config.cfgContent.Type=self.enum.ContentType.text
        self.config.cfgContent.Options.Excludes=[]      
        self.config.cfgContent.Options.PageSimilarity=0.95
        self.config.cfgContent.Options.PageNum=0
        self.config.cfgContent.Options.PageLamda=lambda *x:x[1]            
        return self.config
    
    def csqueryPagination(self,csdom,pagesPaths):
        return super(NewscnContentAnalyst,self).csqueryPagination(csdom,pagesPaths)

    #清空（***）
    def pageContentText(self,content):                
         content=super(NewscnContentAnalyst,self).pageContentText(content) 
         return content
    
    
def getresult(url=''):   
    contentAnalyst=NewscnContentAnalyst()
    contentAnalyst.execute(url);
    content=contentAnalyst.result.content
    echo(content)
    return contentAnalyst.result.toJsonString()

#getresult(URL)

############################# test case #############################

class NewscnContentTC(unittest.TestCase):
        def __init__(self, methodName = 'runTest'):
            super(NewscnContentTC, self).__init__(methodName)
            self.contentAnalyst=NewscnContentAnalyst()
       
        def testConfig(self):            
            url="http://news.xinhuanet.com/fortune/2014-10/11/c_1112785481.htm"
            result=getresult(url)
            result=FunctionHelper.string2object(result)
            print result.article_properties
            self.assertGreater(result.article_properties["title"].find("深辨中国经济新常态之三——全球竞合升级版的中企演进"),-1  )
            self.assertEqual(result.article_properties["author"],"")
            self.assertEqual(result.article_properties["source"],"新华网")
            self.assertEqual(result.article_properties["summary"],"")
            self.assertEqual(result.article_properties["issuedate"],"2014年09月18日 12:53:56")
            self.assertGreaterEqual(result.content.find("俄罗斯信息分析中心网站的一篇文章这样写道：显然，中国商业正在迈向新阶段"),-1) 
            pass

            url="http://news.xinhuanet.com/fortune/2014-09/18/c_1112532966.htm"
            result=getresult(url)
            print result.article_properties
            self.assertGreater(result.article_properties["title"].find("深辨中国经济新常态之三——全球竞合升级版的中企演进"),-1  )
            self.assertEqual(result.article_properties["author"],"")
            self.assertEqual(result.article_properties["source"],"新华网")
            self.assertEqual(result.article_properties["summary"],"")
            self.assertEqual(result.article_properties["issuedate"],"2014年09月18日 12:53:56")
            self.assertGreater(result.content.find("俄罗斯信息分析中心网站的一篇文章这样写道：显然，中国商业正在迈向新阶段"),-1) 
            pass

            url="http://news.xinhuanet.com/fortune/2014-09/11/c_126976059.htm"
            result=getresult(url)
            print result.article_properties
            self.assertGreater(result.article_properties["title"].find("网售处方药放开在即"),-1  )
            self.assertEqual(result.article_properties["author"],"")
            self.assertEqual(result.article_properties["source"],"羊城晚报")
            self.assertEqual(result.article_properties["summary"],"")
            self.assertEqual(result.article_properties["issuedate"],"2014年09月11日 15:01:29")
            self.assertGreater(result.content.find("国内一家药店的老总表示，重提医药分家、处方外流都是次要问题"),-1) 
            pass

            url="http://news.xinhuanet.com/fortune/2014-09/10/c_126972132.htm"
            result=getresult(url)
            print result.article_properties
            self.assertEqual(result.article_properties["title"],'北京分行绿色通道轻松兑换小面额残损币'  )
            self.assertEqual(result.article_properties["author"],"")
            self.assertEqual(result.article_properties["source"],"新华财经")
            self.assertEqual(result.article_properties["summary"],"")
            self.assertEqual(result.article_properties["issuedate"],"2014年09月10日 16:46:07")
            self.assertGreater(result.content.find("既是认真履行残缺人民币的兑换义务的体现"),-1) 
            pass

            url="http://news.xinhuanet.com/fortune/2014-08/29/c_126933166.htm"
            result=getresult(url)
            print result.article_properties
            self.assertEqual(result.article_properties["title"],'华远地产下半年欲推货90亿元 任志强坚持“不降价”'  )
            self.assertEqual(result.article_properties["author"],"")
            self.assertEqual(result.article_properties["source"],"证券日报")
            self.assertEqual(result.article_properties["summary"],"")
            self.assertEqual(result.article_properties["issuedate"],"2014年08月29日 10:21:26")
            self.assertGreater(result.content.find("王丽新"),-1) 
            pass

            url="http://news.xinhuanet.com/fortune/2014-08/29/c_126933242.htm"
            result=getresult(url)
            print result.article_properties
            title=result.article_properties["title"]
            print title
            self.assertEqual(title,'不动产统一登记制度 牵一发动全身')
            self.assertEqual(result.article_properties["author"],"")
            self.assertEqual(result.article_properties["source"],"证券日报")
            self.assertEqual(result.article_properties["summary"],"")
            self.assertEqual(result.article_properties["issuedate"],"2014年08月29日 10:20:56")
            self.assertGreater(result.content.find("安 宁"),-1) 
            pass

            url="http://news.xinhuanet.com/fortune/2014-08/29/c_1112281710.htm"
            result=getresult(url)
            print result.article_properties
            self.assertEqual(result.article_properties["title"],'空气净化器去除甲醛99%?基本是"忽悠" 想买,咋选择?'  )
            self.assertEqual(result.article_properties["author"],"")
            self.assertEqual(result.article_properties["source"],"新华网")
            self.assertEqual(result.article_properties["summary"],"")
            self.assertEqual(result.article_properties["issuedate"],"2014年08月29日 10:55:49")
            self.assertGreater(result.content.find("("),-1)            
            pass
        
if __name__=="__main__":#sys.exit(0)
    unittest.main()



