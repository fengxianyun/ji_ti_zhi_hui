#coding:gbk
'''
Created on 2015��9��2��

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
        #ѭ��������Ѱ����ѽ��
        
        best=default
        max=0.0
        for c in self.categories():
            p=self.fisherprob(item, c)
            #ȷ���䳬������ֵ
            if p>self.getminimum(c) and p>max:
                best=c
                max=p
        return best
        
        
    def cprob(self,feature,category):
        #
        
        #�����ڸ÷����г��ֵ�Ƶ��
        clf=self.fprob(feature, category)
        if clf==0:
            return 0
        
        #���������з����г��ֵ�Ƶ��
        frequsum=sum([self.fprob(feature, c)for c in self.categories()])
        
        #���ʵ��������ڸ÷����е�Ƶ�ʳ�����Ƶ��
        p=clf/(frequsum)
        
        return p
    def fisherprob(self,item,category):
        #�����и���ֵ���
        
        p=1
        features=self.getfeatures(item)
        for f in features:
            p*=(self.weightedProb(f, category, self.cprob))
        
        #ȡ��Ȼ������������-2
        fscore=-2*math.log(p)
        
        #���õ��ö����������������
        return self.invchi2(fscore, len(features)*2)
    
    def invchi2(self,chi,df):
        m=chi/2.0
        sum=term=math.exp(-m)
        for i in range(1,df//2):
            term*=m/i
            sum+=term
        return min(sum,1.0)
    