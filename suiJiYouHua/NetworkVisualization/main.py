#coding:gbk
'''
Created on 2015年8月30日

@author: fxy
'''
import socialnetwork
import optimization
sol=optimization.hillclimb(socialnetwork.domain, socialnetwork.crosscount)
print socialnetwork.crosscount(sol)
print sol
socialnetwork.drawNetWork(sol)
print "lll"