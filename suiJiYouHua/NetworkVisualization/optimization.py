#coding:gbk
'''
Created on 2015年8月13日

@author: fxy
'''

import time
import random
import math

people=[('Seymour','BOS'),
        ('Franny','DAL'),
        ('Zooey','CAK'),
        ('Walt','MIA'),
        ('Buddy','ORD'),
        ('Les','OMA')]
# NewYork 的 laGuardia机场
destination='LGA'

flights={}
#
def getdata():
    for line in file('schedule.txt'):
        origin,dest,depart,arrive,price=line.strip().split(',')
        flights.setdefault((origin,dest),[])
        #将航班详情加入航班列表
        flights[(origin,dest)].append((depart,arrive,int(price)))

def getminutes(t):
    x=time.strptime(t, '%H:%M')
    return x[3]*60+x[4]

#将人们决定搭乘的航班打印成表格
def printschedule(r):
    for d in range(len(r)/2):
        name=people[d][0]
        origin=people[d][1]
        out=flights[(origin,destination)][r[2*d]]
        ret=flights[(destination,origin)][r[2*d+1]]
        print '%10s%10s %5s-%5s $%3s %5s-%5s $%3s'%(name,origin,out[0],out[1],out[2],
                                                  ret[0],ret[1],ret[2])

#计算成本
def schedulecost(sol):
    totalprice=0
    latestarrival=0
    earliestdep=24*60
    
    for d in range(len(sol)/2):
        #得到往返航班
        origin=people[d][1]
        outbound=flights[(origin,destination)][int(sol[2*d])]
        returnf=flights[(destination,origin)][int(sol[2*d+1])]
        
        #总价等于所有往返航班价格之和 
        totalprice+=outbound[2]
        totalprice+=returnf[2]
        
        #记录最晚到达和最早离开的时间
        if latestarrival<getminutes(outbound[1]):
            latestarrival=getminutes(outbound[1])
        if earliestdep>getminutes(returnf[0]):
            earliestdep=getminutes(returnf[0])
    
    #每个人必须在机场等候直到最后一个人到达
    #他们也必须在相同的时间到达，等待返程航班
    totalwait=0
    for d in range(len(sol)/2):
        #得到往返航班
        origin=people[d][1]
        outbound=flights[(origin,destination)][int(sol[2*d])]
        returnf=flights[(destination,origin)][int(sol[2*d+1])]
        
        totalwait+=latestarrival-getminutes(outbound[1])
        totalwait+=getminutes(returnf[0])-earliestdep
    
    #需要多付一天租车费用吗
    if latestarrival<earliestdep:
        totalprice+=50
    return totalprice+totalwait

#随机搜索
#domin为一二元组列表，指定每个变量的最小最大值
#costf为成本函数
def randomoptimize(domain,costf):
    best=999999999
    bestr=None
    for i in range(10000):
        #创建一随机解
        r=[random.randint(domain[i][0],domain[i][1])
           for i in range(len(domain))]
        #得到成本
        cost=costf(r)
        #与目前的最优解比较
        if cost<best:
            best=cost
            bestr=r
    return bestr

#爬山法
def hillclimb(domain,costf):
    #创建一随机解
    sol=[random.randint(domain[i][0],domain[i][1])
           for i in range(len(domain))]
    #主循环
    while 1:
        
        #创建相邻解列表
        neighbors=[]
        for j in range(len(domain)):
            #在每个方向上对原值偏离一点
            if sol[j]>domain[j][0]:
                neighbors.append(sol[0:j]+[sol[j]-1]+sol[j+1:])
            if sol[j]<domain[j][1]:
                neighbors.append(sol[0:j]+[sol[j]+1]+sol[j+1:])
        
        #在相邻解中寻找最优解
        current=costf(sol)
        best=current
        for j in range(len(neighbors)):
            cost=costf(neighbors[j])
            if cost<best:
                best=cost
                sol=neighbors[j]
        if best==current:
            break
    return sol

#模拟退火算法
def annealingoptimize(domain,costf,T=10000.0,cool=0.99,step=1):
    #随机初始化值        
    vec=[random.randint(domain[i][0],domain[i][1])
           for i in range(len(domain))]
    while T>0.1:
        #选择一个索引值
        i=random.randint(0,len(domain)-1)
        
        #选择一个改变索引值的方向
        dir=random.randint(-step,step)
        
        #创建一个代表题解的新列表，改变其中一个值
        vecb=vec[:]
        vecb[i]+=dir
        if vecb[i]<domain[i][0]:
            vecb[i]=domain[i][0]
        if vecb[i]>domain[i][1]:
            vecb[i]=domain[i][1]
            
        #计算当前成本和新成本
        ea=costf(vec)
        eb=costf(vecb)
        
        #判断是否为更好解，或趋向于最优解的可能临界解
        if(eb<ea or random.random()<pow(math.e, -(eb-ea)/T)):
            vec=vecb
        T=T*cool
    return vec

#遗传算法
def geneticoptimize(domain,costf,popsize=100,step=1,
                    mutprob=0.4,elite=0.2,maxiter=100):
    #popsize代表种群大小
    #mutprob代表新成员由变异得来的概率
    #elite代表允许传入下一代的部分
    #maxiter代表运行多少代
    
    #变异操作
    def mutate(vec):
        i=random.randint(0,len(domain)-1)
        if (vec[i]==domain[i][1]or(random.random()<0.5 and vec[i]>domain[i][0])):
            return vec[0:i]+[vec[i]-step]+vec[i+1:]
        elif  vec[i]<domain[i][1]:
            return vec[0:i]+[vec[i]+step]+vec[i+1:]
    
    #交叉操作
    def crossover(r1,r2):
        i=random.randint(1,len(domain)-2)
        return r1[0:i]+r2[i:]
    
    #构造初始种群
    pop=[]
    for i in range(popsize):
        vec=[random.randint(domain[i][0],domain[i][1])
             for i in range(len(domain))]
        pop.append(vec)
    
    #每一代胜出者个数
    topelite=int(elite*popsize)
    
    #主循环
    for i in range(maxiter):
        scores=[(costf(v),v) for v in pop]
        scores.sort()
        ranked=[v for (s,v) in scores]
        
        #将胜者拉入新种群
        pop=ranked[0:topelite]
        
        #添加变异和配对
        while len(pop)<popsize:
            if random.random()<mutprob:
                #变异
                c=random.randint(0,topelite)
                pop.append(mutate(ranked[c]))
            else:
                #交叉
                c1=random.randint(0,topelite)
                c2=random.randint(0,topelite)
                pop.append(crossover(ranked[c1], ranked[c2]))
            #打印当前最优值
        print i,"代"
        print scores[0][0]
        print scores[0][1]
        
    return scores[0][1]    