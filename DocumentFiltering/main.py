#coding:gbk
'''
Created on 2015年8月31日

@author: fxy
'''
import docclass
import naivebayes
import fisherClassifier
# cl=docclass.classifier(docclass.getwords)
# docclass.sampletrain(cl)
# #print cl.fprob('quick', 'good')
# print cl.weightedProb('money', 'good', cl.fprob)
# docclass.sampletrain(cl)
# print cl.weightedProb('money', 'good', cl.fprob)

# cl=docclass.naivebayes(docclass.getwords)
# docclass.sampletrain(cl)
# print cl.prob('quick rabbit', 'good')
# print cl.prob('quick rabbit', 'bad')

# cl=naivebayes.naivebayes(docclass.getwords)
# docclass.sampletrain(cl)
# print cl.classify('quick rabbit', defalt='unknow')
# print cl.classify('quick money', defalt='unknow')
# print cl.prob('quick money', 'good')
# print cl.prob('quick money', 'bad')
# cl.setThreshold('bad', 3.0)
# print cl.classify('quick money', defalt='unknow')
# print cl.prob('quick money', 'good')
# print cl.prob('quick money', 'bad')
# for i in range(10):
#     docclass.sampletrain(cl)
# print cl.classify('quick money', defalt='unknow')
# print cl.prob('quick money', 'good')
# print cl.prob('quick money', 'bad')

# cl=fisherClassifier.FisherClassifier(docclass.getwords)
# docclass.sampletrain(cl)
# print cl.cprob('quick', 'good')
# print cl.cprob('money', 'bad')

# cl=fisherClassifier.FisherClassifier(docclass.getwords)    
# docclass.sampletrain(cl)
# print cl.cprob('quick', 'good')
# print cl.fisherprob('quick rabbit', 'good')
# print cl.fisherprob('quick rabbit', 'bad')

# cl=fisherClassifier.FisherClassifier(docclass.getwords)
# docclass.sampletrain(cl)
# print cl.classify('quick rabbit')
# print cl.classify("quick money")
# cl.setminimum('bad', 0.8)
# print cl.classify("quick money")

cl=fisherClassifier.FisherClassifier(docclass.getwords)
cl.setdb("test1.db")
docclass.sampletrain(cl)
cl2=naivebayes.naivebayes(docclass.getwords)
cl2.setdb("test1.db")
print cl2.classify('quick money')