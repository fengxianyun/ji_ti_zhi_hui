#coding:gbk
'''
Created on 2015��9��12��

@author: fxy
'''
import numPredict
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
def knn(d,v):
    return numPredict.weightedknn(d,v,weightf=numPredict.inverseweight)
def knn2(d,v):
    return numPredict.knnestimate(d, v, 3)
#�����ݷ�Ϊѵ�����Ͳ��Լ��������в���
print numPredict.crossvalidate(knn2, data)
print numPredict.crossvalidate(knn, data)

#���������ݼ��������ݼ��а�������Ԫ�������Ԫ��
data2=numPredict.wineset2()
print numPredict.crossvalidate(knn, data2)
print numPredict.crossvalidate(knn2,data2)
#�Զ���Ԫ�ؽ�������
sdata=numPredict.rescale(data2, [1,1,0,0])
print numPredict.crossvalidate(knn, sdata)
print numPredict.crossvalidate(knn2,sdata)
