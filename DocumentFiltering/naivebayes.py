#coding:gbk
'''
Created on 2015��9��2��

@author: fxy
'''
#���ر�Ҷ˹������
import docclass
class naivebayes(docclass.classifier):
    def docprob(self,item,category):
        features=self.getfeatures(item)
        
        #�����������ĸ������
        p=1.0
        for feature in features:
            p*=self.weightedProb(feature, category, self.fprob)
        return p
    
    #����p(category|feature*feature��������)
    def prob(self,item,category):
        catprob=self.catcount(category)/self.totalcount()
        docprob=self.docprob(item, category)
        return docprob*catprob
    
    
    def classify(self,item,defalt=None):
        probs={}
        #Ѱ�Ҹ������ķ���
        max=0.0
        for category in self.categories():
            probs[category]=self.prob(item, category)
            if probs[category]>max:
                max=probs[category]
                best=category
        #ȷ������ֵ������ֵ*�δ����ֵ
        for category in probs:
            if category==best:
                continue
            if probs[category]*self.getThreshold(best)>probs[best]:
                return defalt
        return best