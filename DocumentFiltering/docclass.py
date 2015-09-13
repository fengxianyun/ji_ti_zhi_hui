#coding:gbk
'''
Created on 2015年8月31日

@author: fxy
'''

import re
import math
from pysqlite2 import  dbapi2 as sqlite

def getwords(doc):
    splitter=re.compile(' ')
    #根据字母字符进行单词拆分
    words=[s.lower()for s in splitter.split(doc)
           if len(s)>2 and len(s)<20]
    
    #只返回一组不重复单词
    return dict([(w,1)for w in words])


def sampletrain(cl):
    cl.train('Nobody owns the water.','good')
    cl.train('the quick rabbit jumps fences','good')
    cl.train('buy pharmaceuticals now','bad')
    cl.train('make quick money at the online casino','bad')
    cl.train('the quick brown fox jumps','good')


class classifier:
    #getfeatures代表提取特征的函数
    def __init__(self,getfeatures,filename=None):
        #统计特征/分类组合的数量
        self.feature_dictionary={}
        #统计每个分类中文档的数量
        self.category_dictionary={}
        self.thresholds={}
        self.getfeatures=getfeatures
        
        
    #增加特征/分类组合的计数值
    def incfeature(self,feature,category):
        count=self.fcount(feature, category)
        if count==0:
            self.con.execute("insert into fc values('%s','%s',1)"%(feature,category))
        else:
            self.con.execute("update fc set count=%d where feature='%s'\
            and category='%s'"%(count+1,feature,category))
        
    #增加对于某一分类的计数
    def incc(self,category):
        count=self.catcount(category)
        if count==0:
            self.con.execute("insert into cc values('%s',1)"%(category))
        else:
            self.con.execute("update cc set count=%d where category='%s'"
                             %(count+1,category))
        
    #某一特征出现于某一分类中的次数
    def fcount(self,feature,category):
        res=self.con.execute('select count from fc where feature="%s" and category="%s"'
                             %(feature,category)).fetchone()
        if res==None:
            return 0
        else:
            return float(res[0])
    
    #属于某一分类的内容项数量
    def catcount(self,category):
        res=self.con.execute("select count from cc where category='%s'"%(category)).fetchone()
        if res==None:
            return 0
        else:
            return float(res[0])
    
    #所有内容项数量
    def totalcount(self):
        res=self.con.execute("select sum(count) from cc").fetchone()
        if res==None:
            return 0
        return res[0]
    
    #所有分类列表
    def categories(self):
        cur=self.con.execute("select category from cc")
        return[d[0] for d in cur]
    
    def train(self,item,category):
        features=self.getfeatures(item)
        #针对该分类增加计数值
        for feature in features:
            self.incfeature(feature, category)
        #增加对该分类的计数
        self.incc(category)
        self.con.commit()
            
    def fprob(self,feature,category):
        #特征在某分类中的个数，除以某分类总数  p(feature|category)    
        
        if self.catcount(category)==0:
            return 0
        #特征在分类中出现的总次数，除以分类中包含内容项的总数
        return self.fcount(feature, category)/self.catcount(category)
    
    def weightedProb(self,feature,category,prf,weight=1.0,ap=0.5):
        #计算当前概率(某分类中特征出现的概率)
        basicprob=prf(feature,category)
        
        #统计特征在所有分类中出现的次数
        totals=sum([self.fcount(feature, c) for c in self.categories()])
        
        #计算加权平均(计算)
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
        
            