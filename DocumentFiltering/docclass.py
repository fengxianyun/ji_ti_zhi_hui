#coding:gbk
'''
Created on 2015��8��31��

@author: fxy
'''

import re
import math
from pysqlite2 import  dbapi2 as sqlite

def getwords(doc):
    splitter=re.compile(' ')
    #������ĸ�ַ����е��ʲ��
    words=[s.lower()for s in splitter.split(doc)
           if len(s)>2 and len(s)<20]
    
    #ֻ����һ�鲻�ظ�����
    return dict([(w,1)for w in words])


def sampletrain(cl):
    cl.train('Nobody owns the water.','good')
    cl.train('the quick rabbit jumps fences','good')
    cl.train('buy pharmaceuticals now','bad')
    cl.train('make quick money at the online casino','bad')
    cl.train('the quick brown fox jumps','good')


class classifier:
    #getfeatures������ȡ�����ĺ���
    def __init__(self,getfeatures,filename=None):
        #ͳ������/������ϵ�����
        self.feature_dictionary={}
        #ͳ��ÿ���������ĵ�������
        self.category_dictionary={}
        self.thresholds={}
        self.getfeatures=getfeatures
        
        
    #��������/������ϵļ���ֵ
    def incfeature(self,feature,category):
        count=self.fcount(feature, category)
        if count==0:
            self.con.execute("insert into fc values('%s','%s',1)"%(feature,category))
        else:
            self.con.execute("update fc set count=%d where feature='%s'\
            and category='%s'"%(count+1,feature,category))
        
    #���Ӷ���ĳһ����ļ���
    def incc(self,category):
        count=self.catcount(category)
        if count==0:
            self.con.execute("insert into cc values('%s',1)"%(category))
        else:
            self.con.execute("update cc set count=%d where category='%s'"
                             %(count+1,category))
        
    #ĳһ����������ĳһ�����еĴ���
    def fcount(self,feature,category):
        res=self.con.execute('select count from fc where feature="%s" and category="%s"'
                             %(feature,category)).fetchone()
        if res==None:
            return 0
        else:
            return float(res[0])
    
    #����ĳһ���������������
    def catcount(self,category):
        res=self.con.execute("select count from cc where category='%s'"%(category)).fetchone()
        if res==None:
            return 0
        else:
            return float(res[0])
    
    #��������������
    def totalcount(self):
        res=self.con.execute("select sum(count) from cc").fetchone()
        if res==None:
            return 0
        return res[0]
    
    #���з����б�
    def categories(self):
        cur=self.con.execute("select category from cc")
        return[d[0] for d in cur]
    
    def train(self,item,category):
        features=self.getfeatures(item)
        #��Ը÷������Ӽ���ֵ
        for feature in features:
            self.incfeature(feature, category)
        #���ӶԸ÷���ļ���
        self.incc(category)
        self.con.commit()
            
    def fprob(self,feature,category):
        #������ĳ�����еĸ���������ĳ��������  p(feature|category)    
        
        if self.catcount(category)==0:
            return 0
        #�����ڷ����г��ֵ��ܴ��������Է����а��������������
        return self.fcount(feature, category)/self.catcount(category)
    
    def weightedProb(self,feature,category,prf,weight=1.0,ap=0.5):
        #���㵱ǰ����(ĳ�������������ֵĸ���)
        basicprob=prf(feature,category)
        
        #ͳ�����������з����г��ֵĴ���
        totals=sum([self.fcount(feature, c) for c in self.categories()])
        
        #�����Ȩƽ��(����)
        bp=((weight*ap)+(basicprob*totals))/(weight+totals)
        return bp
    
    def setThreshold(self,category,t):
        self.thresholds[category]=t

    def getThreshold(self,category):
        if category not in self.thresholds:
            return 1.0
        return self.thresholds[category]
    
    def setdb(self,dbfile):
        self.con=sqlite.connect(dbfile)
        self.con.execute('create table if not exists fc(feature,category,count)')
        self.con.execute('create table if not exists cc(category,count)')
        
            