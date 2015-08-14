#coding=utf-8
import unittest
import sys
#sys.path.append("msn_fashion")
#sys.path.append("msn_auto")
sys.path.append("msn_finance")

#from msn_fashion import fashion_ifeng_content
#from fashion_pclady_list_csquery import *
#from fashion_pclady_list_xpath import *
#import auto_cheshi_content_csqery_xpath 
##
from finance_dayoo_list_csquery import *
from finance_dayoo_content_csquery import *
###
from finance_bjnews_list import *
from finance_bjnews_content import *
####
from finance_jinghua_list_csquery import *
from finance_jinghua_content_csquery  import *
####
from finance_bjbusiness_list_csquery import *
from finance_bjbusiness_content_csquery import *
###
from finance_xkb_list_csquery import *
from finance_xkb_content_csquery import *

from finance_chinanews_list_csquery import *
from finance_chinanews_content_csquery import *

from finance_21cbh_list_csquery import *
from finance_21cbh_content_csquery import *

Debug=True

if __name__=="__main__":#sys.exit(0) 
    unittest.main()    
    #自动测试  跑所有测试  有一个地方出错 就断了  所有页面用到就写到farmeworks 重启一下  XPASS抛弃了CSQ 不满足用XPASS  Xpass开头不用管了
    
    #class TC(unittest.TestCase):
    #    def __init__(self, methodName = 'runTest'):
    #        super(TC, self).__init__(methodName)
    #        self.ifeng_content=fashion_ifeng_content.FashionIfengContentAnalyst()
    #        self.pclady_list_xpath=FashionPcladyListAnalyst()
    #        self.pclady_list_csquery=CSFashionPcladyListAnalyst()
    #        self.auto_cheshi_content_xpath=auto_cheshi_content_csqery_xpath.CheshiContentAnalyst()
    #        self.auto_cheshi_content_csquery=auto_cheshi_content_csqery_xpath.CheshiCQContentAnalyst()
    #        self.finance_bjnews_list=BJNewsListAnalyst()
            
       
    #    def testConfig(self):
    #        result=self.finance_bjnews_list.getresult()
    #        print result
    #        self.ifeng_content.execute("http://fashion.ifeng.com/a/20140819/40035171_0.shtml")
    #        result=self.ifeng_content.result
    #        article_properties={'title':'','author':'','source':'','summary':'','issuedate':''}           
    #        print result.article_properties
    #        self.assertEqual(result.article_properties["title"],"北京时间版2015春夏纽约时装周时间表")
    #        self.assertEqual(result.article_properties["author"],"")
    #        self.assertEqual(result.article_properties["source"],"凤凰网时尚")
    #        self.assertEqual(result.article_properties["summary"],"导语：2015春夏纽约时装周（9月4日-9月12日）拉开帷幕，凤凰时尚为你精心整理看秀日程，重点秀场以星号标注供参考。以下时间均为北京时间。")
    #        self.assertEqual(result.article_properties["issuedate"],"2014年08月19日 08:11")
    #        self.assertGreaterEqual(result.content.find("@@abcMSNPageMarkerabc@@"),10)
    #        self.assertGreaterEqual(result.content.find("#embed_hzh_div"),-1)
    #        pass
            
    #        self.pclady_list_xpath.execute("http://dress.pclady.com.cn/fashion/index.html")
    #        result=self.pclady_list_xpath.result            
    #        self.assertEqual(result.article_properties["title"],"PCLADY首页")
    #        self.assertEqual(result.article_properties["author"],"时装")
    #        self.assertEqual(len(result.content.split("|")),self.pclady_list_xpath.config.cfgContent.Options.PageNum*10)

    #        self.pclady_list_csquery.execute("http://dress.pclady.com.cn/fashion/index.html")
    #        result2=self.pclady_list_csquery.result
    #        self.assertEqual(result.content,result2.content)
    #        pass

    #        url="http://news.cheshi.com/20140804/1453814.shtml"
    #        self.auto_cheshi_content_xpath.execute(url)
    #        result==self.auto_cheshi_content_xpath.result
    #        self.auto_cheshi_content_csquery.execute(url)
    #        result2=self.auto_cheshi_content_csquery.result
    #        self.assertEqual(result.article_properties["title"],result2.article_properties["title"])
    #        self.assertEqual(result.article_properties["author"],result2.article_properties["author"])
    #        self.assertEqual(result.article_properties["source"],result2.article_properties["source"])
    #        self.assertEqual(result.article_properties["summary"],result2.article_properties["summary"])
    #        self.assertEqual(result.article_properties["issuedate"],result2.article_properties["issuedate"])
    #        self.assertEqual(result.content,result2.content)
    #        pass
