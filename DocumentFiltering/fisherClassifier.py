#coding:gbk
'''
Created on 2015年9月2日

@author: fxy
'''

import docclass
import math
from pysqlite2 import  dbapi2 as sqlite

class FisherClassifier(docclass.classifier):
    '''
    classdocs
    '''
    def __init__(self,getfeatures):
        docclass.classifier.__init__(self,getfeatures)
        self.minimums={}
    
    def getminimum(self,cat):
        if cat not in self.minimums:
            return 0
        return self.minimums[cat]
    
    def setminimum(self,cat,min):
        self.minimums[cat]=min
        
    def classify(self,item,default=None):
        #循环遍历并寻找最佳结果
        
        best=default
        max=0.0
        for c in self.categories():
            p=self.fisherprob(item, c)
            #确保其超过下限值
            if p>self.getminimum(c) and p>max:
                best=c
                max=p
        return best
        
        
    def cprob(self,feature,category):
        #
        
        #特征在该分类中出现的频率
        clf=self.fprob(feature, category)
        if clf==0:
            return 0
        
        #特征在所有分类中出现的频率
        frequsum=sum([self.fprob(feature, c)for c in self.categories()])
        
        #概率等于特征在该分类中的频率除以总频率
        p=clf/(frequsum)
        
        return p
    def fisherprob(self,item,category):
        #将所有概率值相乘
        
        p=1
        features=self.getfeatures(item)
        for f in features:
            p*=(self.weightedProb(f, category, self.cprob))
        
        #取自然对数，并乘以-2
        fscore=-2*math.log(p)
        
        #利用倒置对数卡方函数求概率
        return self.invchi2(fscore, len(features)*2)
    
    def invchi2(self,chi,df):
        m=chi/2.0
        sum=term=math.exp(-m)
        for i in range(1,df//2):
            term*=m/i
            sum+=term
        return min(sum,1.0)
    