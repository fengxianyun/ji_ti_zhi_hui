#coding:gbk
'''
Created on 2015年9月24日

@author: fxy
'''
import advancedClassify
import draw
agesonly=advancedClassify.loadMatch('agesonly.csv', allnum=True)

#画出成功率，年龄分布规律
draw.plotAgeMatches(agesonly)
avgs=advancedClassify.linearTrain(agesonly)
