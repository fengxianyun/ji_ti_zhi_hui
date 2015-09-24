#coding:gbk
'''
Created on 2015年9月12日

@author: fxy
'''
from random import random,randint
import math
from pylab import *

weightdomain=[(0,20)]*4

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
        #通道信息（多余）
        aise=float(randint(1,20))
        #瓶子大小
        bottlesize=[375.0,750.0,1500.0,3000.0][randint(0,3)]
        price=wineprice(rating, age)
        price*=(bottlesize/750)
        price*=(random()*0.4+0.8)
        rows.append({'input':(rating,age,aise,bottlesize),'result':price})
    return rows

def wineset3():
    #创造不对称分布的数据
    
    rows=wineset1()
    for row in rows:
        if random()<0.5:
            #葡萄酒是从折扣店购得
            row['result']*=0.5
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

def gaussian(dist,sigma=10.0):
    #为近邻分配权重
    #高斯函数
    return math.e**(-dist**2/(2*sigma**2))

def weightedknn(data,vec1,k=5,weightf=gaussian):
    
    
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

def creatcostfunction(algf,data):
    def costf(scale):
        sdata=rescale(data, scale)
        return crossvalidate(algf, data, trials=10)
    return  costf
    
def probguess(data,vec1,low,high,k=5,weightf=gaussian):
    #计算范围内的权重值
    #data数据集
    #vec中心点
    #low范围最小值
    #high范围最大值
    #k取中心点附近点的个数
    #计算权值的方法
    
    dlist=getdistances(data, vec1)
    nweight=0.0
    tweight=0.0
    for i in range(k):
        dist=dlist[i][0]
        idx=dlist[i][1]
        weight=weightf(dist)
        v=data[idx]['result']
        
        #当前数据位于指定范围吗
        if v>=low and v<=high:
            nweight+=weight
        tweight+=weight
    if tweight==0:
        return 0
    return nweight/tweight

def cumulativegraph(data,vec1,high,k=5,weightf=gaussian):
    #绘制递增式的概率分布图
    #data数据集
    #vec中心点
    #high范围最大值
    #k取中心点附近点的个数
    #计算权值的方法
    
    t1=arange(0.0,high,0.1)
    cprob=array([probguess(data, vec1, 0, v, k, weightf) for v in t1])
    plot(t1,cprob)
    show()

def probabilitygrah(data,vec1,high,k=5,weightf=gaussian,ss=5.0):
    #绘制高斯式的概率分布图
    #data数据集
    #vec中心点
    #high范围最大值
    #k取中心点附近点的个数
    #计算权值的方法
    
    #建立一个代表价格的值域范围
    t1=arange(0.0,high,0.1)
    
    #得到整个概率范围内所有概率
    probs=[probguess(data, vec1, v, v+0.1, k, weightf) for v in t1]
    
    #通过加上近邻的高斯计算结果，对概率做平滑处理
    smoothed=[]
    for i in range(len(probs)):
        sv=0.0
        for j in range(0,len(probs)):
            dist=abs(i-j)*0.1
            weight=gaussian(dist, sigma=ss)
            sv+=weight*probs[j]
        smoothed.append(sv)
    smoothed=array(smoothed)
    
    plot(t1,smoothed)
    plot(t1,array(probs))
    show()
            
            
