#coding:gbk
'''
Created on 2015��9��12��

@author: fxy
'''
from random import random,randint
import math
from audioop import avg

def wineprice(rating,age):
    #
    
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

