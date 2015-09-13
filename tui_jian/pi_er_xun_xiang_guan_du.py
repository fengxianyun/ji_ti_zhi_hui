#coding:gbk
'''
Created on 2015年7月16日

@author: fxy
'''
#返回p1和p2的皮尔逊相关系数
from math import sqrt
def sim_pearson(prefs,p1,p2):
    #得到双方都曾评价过的物品列表
    si={}
    for item in prefs[p1]:
        if item in prefs[p2]:
            si[item]=1
    #得到列表元素个数
    n=len(si)
    if n==0:
        return 1
    #对所有偏好求和
    sum1=sum([prefs[p1][it] for it in si])
    sum2=sum([prefs[p2][it] for it in si])
    #求平方和
    sum1Sq=sum([pow(prefs[p1][it], 2)for it in si])
    sum2Sq=sum([pow(prefs[p2][it], 2)for it in si])
    #求乘积之和
    pSum=sum([prefs[p1][it]*prefs[p2][it] for it in si])
    #计算皮尔逊评价值
    num=pSum-(sum1*sum2/n)
    den=sqrt((sum1Sq-pow(sum1, 2)/n)*(sum2Sq-pow(sum2, 2)/n))
    if den==0:
        return 0
    r=num/den
    return r
