import sys
sys.path.append("modules")
from core.framework import *

import time
class PaperPeopleContentAnalyst(PythonContentAnalyst):

    def setConfig(self,url):
        self.config.cfgUrl=url
        self.config.cfgCharset=self.enum.Charset.utf8
        self.config.cfgSelector=self.enum.Selector.csquery
        self.config.cfgTitle=["div.text_c > h1"]
        self.config.cfgAuthor=[("div.text_c > h4",lambda x:x.replace("本报记者","").strip())]
        self.config.cfgSource=[("div.lai",lambda x:x[x.find("《")+1:x.find("》")-1].replace("\n","").strip())]
        self.config.cfgSummary=["div.text_c > h3"]
        self.config.cfgIssuedate=[("div.lai",lambda x:x[x.find("》")+1:])]
        self.config.cfgContent.Type=self.enum.ContentType.text
        self.config.cfgContent.Options.Excludes=["input"]    
        self.config.cfgContent.Path=["div.c_c"]         
        self.config.cfgContent.Pages=[] 
        self.config.cfgContent.Options.PageNum=0 #0=限制 
        self.config.cfgContent.Options.PageLamda=lambda *x:x[1]
        self.config.cfgContent.Options.PageSimilarity=0.95 #相似度
        return self.config


    def csqueryPagination(self,csdom,pagesPaths):
        '''默认实现相似度计算，可识别路径/、？'''
        return super(PaperPeopleContentAnalyst,self).csqueryPagination(csdom,pagesPaths)

    def csqueryConents(self,csdompagination):
        return super(PaperPeopleContentAnalyst,self).csqueryConents(csdompagination)

    def lastCsdomp(self,lastcsdompage):
        '''最后一个段落<p>'''
        csparent=lastcsdompage.Find("p").First().Parent()
        return super(PaperPeopleContentAnalyst,self).lastCsdomp(csparent)

    def pageContentText(self,content):
        """分页的内容清理，默认清空注释、style、onmouseover，粗体替换，unicode编码转汉字"""
        return super(PaperPeopleContentAnalyst,self).pageContentText(content)

    def pageCsContentImage(self,cspage):
        """<img/>路径识别，默认支持/路径转换"""        
        return  super(PaperPeopleContentAnalyst,self).pageCsContentImage(cspage)

def getresult(url=''):   
    contentAnalyst=PaperPeopleContentAnalyst()
    contentAnalyst.execute(url);
    content=contentAnalyst.result.content
    echo(content)
    return contentAnalyst.result.toJsonString()

#getresult(URL)

####################### test case ######################
    
class PaperPeopleContentAnalystTC(unittest.TestCase):
    def __init__(self, methodName = 'runTest'):
        super(PaperPeopleContentAnalystTC, self).__init__(methodName)
        self.contentAnalyst=PaperPeopleContentAnalyst()
       
    def testConfig(self):         
        result=getresult("http://paper.people.com.cn/rmrb/html/2014-10/20/nw.D110000renmrb_20141020_1-18.htm")
        result=FunctionHelper.string2object(result)
        self.assertGreater(result.article_properties["title"].find("改革预期催升股市（热点聚焦·股市新观察①"),-1)
        self.assertEqual(result.article_properties["author"],"吴秋余")
        #print result.article_properties["summary"]
        self.assertGreater(result.article_properties["summary"].find("指更是创出历史新高"),-1)
        self.assertEqual(result.article_properties["source"],"人民日报")        
        self.assertGreater(result.article_properties["issuedate"].find("2014年10月20日"),-1)
        self.assertGreater(result.content.find("，要继续严厉打击上市公司的造假、圈钱等行为"),-1) 
        print result.article_properties["source"],result.article_properties["issuedate"]
           
        result=getresult("http://paper.people.com.cn/rmrb/html/2014-10/16/nw.D110000renmrb_20141016_4-01.htm")
        result=FunctionHelper.string2object(result)
        self.assertGreater(result.article_properties["title"].find("关于坚持和完善普通高等"),-1)
        self.assertEqual(result.article_properties["author"],"")
        self.assertEqual(result.article_properties["summary"],"")
        self.assertGreater(result.article_properties["source"].find("人民日报"),-1)        
        self.assertGreater(result.article_properties["issuedate"].find("2014年10月16日"),-1)
        self.assertGreater(result.content.find("的中国特色社会主义事业合格建设者和可靠接班"),-1) 
        print result.article_properties["source"],result.article_properties["issuedate"]             
       
        pass
        

if __name__=="__main__":#sys.exit(0) 
    unittest.main()
