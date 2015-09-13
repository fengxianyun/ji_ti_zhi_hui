#coding:gbk
'''
Created on 2015年9月2日

@author: fxy
'''
#朴素贝叶斯分类器
import docclass
class naivebayes(docclass.classifier):
    def docprob(self,item,category):
        features=self.getfeatures(item)
        
        #将所有特征的概率相乘
        p=1.0
        for feature in features:
            p*=self.weightedProb(feature, category, self.fprob)
        return p
    
    #计算p(category|feature*feature…………)
    def prob(self,item,category):
        catprob=self.catcount(category)/self.totalcount()
        docprob=self.docprob(item, category)
        return docprob*catprob
    
    
    def classify(self,item,defalt=None):
        probs={}
        #寻找概率最大的分类
        max=0.0
        for category in self.categories():
            probs[category]=self.prob(item, category)
            if probs[category]>max:
                max=probs[category]
                best=category
        #确保概率值超出阈值*次大概率值
        for category in probs:
            if category==best:
                continue
            if probs[category]*self.getThreshold(best)>probs[best]:
                return defalt
        return best