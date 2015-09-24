#coding:gbk
'''
Created on 2015��9��24��

@author: fxy
'''
from MatcthRow import MatchRow
from audioop import avg

def loadMatch(f,allnum):
    #����MatchRow����б�
    
    rows=[]
    for line in file(f):
        rows.append(MatchRow(line.split(','),allnum))
    return rows

def linearTrain(rows):
    #�����ֵ��
    
    averages={}
    counts={}
    
    for row in rows:
        
        #�õ��ĵ�������������
        cl=row.match
        
        averages.setdefault(cl,[0.0]*len(row.data))
        counts.setdefault(cl,0)
        
        #������������averages��
        for i in range(len(row.data)):
            averages[cl][i]+=float(row.data[i])
        
        #��¼ÿ���������ж��ٵ�
        counts[cl]+=1
    
    #��ƽ��ֵ
    for cl,avg in averages.items():
        for i in range(len(avg)):
            avg[i]/=counts[i]
    
    return averages 


def dotProduct(v1,v2):
    #������������һ�������е�ÿ��ֵ�͵ڶ��������еĶ�Ӧֵ���
    return sum([v1[i]*v2[i] for i in range(len(v1))])

