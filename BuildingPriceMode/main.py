#coding:gbk
'''
Created on 2015年9月12日

@author: fxy
'''
import numPredict
import sys
from pylab import *

sys.path.append("..")
from suiJiYouHua.NetworkVisualization import optimization
#构造数据集
data=numPredict.wineset1()
# print data[0]['input']
# print data[1]['input']
# #测试两个数据的相似度
# print numPredict.euclidean(data[0]['input'], data[1]['input'])
# #测试两种计算价格的函数
# print numPredict.knnestimate(data, (99.0,5.0))
# print numPredict.weightedknn(data, (99.0,5.0))
# #构造计算价格的函数
# def knn(d,v):
#     return numPredict.weightedknn(d,v,weightf=numPredict.inverseweight)
# def knn2(d,v):
#     return numPredict.knnestimate(d, v, 3)
# #将数据分为训练集和测试集，并进行测试
# print numPredict.crossvalidate(knn2, data)
# print numPredict.crossvalidate(knn, data)
# 
# #构造新数据集，此数据集中包含多余元素与干扰元素
# data2=numPredict.wineset2()
# print numPredict.crossvalidate(knn, data2)
# print numPredict.crossvalidate(knn2,data2)
# #对多余元素进行缩放
# sdata=numPredict.rescale(data2, [10,10,0,1])
# print numPredict.crossvalidate(knn, sdata)
# print numPredict.crossvalidate(knn2,sdata)
# #优化（感觉效果并不是很好）
# costf=numPredict.creatcostfunction(numPredict.knnestimate, sdata)
# print"优化打印"
# weight=optimization.geneticoptimize(numPredict.weightdomain, costf, maxiter=10)
# print weight
# sdata=numPredict.rescale(data2, weight)
# print numPredict.crossvalidate(knn, sdata)
# print numPredict.crossvalidate(knn2,sdata)

#测试权重
print numPredict.probguess(data, [99,20], 0, 100)
print numPredict.probguess(data, [99,20], 100, 200)

#绘制概率分布
numPredict.cumulativegraph(data, (1,1), 120,k=5)
numPredict.probabilitygrah(data, (1,1), 120,k=5)