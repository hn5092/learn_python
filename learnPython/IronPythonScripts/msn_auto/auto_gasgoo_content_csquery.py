import sys
sys.path.append("modules")
from core.framework import *

class gasgooContentAnalyst(PythonContentAnalyst):

    def setConfig(self,url):
        self.config.cfgUrl=url
        self.config.cfgCharset=self.enum.Charset.utf8
        self.config.cfgSelector=self.enum.Selector.csquery
        self.config.cfgTitle=["div.atitle h1"]
        self.config.cfgAuthor=[("p.pleft > span:eq(1)",lambda x:x[3:])]
        self.config.cfgSource=["p.pleft > span:eq(0) a"]
        self.config.cfgSummary=[]
        self.config.cfgIssuedate=["p.pleft > em"]
        self.config.cfgContent.Type=self.enum.ContentType.text
        self.config.cfgContent.Options.Excludes=["div.dpages","div#content p:last > span > b"]    
        self.config.cfgContent.Path=["div#content"]
        #self.config.cfgContent.Options.Lamda=lambda *x:x[1] #没用到 
        self.config.cfgContent.Pages=["div.dpages"] 
        self.config.cfgContent.Options.PageNum=0 #0=无限制 
        self.config.cfgContent.Options.PageLamda=lambda *x:x[1]
        self.config.cfgContent.Options.PageSimilarity=0.95 #相似度
        return self.config
    
   
    def csqueryPagination(self,csdom,pagesPaths):
        '''默认实现相似度计算，可识别路径/、？'''
        return super(gasgooContentAnalyst,self).csqueryPagination(csdom,pagesPaths)

    def csqueryConents(self,csdompagination):        
         return super(gasgooContentAnalyst,self).csqueryConents(csdompagination)

    def lastCsdomp(self,lastcsdompage):
        '''最后一个段落<p>'''
        return super(gasgooContentAnalyst,self).lastCsdomp(lastcsdompage)

    def pageContentText(self,content):
        """分页的内容清理，默认清空注释、style、onmouseover，粗体替换，unicode编码转汉字"""
        return super(gasgooContentAnalyst,self).pageContentText(content)

    def pageCsContentImage(self,cspage):
        """<img/>路径识别，默认支持/路径转换"""        
        return  super(gasgooContentAnalyst,self).pageCsContentImage(cspage)

def getresult(url=''):   
    contentAnalyst=gasgooContentAnalyst()
    contentAnalyst.execute(url);
    content=contentAnalyst.result.content
    echo(content)
    return contentAnalyst.result.toJsonString()

#getresult(URL)

####################### test case ######################
    
class gasgooContentAnalystTC(unittest.TestCase):
    def __init__(self, methodName = 'runTest'):
        super(gasgooContentAnalystTC, self).__init__(methodName)
        self.contentAnalyst=gasgooContentAnalyst()
       
    def testConfig(self):
        result=getresult("http://auto.gasgoo.com/News/2015/05/08015419541960334840705.shtml")
        result=FunctionHelper.string2object(result)
        self.assertGreater(result.article_properties["title"].find("奔腾X80纪念版5月8日上市 外观内饰小改"),-1  )
        self.assertEqual(result.article_properties["author"],"盖世汽车研究院") 
        #self.assertGreater(result.article_properties["summary"].find(""),-1)
        self.assertEqual(result.article_properties["source"],"盖世汽车网")         
        self.assertEqual(result.article_properties["issuedate"],"14-11-17 07:00")
        self.assertGreater(result.content.find("在目前的国内汽车市场上，儿童乘车安全的相关配置普及率极低"),-1)
        pass


        result=getresult("http://info.xcar.com.cn/201505/news_1795505_1.html")
        result=FunctionHelper.string2object(result)
        self.assertGreater(result.article_properties["title"].find("奔腾X80纪念版5月8日上市 外观内饰小改"),-1  )
        self.assertEqual(result.article_properties["author"],"盖世汽车研究院") 
        #self.assertGreater(result.article_properties["summary"].find(""),-1)
        self.assertEqual(result.article_properties["source"],"盖世汽车网")         
        self.assertEqual(result.article_properties["issuedate"],"14-11-17 07:00")
        self.assertGreater(result.content.find("在目前的国内汽车市场上，儿童乘车安全的相关配置普及率极低"),-1)
        pass


        result=getresult("http://auto.gasgoo.com/News/2014/07/09034610461060303780716.shtml")
        result=FunctionHelper.string2object(result)
        self.assertGreater(result.article_properties["title"].find("儿童乘车安全受关注新车安装相关配置渐成趋势"),-1  )
        self.assertEqual(result.article_properties["author"],"盖世汽车研究院") 
        #self.assertGreater(result.article_properties["summary"].find(""),-1)
        self.assertEqual(result.article_properties["source"],"盖世汽车网")         
        self.assertEqual(result.article_properties["issuedate"],"14-11-17 07:00")
        self.assertGreater(result.content.find("在目前的国内汽车市场上，儿童乘车安全的相关配置普及率极低"),-1)
        pass

        result=getresult("http://auto.gasgoo.com/News/2014/11/140712041246031684412.shtml")
        result=FunctionHelper.string2object(result)
        self.assertGreater(result.article_properties["title"].find("高田在墨西哥扩产气囊替换零件 应对召回"),-1  )
        self.assertEqual(result.article_properties["author"],"Ryan") 
        #self.assertGreater(result.article_properties["summary"].find(""),-1)
        self.assertEqual(result.article_properties["source"],"盖世汽车网")         
        self.assertEqual(result.article_properties["issuedate"],"14-11-17 03:12")
        self.assertGreater(result.content.find("目前难以确定这两家公司能否在高田的新生产线投产之前开始生产"),-1)
        pass
        
        result=getresult("http://auto.gasgoo.com/News/2014/11/1611240024060316895263.shtml")
        result=FunctionHelper.string2object(result)
        self.assertGreater(result.article_properties["title"].find("2014年10月国产外资品牌销量分析"),-1  )
        self.assertEqual(result.article_properties["author"],"盖世汽车研究院") 
        #self.assertGreater(result.article_properties["summary"].find(""),-1)
        self.assertEqual(result.article_properties["source"],"盖世汽车网")         
        self.assertEqual(result.article_properties["issuedate"],"14-11-17 07:00")
        self.assertGreater(result.content.find("美系品牌10月乘用车销量21.04万辆，同比仅增2.4%。其中"),-1)
        pass
    
        result=getresult("http://auto.gasgoo.com/News/2014/11/18074437443760317082662.shtml")
        result=FunctionHelper.string2object(result)
        self.assertGreater(result.article_properties["title"].find("高田气囊门遭对手趁虚而入"),-1  )
        self.assertEqual(result.article_properties["author"],"Martin Shi") 
        #self.assertGreater(result.article_properties["summary"].find(""),-1)
        self.assertEqual(result.article_properties["source"],"盖世汽车网")         
        self.assertEqual(result.article_properties["issuedate"],"14-11-18 07:44")
        self.assertGreater(result.content.find("而不是仅仅因为召回而替换"),-1)
        pass
    

if __name__=="__main__":#sys.exit(0) 
    unittest.main()


#v1.0 旧脚本
#def removefomate(content):
#    p1,number=re.subn('class=[\"|\']?.*?[\"|\']','',content)

#    p2,number=re.subn('<script[^>]*?>[\\s\\S]*?<\\/script>','',p1)
#    p3,number=re.subn('style=[\"|\'][\\s\\S]*?[\"|\']','',p2)
#    p4,number=re.subn('<table[^>]*?>[\\s\\S]*?<\\/table>','',p3)
#    p5,number=re.subn('</?(a|div)[^<>]*>','',p4)
     
#    p7,number=re.subn("(?<=<img[\\s\\S]*?src=[\'\"])[(../)]*(?=[^\'\"]+[\'\"][\\s\\S]*?>)", "http://auto.gasgoo.com/",p5)
   
#    return p7

#def getresult(url=''):    
#    request=  HttpRequest()
#    result=request.getResponseStr(url=url,ifmodifysince='')
#    result.body=result.body.decode('utf-8')
#    cqhtml=  PyCQ(html=result.body)
#    cqcontent=cqhtml.select('#info')
#    articleinfo=cqcontent
#    result.article_properties['title']=articleinfo.select(".dtil").select('h1').text().strip()
    
#    result.article_properties['issuedate']=articleinfo.select(".dwirts").select("dt").select("span").eq(0).text().strip()
#    result.article_properties['source']=articleinfo.select(".dwirts").select("dt").select("span").eq(1).select("a").text().strip()

#    #author=cqcontent.select('.article_text_title02').text()
#    #author=author[author.index("作者")+3:]
#    result.article_properties['author']=""
#    result.article_properties['summary']=""
#    content=cqcontent.select('#content').select("p").render()
#    p1con=removefomate(content)
     
#    #因为这个网站的内容有分页 故需要拼接各页的内容
#    #先判断是否有多页
#    pflag=cqhtml.select(".dpage").select("a").eq(0).text() ; 
     
#    if pflag !="" :
#        #p6="有多页"+p6.strip()
#        t=cqhtml.select(".dpage").select("a").render() 
#        p=re.compile("href=(\S*?)[\s|>]")
#        hrefs=p.findall(t)  
#        #这样能保存数组里面的元素原来的位置 
#        #hrefs=hrefs.pop()
#        hrefs.pop()
       
#        hrefs2 = list(set(hrefs))
#        hrefs2.sort(key=hrefs.index)
#        con=""
#        if hrefs2:
#            for ht in hrefs2: 
#                request=  HttpRequest()
#                result2=request.getResponseStr(url="http://auto.gasgoo.com/"+ht.strip("\""),ifmodifysince='')
#                result2.body=result2.body.decode('utf-8')
#                cqhtml2=  PyCQ(html=result2.body)
#                con+="@@abcMSNPageMarkerabc@@"+removefomate(cqhtml2.select('#content').select("p").render() )
                
#        result.content=p1con +con
#    else:
#        result.content=p1con.strip()
    
#    return result
 
#getresult(URL)