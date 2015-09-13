#coding:gbk
import sys
reload(sys)
'''

@author: fxy
'''
#��url�Ŀ�
import urllib2
#�������ݿ�
from pysqlite2 import dbapi2 as sqlite
#����html
from bs4 import *
from urlparse import urljoin
from html5lib import *

import re

import jieba
#����ԭ��
#��һС����ҳ��ʼ���й������������ֱ��ĳһ�������
#�ڼ�Ϊ��ҳ��������
    #������ҳHTML
    #Ϊÿ����ҳ��������
        #��html��ҳ����ȡ����
        #�ִ�
        #��ÿ��������url��أ�������ҳ���ֵĵ��ʣ��뱾��url�йأ�
    #����ҳ����ȡ<a>��ǩ
    #���<a>��ǩ���Ƿ���href����
    #�����Ѵ��ڵ�url�������
    #���һ������������ҳ������
    #��ͷ��ʼ
#pagerank



class crawler():
    '''
    classdocs
    '''

    def __init__(self, dbname):
        self.con=sqlite.connect(dbname)
        self.ignorewords=set(['��','��','��','��','\'',',','��','~','!','@','#','$','%','^','&','*','(',')','-','+','_','=','[',']','{','}','/','?','<','>','"'])
    def __del__(self):
        self.con.close()
    def dbcommit(self):
        self.con.commit()
    
    
    #�������������ڻ�ȡ��Ŀ��id��������Ŀ�����ڣ��ͽ���������ݿ�
    def getentryid(self,table,field,value,createnew=True):
        cur=self.con.execute("select rowid from %s where %s='%s'" %(table,field,value))
        res=cur.fetchone()
        if res==None:
            cur=self.con.execute("insert into %s (%s) values ('%s')" %(table,field,value))
            return cur.lastrowid
        else:
            return res[0]
    
    
    
    #Ϊÿ����ҳ��������
    def addtoindex(self,url,soup):
        if self.isindexed(url):
            return
        print 'Indexing '+url
        #��ȡÿ������
        text=self.gettextonly(soup)
        print text
        #�ִ�
        words=self.separatewords(text)
        #�õ�url��id
        urlid=self.getentryid('urllist', 'url', url)
        #��ÿ��������url���
        for i in range(len(words)):
            word=words[i]
            if word in self.ignorewords:
                continue
            wordid=self.getentryid('wordlist', 'word',word)
            self.con.execute("insert into wordlocation (urlid,wordid,location)\
            values(%d,%d,%d)"%(urlid,wordid,i))
    
    
    #��html��ҳ����ȡ���֣�������ǩ�����ݹ����
    #�����
    def gettextonly(self,soup):
        #���岻��
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
    
    
    
    #���ݷǿհ��ַ����зִʴ���
    def separatewords(self,text):
        splitter=jieba.cut(text)
        return[word for word in splitter if word!=" " and word!='\n']
    
    
    
    
    #���url�ѽ������������򷵻�true
    def isindexed(self,url):
        u=self.con.execute \
        ("select rowid from urllist where url='%s'" % url).fetchone()
        if u !=None:
            v=self.con.execute('select * from wordlocation where urlid=%d' %u[0]).fetchone()
            if v!=None:
                return True
        return False
    
    
    
    #���һ������������ҳ������
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
        
    
    
    
    
    #��һС����ҳ��ʼ���й������������ֱ��ĳһ�������
    #�ڼ�Ϊ��ҳ��������
    #pagesΪ��ҳurl��depthΪ���
    def crawl(self,pages,depth=2):
        for i in range(depth):
            #��ʼ��newpage
            newpages=set()
            for page in pages:
                try:
                    #������
                    c=urllib2.urlopen(page)
                except:
                    #��ʧ��
                    print "Could not open %s" %page
                    continue
                #BeautifulSoupΪһ�����������������ҳHTML
                soup=BeautifulSoup(c.read(),"html5lib")
                self.addtoindex(page, soup)
                
                #����ҳ����ȡ<a>��ǩ
                links=soup('a')
                for link in links:
                    #���<a>��ǩ���Ƿ���href����
                    if('href' in dict(link.attrs)):
                        url=urljoin(page,link['href'])
                        if(url.find("'")!=-1):
                            continue
                        #ȥ��ê��
                        url=url.split('#')[0]
                        #�����Ѵ��ڵ�url�������
                        if(url[0:4]=='http' and not self.isindexed(url)):
                            newpages.add(url)
                        linkText=self.gettextonly(link)
                        self.addlinkref(page, url, linkText)
                self.dbcommit()
            pages=newpages   
                            
        pass
    #�������ݿ��
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
        
        
    #pageRank�㷨��ÿ����ҳ��ʼֵ��Ϊ1��ͨ�����ϵ������ҳ�PageRankֵ�����趨��������Ϊ20    
    def calculatePageRank(self,iterations=20):
        #���pagerank��
        self.con.execute('drop table if exists pagerank')
        self.con.execute('create table pagerank(urlid primary key,score)')
        #��ʼ��ÿ��url������pagerankֵΪ1
        self.con.execute('insert into pagerank select rowid,1.0 from urllist')
        self.dbcommit()
        
        for i in range(iterations):
            print "Iteration %d"%(i)
            for (urlid,) in self.con.execute('select rowid from urllist'):
                pr=0.15
                
                #ѭ������ָ��ǰ��ҳ������������ҳ
                for(linker,) in self.con.execute('select distinct fromid from link where toid=%d' % urlid):
                    #�õ�����Դ��Ӧ��ҳ��PageRankֵ
                    linkingPr=self.con.execute('select score from pagerank where urlid=%d'% linker).fetchone()[0]
                    
                    #��������Դ�����ܵ�������
                    linkingCount=self.con.execute('select count(*) from link where fromid=%d' % linker).fetchone()[0]
                    pr+=0.85*(linkingPr/linkingCount)
                self.con.execute('update pagerank set score=%f where urlid=%d'%(pr,urlid))
            self.dbcommit()
    