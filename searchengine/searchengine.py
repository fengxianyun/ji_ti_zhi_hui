#coding:gbk
import sys
reload(sys)
'''

@author: fxy
'''
#打开url的库
import urllib2
#关于数据库
from pysqlite2 import dbapi2 as sqlite
#解析html
from bs4 import *
from urlparse import urljoin
from html5lib import *

import re

import jieba
#基本原理
#从一小组网页开始进行广度优先搜索，直至某一给定深度
#期间为网页建立索引
    #读出网页HTML
    #为每个网页建立索引
        #从html网页中提取文字
        #分词
        #将每个单词与url相关（即，本页出现的单词，与本个url有关）
    #从网页中提取<a>标签
    #检测<a>标签中是否有href属性
    #不在已存在的url中则加入
    #添加一个关联两个网页的链接
    #从头开始
#pagerank



class crawler():
    '''
    classdocs
    '''

    def __init__(self, dbname):
        self.con=sqlite.connect(dbname)
        self.ignorewords=set(['在','是','的','了','\'',',','。','~','!','@','#','$','%','^','&','*','(',')','-','+','_','=','[',']','{','}','/','?','<','>','"'])
    def __del__(self):
        self.con.close()
    def dbcommit(self):
        self.con.commit()
    
    
    #辅助函数，用于获取条目的id，并且条目不存在，就将其加入数据库
    def getentryid(self,table,field,value,createnew=True):
        cur=self.con.execute("select rowid from %s where %s='%s'" %(table,field,value))
        res=cur.fetchone()
        if res==None:
            cur=self.con.execute("insert into %s (%s) values ('%s')" %(table,field,value))
            return cur.lastrowid
        else:
            return res[0]
    
    
    
    #为每个网页建立索引
    def addtoindex(self,url,soup):
        if self.isindexed(url):
            return
        print 'Indexing '+url
        #获取每个单词
        text=self.gettextonly(soup)
        print text
        #分词
        words=self.separatewords(text)
        #得到url的id
        urlid=self.getentryid('urllist', 'url', url)
        #将每个单词与url相关
        for i in range(len(words)):
            word=words[i]
            if word in self.ignorewords:
                continue
            wordid=self.getentryid('wordlist', 'word',word)
            self.con.execute("insert into wordlocation (urlid,wordid,location)\
            values(%d,%d,%d)"%(urlid,wordid,i))
    
    
    #从html网页中提取文字（不带标签），递归调用
    #需改善
    def gettextonly(self,soup):
        #意义不明
        v=soup.string
        if v==None:
            c=soup.contents
            resulttext=''
            for t in c:
                subtext=self.gettextonly(t)
                resulttext+=str(subtext)+'\n'
            return resulttext
        else:
            return v.strip()
    
    
    
    #根据非空白字符进行分词处理
    def separatewords(self,text):
        splitter=jieba.cut(text)
        return[word for word in splitter if word!=" " and word!='\n']
    
    
    
    
    #如果url已建立过索引，则返回true
    def isindexed(self,url):
        u=self.con.execute \
        ("select rowid from urllist where url='%s'" % url).fetchone()
        if u !=None:
            v=self.con.execute('select * from wordlocation where urlid=%d' %u[0]).fetchone()
            if v!=None:
                return True
        return False
    
    
    
    #添加一个关联两个网页的链接
    def addlinkref(self,urlFrom,urlTo,linkText):
        words=self.separatewords(linkText)
        fromid=self.getentryid('urllist','url',urlFrom)
        toid=self.getentryid('urllist','url',urlTo)
        if fromid==toid: 
            return
        cur=self.con.execute("insert into link(fromid,toid) values (%d,%d)" % (fromid,toid))
        linkid=cur.lastrowid
        for word in words:
            if word in self.ignorewords: 
                continue
            wordid=self.getentryid('wordlist','word',word)
            self.con.execute("insert into linkwords(linkid,wordid) values (%d,%d)" % (linkid,wordid))
        
    
    
    
    
    #从一小组网页开始进行广度优先搜索，直至某一给定深度
    #期间为网页建立索引
    #pages为网页url，depth为深度
    def crawl(self,pages,depth=2):
        for i in range(depth):
            #初始化newpage
            newpages=set()
            for page in pages:
                try:
                    #打开链接
                    c=urllib2.urlopen(page)
                except:
                    #打开失败
                    print "Could not open %s" %page
                    continue
                #BeautifulSoup为一个解析插件，读出网页HTML
                soup=BeautifulSoup(c.read(),"html5lib")
                self.addtoindex(page, soup)
                
                #从网页中提取<a>标签
                links=soup('a')
                for link in links:
                    #检测<a>标签中是否有href属性
                    if('href' in dict(link.attrs)):
                        url=urljoin(page,link['href'])
                        if(url.find("'")!=-1):
                            continue
                        #去除锚？
                        url=url.split('#')[0]
                        #不在已存在的url中则加入
                        if(url[0:4]=='http' and not self.isindexed(url)):
                            newpages.add(url)
                        linkText=self.gettextonly(link)
                        self.addlinkref(page, url, linkText)
                self.dbcommit()
            pages=newpages   
                            
        pass
    #创建数据库表
    def createindextables(self):
        self.con.execute('create table urllist(url)')
        self.con.execute('create table wordlist(word)')
        self.con.execute('create table wordlocation(urlid,wordid,location)')
        self.con.execute('create table link(fromid integer,toid integer)')
        self.con.execute('create table linkwords(wordid,linkid)')
        self.con.execute('create index wordidx on wordlist(word)')
        self.con.execute('create index urlidx on urllist(url)')
        self.con.execute('create index wordurlidx on wordlocation(wordid)')
        self.con.execute('create index urltoidx on link(toid)')
        self.con.execute('create index urlfromidx on link(fromid)')
        self.dbcommit()
        
        
    #pageRank算法，每个网页初始值设为1，通过不断迭代，找出PageRank值，先设定迭代次数为20    
    def calculatePageRank(self,iterations=20):
        #清除pagerank表
        self.con.execute('drop table if exists pagerank')
        self.con.execute('create table pagerank(urlid primary key,score)')
        #初始化每个url，令其pagerank值为1
        self.con.execute('insert into pagerank select rowid,1.0 from urllist')
        self.dbcommit()
        
        for i in range(iterations):
            print "Iteration %d"%(i)
            for (urlid,) in self.con.execute('select rowid from urllist'):
                pr=0.15
                
                #循环遍历指向当前网页的所有其他网页
                for(linker,) in self.con.execute('select distinct fromid from link where toid=%d' % urlid):
                    #得到链接源对应网页的PageRank值
                    linkingPr=self.con.execute('select score from pagerank where urlid=%d'% linker).fetchone()[0]
                    
                    #根据链接源，求总的链接数
                    linkingCount=self.con.execute('select count(*) from link where fromid=%d' % linker).fetchone()[0]
                    pr+=0.85*(linkingPr/linkingCount)
                self.con.execute('update pagerank set score=%f where urlid=%d'%(pr,urlid))
            self.dbcommit()
    