#coding:gbk
'''
Created on 2015年7月16日

@author: fxy
'''
from math import sqrt
#返回一个有关person1和person2的基于距离的相似度评价,输入一个字典和字典中的两个人
def sim_distance(prefs,person1,person2):
    #得到share_items的列表
    si={}
    for item in prefs[person1]:
        if item in prefs[person2]:
            si[item]=1
    #如果两者没有共同之处返回0
    if len(si)==0:
        return 0
    #计算所有差值的平方和
    sum_of_squares=sum([pow(prefs[person1][item]-prefs[person2][item], 2)
                        for item in prefs[person1]if item in prefs[person2]])
    return 1/(1+sqrt(sum_of_squares))
