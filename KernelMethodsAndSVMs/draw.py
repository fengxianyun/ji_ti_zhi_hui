#coding:gbk
'''
Created on 2015年9月24日

@author: fxy
'''
from pylab import *
def plotAgeMatches(rows):
    xdm,ydm=[r.data[0]for r in rows if r.match==1],[r.data[1] for r in rows if r.match==1]
    xdn,ydn=[r.data[0]for r in rows if r.match==0],[r.data[1] for r in rows if r.match==0]
    
    plot(xdm,ydm,'go')
    plot(xdn,ydn,'ro')
    show()