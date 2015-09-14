#coding:gbk
'''
Created on 2015��9��12��

@author: fxy
'''
from random import random,randint
import math
from audioop import avg

def wineprice(rating,age):
    #����ȼ������
    
    peak_age=rating-50
    
    #���ݵȼ�������۸�
    price=rating/2
    if age>peak_age:
        #������ֵ��,�����������Ʒ�ʽ�����
        price=price*(5-(age-peak_age))
    else:
        #�۸��ڽӽ���ֵʱ�����ӵ�ԭֵ���屶
        price=price*(5*(age+1)/peak_age)
    if price<0:
        price=0
    return price


def wineset1():
    #�������300ƿ�Ƶļ�ֵ
    rows=[]
    for i in range(300):
        #�����������͵ȼ�
        rating=random()*50+50
        age=random()*50
        
        #�õ�һ���ο��۸�
        price=wineprice(rating, age)
        
        #��������
        price*=(random()*0.4+0.8)
        
        #�������ݼ�
        rows.append({'input':(rating,age),'result':price})
    return rows

def wineset2():
    #�������300ƿ�Ƶļ�ֵ
    
    rows=[]
    for i in range(300):
        rating=random()*50+50
        age=random()*50
        aise=float(randint(1,20))
        bottlesize=[375.0,750.0,1500.0,3000.0][randint(0,3)]
        price=wineprice(rating, age)
        price*=(bottlesize/750)
        price*=(random()*0.9+0.2)
        rows.append({'input':(rating,age,aise,bottlesize),'result':price})
    return rows


def euclidean(v1,v2):
    #�������ƶ�
    d=0.0
    for i in range(len(v1)):
        d+=(v1[i]-v2[i])**2
    return math.sqrt(d)

def getdistances(data,vec1):
    #��������б�����ƽ��ֵ
    distance_list=[]
    for i in range(len(data)):
        vec2=data[i]['input']
        distance_list.append((euclidean(vec1, vec2),i))
    distance_list.sort(cmp=None, key=None, reverse=False)
    return distance_list

def knnestimate(data,vec1,k=5):
    #��ǰk��ȡƽ��ֵm������۸�
    
    #�õ���������ľ���ֵ
    dlist=getdistances(data, vec1)
    avg=0.0
    
    #��ǰk������ƽ��
    for i in range(k):
        idx=dlist[i][1]
        avg+=data[idx]['result']
    avg=avg/k
    return avg

def inverseweight(dist,num=1.0,const=1.0):
    #Ϊ���ڷ���Ȩ��
    #������
    return num/(dist+const)

def subtractweight(dist,const=1.0):
    #Ϊ���ڷ���Ȩ��
    #һ�κ������ݼ�
    if dist>const:
        return 0
    else:
        return const-dist

def gussian(dist,sigma=10.0):
    #Ϊ���ڷ���Ȩ��
    #��˹����
    return math.e**(-dist**2/(2*sigma**2))

def weightedknn(data,vec1,k=5,weightf=gussian):
    
    
    #�õ�����ֵ
    dlist=getdistances(data, vec1)
    avg=0.0
    totalweight=0.0
    
    #�õ���Ȩƽ��ֵ
    for i in range(k):
        dist=dlist[i][0]
        idx=dlist[i][1]
        weight=weightf(dist)
        avg+=weight*data[idx]['result']
        totalweight+=weight
    avg=avg/totalweight
    return avg

def dividedata(data,test=0.05):
    #�������Ϊѵ�������Ͳ��Լ�
    trainset=[]
    testset=[]
    for row in data:
        r=random()
        if r<test:
            testset.append(row)
        else:
            trainset.append(row)
    return trainset,testset

def testalgorithm(algf,trainset,testset):
    #�����㷨�û�
    error=0.0
    for row in testset:
        guess=algf(trainset,row['input'])
        error+=(row['result']-guess)**2
    return error/len(testset)

def crossvalidate(algf,data,trials=100,test=0.05):
    #������֤
    #������μ��㣬����㷨�û�
    
    error=0.0
    for i in range(trials):
        trainset,testset=dividedata(data, test)
        error+=testalgorithm(algf, trainset, testset)
    return error/trials
    
    
def rescale(data,scale):
    #����������
    #��Ԫ�ؽ������ţ�ʹ��Ӱ��ı䣨����û��Ԫ��Ȩֵ��
    
    scaleddate=[]
    for row in data:
        scaled=[scale[i]*row['input'][i] for i in range(len(scale))]
        scaleddate.append({'input':scaled,'result':row['result']})
    return scaleddate
    
    

