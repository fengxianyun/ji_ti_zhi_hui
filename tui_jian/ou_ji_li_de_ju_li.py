#coding:gbk
'''
Created on 2015��7��16��

@author: fxy
'''
from math import sqrt
#����һ���й�person1��person2�Ļ��ھ�������ƶ�����,����һ���ֵ���ֵ��е�������
def sim_distance(prefs,person1,person2):
    #�õ�share_items���б�
    si={}
    for item in prefs[person1]:
        if item in prefs[person2]:
            si[item]=1
    #�������û�й�֮ͬ������0
    if len(si)==0:
        return 0
    #�������в�ֵ��ƽ����
    sum_of_squares=sum([pow(prefs[person1][item]-prefs[person2][item], 2)
                        for item in prefs[person1]if item in prefs[person2]])
    return 1/(1+sqrt(sum_of_squares))
