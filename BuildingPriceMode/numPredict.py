#coding:gbk
'''
Created on 2015年9月12日

@author: fxy
'''
from random import random,randint
import math
from audioop import avg

def wineprice(rating,age):
    #输入等级和年代
    
    peak_age=rating-50
    
    #根据等级来计算价格
    price=rating/2
    if age>peak_age:
        #经过峰值年,后继五年里其品质将会变差
        price=price*(5-(age-peak_age))
    else:
        #价格在接近峰值时会增加到原值的五倍
        price=price*(5*(age+1)/peak_age)
    if price<0:
        price=0
    return price


def wineset1():
    #随机生成300瓶酒的价值
    rows=[]
    for i in range(300):
        #随机生成年代和等级
        rating=random()*50+50
        age=random()*50
        
        #得到一个参考价格
        price=wineprice(rating, age)
        
        #增加噪声
        price*=(random()*0.4+0.8)
        
        #加入数据集
        rows.append({'input':(rating,age),'result':price})
    return rows

def wineset2():
    #随机生成300瓶酒的价值
    
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
    #定义相似度
    d=0.0
    for i in range(len(v1)):
        d+=(v1[i]-v2[i])**2
    return math.sqrt(d)

def getdistances(data,vec1):
    #算出距离列表，并求平均值
    distance_list=[]
    for i in range(len(data)):
        vec2=data[i]['input']
        distance_list.append((euclidean(vec1, vec2),i))
    distance_list.sort(cmp=None, key=None, reverse=False)
    return distance_list

def knnestimate(data,vec1,k=5):
    #对前k项取平均值m，算出价格
    
    #得到经过排序的距离值
    dlist=getdistances(data, vec1)
    avg=0.0
    
    #对前k项结果求平均
    for i in range(k):
        idx=dlist[i][1]
        avg+=data[idx]['result']
    avg=avg/k
    return avg

def inverseweight(dist,num=1.0,const=1.0):
    #为近邻分配权重
    #反函数
    return num/(dist+const)

def subtractweight(dist,const=1.0):
    #为近邻分配权重
    #一次函数，递减
    if dist>const:
        return 0
    else:
        return const-dist

def gussian(dist,sigma=10.0):
    #为近邻分配权重
    #高斯函数
    return math.e**(-dist**2/(2*sigma**2))

def weightedknn(data,vec1,k=5,weightf=gussian):
    
    
    #得到距离值
    dlist=getdistances(data, vec1)
    avg=0.0
    totalweight=0.0
    
    #得到加权平均值
    for i in range(k):
        dist=dlist[i][0]
        idx=dlist[i][1]
        weight=weightf(dist)
        avg+=weight*data[idx]['result']
        totalweight+=weight
    avg=avg/totalweight
    return avg

def dividedata(data,test=0.05):
    #拆分数据为训练集，和测试集
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
    #测试算法好坏
    error=0.0
    for row in testset:
        guess=algf(trainset,row['input'])
        error+=(row['result']-guess)**2
    return error/len(testset)

def crossvalidate(algf,data,trials=100,test=0.05):
    #交叉验证
    #经过多次计算，算出算法好坏
    
    error=0.0
    for i in range(trials):
        trainset,testset=dividedata(data, test)
        error+=testalgorithm(algf, trainset, testset)
    return error/trials
    
    
def rescale(data,scale):
    #按比例缩放
    #对元素进行缩放，使其影响改变（减少没用元素权值）
    
    scaleddate=[]
    for row in data:
        scaled=[scale[i]*row['input'][i] for i in range(len(scale))]
        scaleddate.append({'input':scaled,'result':row['result']})
    return scaleddate
    
    

