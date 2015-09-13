#coding:gbk
'''
Created on 2015年7月16日

@author: fxy
'''
#从反应偏好的字典中返回最为匹配者
#返回结果的个数和相似度函数均可作为参数
from ou_ji_li_de_ju_li import sim_distance
from pi_er_xun_xiang_guan_du import sim_pearson
def topMatches(prefs,person,n=5,similarity=sim_pearson):
    scores=[(similarity(prefs,person,other) ,other )
            for other in prefs if other!=person]
    #对列表进行排序
    scores.sort();
    scores.reverse();
    return scores[0:n]

#利用其它所有人的评价值加权平均，提供建议
def getRecommendations(prefs,person,similarity=sim_distance):
    totals={}
    simSums={}
    for other in prefs:
        #不要和自己进行比较
        if other==person:
            continue
        sim=similarity(prefs,person,other)
        #忽略评价值小于等于0的情况
        if sim<=0:
            continue
        
        for item in prefs[other]:
        #只对自己还未看过的影片进行评价
            if item not in prefs[person] or prefs[person][item]==0:
                #相似度评价
                totals.setdefault(item,0)
                totals[item]+=prefs[other][item]*sim
                #相似度之和
                simSums.setdefault(item,0)
                simSums[item]+=sim
    
    #建立一个归一化列表
    rankings=[(total/simSums[item],item)for item,total in totals.items()]
    #返回经过排序的列表
    rankings.sort()
    rankings.reverse()
    return rankings            