#coding:gbk
'''
Created on 2015��8��13��

@author: fxy
'''
import optimization
optimization.getdata()
# s=[1,4,3,2,7,3,6,3,2,4,5,3]
# print optimization.printschedule(s)
# print optimization.schedulecost(s)

# #�����
# domain=[(0,9)]*(len(optimization.people)*2)
# s=optimization.randomoptimize(domain, optimization.schedulecost)
# print optimization.schedulecost(s)
# print optimization.printschedule(s)

# #��ɽ��
# domain=[(0,9)]*(len(optimization.people)*2)
# s=optimization.hillclimb(domain, optimization.schedulecost)
# print optimization.schedulecost(s)
# print optimization.printschedule(s)

# #ģ���˻�
# domain=[(0,9)]*(len(optimization.people)*2)
# s=optimization.annealingoptimize(domain, optimization.schedulecost)
# print optimization.schedulecost(s)
# print optimization.printschedule(s)

#�Ŵ��㷨
domain=[(0,9)]*(len(optimization.people)*2)
s=optimization.geneticoptimize(domain, optimization.schedulecost)
print optimization.printschedule(s)
print optimization.schedulecost(s)