#coding:gbk
'''
Created on 2015��7��16��

@author: fxy
'''
#�ӷ�Ӧƫ�õ��ֵ��з�����Ϊƥ����
#���ؽ���ĸ��������ƶȺ���������Ϊ����
from ou_ji_li_de_ju_li import sim_distance
from pi_er_xun_xiang_guan_du import sim_pearson
def topMatches(prefs,person,n=5,similarity=sim_pearson):
    scores=[(similarity(prefs,person,other) ,other )
            for other in prefs if other!=person]
    #���б��������
    scores.sort();
    scores.reverse();
    return scores[0:n]

#�������������˵�����ֵ��Ȩƽ�����ṩ����
def getRecommendations(prefs,person,similarity=sim_distance):
    totals={}
    simSums={}
    for other in prefs:
        #��Ҫ���Լ����бȽ�
        if other==person:
            continue
        sim=similarity(prefs,person,other)
        #��������ֵС�ڵ���0�����
        if sim<=0:
            continue
        
        for item in prefs[other]:
        #ֻ���Լ���δ������ӰƬ��������
            if item not in prefs[person] or prefs[person][item]==0:
                #���ƶ�����
                totals.setdefault(item,0)
                totals[item]+=prefs[other][item]*sim
                #���ƶ�֮��
                simSums.setdefault(item,0)
                simSums[item]+=sim
    
    #����һ����һ���б�
    rankings=[(total/simSums[item],item)for item,total in totals.items()]
    #���ؾ���������б�
    rankings.sort()
    rankings.reverse()
    return rankings            