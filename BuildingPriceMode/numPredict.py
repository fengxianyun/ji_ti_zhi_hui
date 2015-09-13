#coding:gbk
'''
Created on 2015年9月12日

@author: fxy
'''
from random import random,randint
import math
from audioop import avg

def wineprice(rating,age):
    #
    
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

