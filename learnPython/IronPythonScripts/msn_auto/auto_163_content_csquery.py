import sys
sys.path.append("modules")
from core.framework import *

class auto163ContentAnalyst(PythonContentAnalyst):

    def setConfig(self,url):
        self.config.cfgUrl=url
        self.config.cfgCharset=self.enum.Charset.gb2312
        self.config.cfgSelector=self.enum.Selector.csquery
        self.config.cfgTitle=["h1#h1title","h3.title span"] 
        self.config.cfgAuthor=["div.bct p:eq(0)",("div.ep-source span",lambda x:x[x.rfind(":")-1:])] #("p.pleft > span:eq(1)",lambda x:x[3:])
        self.config.cfgSource=["div.clearfix div.ep-info div.left a:eq(0)","a#ne_article_source","div.bct p:last","span.info a:eq(0)","div.ep-time-soure a:eq(0)"]
        self.config.cfgSummary=["p.ep-summary","div.ds_page_summarize","p.summary"]
        self.config.cfgIssuedate=[("div.clearfix div.ep-info div.left",lambda x:gettime(x)),("div.clearfix div.ep-time-soure",lambda x:gettime(x)),"span.pleft span.blogsep:eq(0)"]
        self.config.cfgContent.Type=self.enum.ContentType.text
        self.config.cfgContent.Options.Excludes=["div.ds_order","div.ep-pages","div.ep-pagenav","div.sharecommend-wrap","div.nph_photo_ctrl","div.nph_cnt","h1#h1title","div.clearfix","p.ep-summary","link","div#gallery176177","div.extra-tag","div.WZTJ_htpGG","div.ep-pages","div.sharecommend-wrap","div.ep-keywords","div#auto_comment","div.newcar_pic_mod","div.atleLP","div.sy_page_bottom","div.autoinfocard"]    
        self.config.cfgContent.Path=["div.end-text","div#endText","div.bct"]
        #self.config.cfgContent.Options.Lamda=lambda *x:x[1] #没用到 
        self.config.cfgContent.Pages=["div.ep-pages"] 
        self.config.cfgContent.Options.PageNum=0 #0=无限制 
        self.config.cfgContent.Options.PageLamda=lambda *x:x[1]
        self.config.cfgContent.Options.PageSimilarity=0.95 #相似度
        return self.config
    
   
    def csqueryPagination(self,csdom,pagesPaths):
        '''默认实现相似度计算，可识别路径/、？'''
        return super(auto163ContentAnalyst,self).csqueryPagination(csdom,pagesPaths)

    def csqueryConents(self,csdompagination):
        return super(auto163ContentAnalyst,self).csqueryConents(csdompagination)

    def lastCsdomp(self,lastcsdompage):
        '''最后一个段落<p>'''
        return super(auto163ContentAnalyst,self).lastCsdomp(lastcsdompage)

    def pageContentText(self,content):
        """分页的内容清理，默认清空注释、style、onmouseover，粗体替换，unicode编码转汉字"""
        try:
            content=RemoveText(content,['<!--[^>]*?-->','(?<=style=["\'])[^"\']+','(?<=onmouseover=["\'])[^"\']+'])
            content=self.defaultReplace(content)
            content=StringHelper.EscapeUnicode(content)     
            echo(content)
        except Exception as err:
            pass
        finally:
            return content
        #return super(auto163ContentAnalyst,self).pageContentText(content)

    def pageCsContentImage(self,cspage):
        """<img/>路径识别，默认支持/路径转换"""        
        return  super(auto163ContentAnalyst,self).pageCsContentImage(cspage)

def getresult(url=''):   
    contentAnalyst=auto163ContentAnalyst()
    contentAnalyst.execute(url);
    content=contentAnalyst.result.content
    echo(content)
    return contentAnalyst.result.toJsonString()

def gettime(str):
    #import re 
    #p=re.compile('\s+') 
    #trimstr=re.sub(p,'',str) 
    trimstr=str.strip()
    trimstr=trimstr[:19]
    return trimstr

#getresult(URL)

####################### test case ######################
    
class auto163ContentAnalystTC(unittest.TestCase):
    def __init__(self, methodName = 'runTest'):
        super(auto163ContentAnalystTC, self).__init__(methodName)
        self.contentAnalyst=auto163ContentAnalyst()
       
    def testConfig(self): 
        result=getresult("http://auto.163.com/15/0605/16/ARC2LRM50008581L.html")
        result=FunctionHelper.string2object(result)
        self.assertGreater(result.article_properties["title"].find("哈弗H9降价促销优惠1.00万"),-1)       
        self.assertGreater(result.article_properties["summary"].find("库存方面店内现车充足详细请看下表"),-1)
        self.assertGreater(result.article_properties["source"].find("网易原创"),-1)         
        self.assertEqual(result.article_properties["issuedate"],"2015-06-05 16:44:39")
        #self.assertGreater(result.content.find("湖南有道汽车有限公司长城汽车哈弗店"),-1)
        #self.assertGreater(result.article_properties["author"].find("费希"),-1) 
        pass

        result=getresult("http://auto.163.com/15/0603/11/AR6D05UA00084TUO.html")
        result=FunctionHelper.string2object(result)
        self.assertGreater(result.article_properties["title"].find("前驱平台/空间增大"),-1)       
        self.assertGreater(result.article_properties["summary"].find("日前，宝马官方正式发布"),-1)
        self.assertGreater(result.article_properties["source"].find("网易汽车"),-1)         
        self.assertEqual(result.article_properties["issuedate"],"2015-06-03 11:49:37")
        self.assertGreater(result.content.find("首批上市的新车为采用前轮驱动的X1"),-1)
        self.assertGreater(result.article_properties["author"].find("费希"),-1) 
        pass 

        result=getresult("http://jluautoman.blog.163.com/blog/static/20063036620137297658934/")
        result=FunctionHelper.string2object(result)
        self.assertGreater(result.article_properties["title"].find("千牌车主事件"),-1)       
        #self.assertGreater(result.article_properties["summary"].find("着更多的人才"),-1)
        self.assertGreater(result.article_properties["source"].find("版权授予网易汽车"),-1)         
        self.assertEqual(result.article_properties["issuedate"],"2013-08-29 07:06:58")
        self.assertGreater(result.content.find("的幌子进行呢"),-1)
        self.assertGreater(result.article_properties["author"].find("文/墨鱼"),-1) 
        pass 

        result=getresult("http://auto.163.com/15/0515/19/APM88OFI00084TV5.html")
        result=FunctionHelper.string2object(result)
        self.assertGreater(result.article_properties["title"].find("长安福特营销趋向年轻化"),-1)       
        self.assertGreater(result.article_properties["summary"].find("着更多的人才"),-1)
        self.assertEqual(result.article_properties["source"],"网易汽车")         
        self.assertEqual(result.article_properties["issuedate"],"2015-05-15 19:03:22")
        self.assertGreater(result.content.find("提升青年群体的汽车驾驶意识与责任，为企业自身和汽车领域发展选拔、培养优秀人才"),-1)
        self.assertGreater(result.article_properties["author"].find("张南"),-1) 
        pass 

        #result=getresult("http://auto.163.com/13/0516/22/8V1H8EEA00084TV1.html")
        #result=FunctionHelper.string2object(result)
        #self.assertGreater(result.article_properties["title"].find("百亿经销商达25家 扩张未带来规模效应"),-1)       
        #self.assertGreater(result.article_properties["summary"].find("利润水平有很大的下滑"),-1)
        #self.assertEqual(result.article_properties["source"],"网易汽车")         
        #self.assertEqual(result.article_properties["issuedate"],"2013-05-16 22:46:00")
        #self.assertGreater(result.content.find("30位的经销商集团中的30.5%"),-1)
        #self.assertGreater(result.article_properties["author"].find("章章"),-1) 
        #pass 


        #result=getresult("http://auto.163.com/14/1215/20/ADHJB9U800084JTI.html")
        #result=FunctionHelper.string2object(result)
        #self.assertGreater(result.article_properties["title"].find("萨瓦纳野出真性情"),-1)       
        #self.assertGreater(result.article_properties["summary"].find("拉尔极地挑战"),-1)
        ##self.assertGreater(result.article_properties["author"].find("王晖"),-1) 
        #self.assertEqual(result.article_properties["source"],"网易汽车")         
        #self.assertEqual(result.article_properties["issuedate"],"2014-12-15 20:32:26")
        #self.assertGreater(result.content.find("越野族”带来更多惊喜"),-1)        
        #pass


        #result=getresult("http://auto.163.com/15/0602/19/AR4MJKA800084TUO.html")
        #result=FunctionHelper.string2object(result)
        #self.assertGreater(result.article_properties["title"].find("高配采用LED光源 国产金牛座多车型谍照"),-1)       
        #self.assertGreater(result.article_properties["summary"].find("素大灯，而高配车型则为LED"),-1)
        ##self.assertGreater(result.article_properties["author"].find("王晖"),-1) 
        #self.assertEqual(result.article_properties["source"],"网易汽车")         
        #self.assertEqual(result.article_properties["issuedate"],"2015-06-02 19:59:02")
        #self.assertGreater(result.content.find("动力方面，国产金牛座将搭载1.5T、2.0T以及2.7T三款发动机，传动方面，或将匹配6速双离合变速箱。"),-1)        
        #pass

        #result=getresult("http://auto.163.com/15/0528/05/AQM8PR7R00084TUR_5.html")
        #result=FunctionHelper.string2object(result)
        #self.assertGreater(result.article_properties["title"].find("试驾力帆820旗舰版"),-1)       
        #self.assertGreater(result.article_properties["summary"].find("二线品牌力帆这款车怎么能够“行”呢"),-1)
        #self.assertGreater(result.article_properties["author"].find("王晖"),-1) 
        #self.assertEqual(result.article_properties["source"],"网易汽车")         
        #self.assertEqual(result.article_properties["issuedate"],"2015-05-28 05:28:24")
        #self.assertGreater(result.content.find("好的产品、稳定的质量，才是王道"),-1)        
        #pass


    
          

if __name__=="__main__":#sys.exit(0) 
    unittest.main()
    sys.exit(0)