#coding:gbk
'''
Created on 2015��9��29��

@author: fxy
'''
import theano.tensor as T
from theano import  function
from theano import pp
import numpy
#����һ��������ӵĺ���
#����һ��������ת��Ϊc���룬������?
x=T.dscalar('x')
y=T.dscalar('y')
z=x+y
f=function([x,y], z)

print f(2,3)
print f(16.3,12.1)
#չʾ z�Ķ���?
print pp(z)
#����һ����������ӵĺ���
x=T.dmatrix('x')
y=T.dmatrix('y')
z=x+y
f2=function([x,y], z)
print f2([[1,2],[3,4]],[[10,20],[30,40]])
print f2(numpy.array([[1,2],[3,4]]),numpy.array([[10,20],[30,40]]))

a = T.vector() # ����
b = T.vector()
out = a**2 + b**2+2*a*b               # build symbolic expression
f3= function([a,b], out)   # compile function
print(f3([0, 1, 2],[0,1,2]))
