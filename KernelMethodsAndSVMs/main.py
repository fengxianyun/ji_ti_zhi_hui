#coding:gbk
'''
Created on 2015��9��24��

@author: fxy
'''
import advancedClassify
import draw
agesonly=advancedClassify.loadMatch('agesonly.csv', allnum=True)

#�����ɹ��ʣ�����ֲ�����
draw.plotAgeMatches(agesonly)
avgs=advancedClassify.linearTrain(agesonly)
