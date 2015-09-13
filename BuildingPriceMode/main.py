#coding:gbk
'''
Created on 2015年9月12日

@author: fxy
'''
import numPredict
data=numPredict.wineset1()
print data[0]['input']
print data[1]['input']
print numPredict.euclidean(data[0]['input'], data[1]['input'])