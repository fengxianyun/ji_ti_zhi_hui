#coding:gbk
'''
Created on 2015年9月24日

@author: fxy
'''
from MatcthRow import MatchRow
from audioop import avg

def loadMatch(f,allnum):
    #构造MatchRow类的列表
    
    rows=[]
    for line in file(f):
        rows.append(MatchRow(line.split(','),allnum))
    return rows

def linearTrain(rows):
    #计算均值点
    
    averages={}
    counts={}
    
    for row in rows:
        
        #得到改点坐标所属分类
        cl=row.match
        
        averages.setdefault(cl,[0.0]*len(row.data))
        counts.setdefault(cl,0)
        
        #将该坐标点加入averages中
        for i in range(len(row.data)):
            averages[cl][i]+=float(row.data[i])
        
        #记录每个分类中有多少点
        counts[cl]+=1
    
    #求平均值
    for cl,avg in averages.items():
        for i in range(len(avg)):
            avg[i]/=counts[i]
    
    return averages 


def dotProduct(v1,v2):
    #计算点积，降低一个向量中的每个值和第二个向量中的对应值相乘
    return sum([v1[i]*v2[i] for i in range(len(v1))])

