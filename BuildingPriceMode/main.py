#coding:gbk
'''
Created on 2015��9��12��

@author: fxy
'''
import numPredict
import sys
from pylab import *

sys.path.append("..")
from suiJiYouHua.NetworkVisualization import optimization
#�������ݼ�
data=numPredict.wineset1()
# print data[0]['input']
# print data[1]['input']
# #�����������ݵ����ƶ�
# print numPredict.euclidean(data[0]['input'], data[1]['input'])
# #�������ּ���۸�ĺ���
# print numPredict.knnestimate(data, (99.0,5.0))
# print numPredict.weightedknn(data, (99.0,5.0))
# #�������۸�ĺ���
# def knn(d,v):
#     return numPredict.weightedknn(d,v,weightf=numPredict.inverseweight)
# def knn2(d,v):
#     return numPredict.knnestimate(d, v, 3)
# #�����ݷ�Ϊѵ�����Ͳ��Լ��������в���
# print numPredict.crossvalidate(knn2, data)
# print numPredict.crossvalidate(knn, data)
# 
# #���������ݼ��������ݼ��а�������Ԫ�������Ԫ��
# data2=numPredict.wineset2()
# print numPredict.crossvalidate(knn, data2)
# print numPredict.crossvalidate(knn2,data2)
# #�Զ���Ԫ�ؽ�������
# sdata=numPredict.rescale(data2, [10,10,0,1])
# print numPredict.crossvalidate(knn, sdata)
# print numPredict.crossvalidate(knn2,sdata)
# #�Ż����о�Ч�������Ǻܺã�
# costf=numPredict.creatcostfunction(numPredict.knnestimate, sdata)
# print"�Ż���ӡ"
# weight=optimization.geneticoptimize(numPredict.weightdomain, costf, maxiter=10)
# print weight
# sdata=numPredict.rescale(data2, weight)
# print numPredict.crossvalidate(knn, sdata)
# print numPredict.crossvalidate(knn2,sdata)

#����Ȩ��
print numPredict.probguess(data, [99,20], 0, 100)
print numPredict.probguess(data, [99,20], 100, 200)

#���Ƹ��ʷֲ�
numPredict.cumulativegraph(data, (1,1), 120,k=5)
numPredict.probabilitygrah(data, (1,1), 120,k=5)