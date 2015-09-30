#coding:gbk
'''
Created on 2015年9月29日

@author: fxy
'''
#构造可接受矩阵的函数，对函数内的每个值运行此函数
import theano
import theano.tensor as T
x=T.dmatrix('x')
s=1/(1+T.exp(-x))
logistic=theano.function([x],s)
s2=(1+T.tanh(x/2))/2
logistic2=theano.function([x],s2)
print logistic([[0,1,-1,-2]])
print logistic2([[0,1,-1,-2]])
theano.printing.pydotprint(logistic, "lll.png", var_with_name_simple=True)

#计算矩阵只差，方差，和差的绝对值,输出多个变量
a,b=T.dmatrices('a','b')
diff=a-b
abs_diff=abs(diff)
diff_squared=diff**2
f=theano.function([a,b],[diff,abs_diff,diff_squared])
print f([[1, 1], [1, 1]], [[0, 1], [2, 3]])

#使用初始值
x,y=T.dscalars('x','y')
z=x+y
f=theano.function([theano.Param(x,default=1),theano.Param(y,default=2)],z)
print f()
print f(3)
print f(3,4)

#随机数
srng=T.shared_randomstreams.RandomStreams(seed=234)
rv_u=srng.uniform((2,2))#形成一个2*2的服从均匀分布的矩阵
rv_n=srng.normal((2,2))#形成一个2*2的服从正态分布的矩阵,
f=theano.function([],rv_u)#每次调用会改变值
g=theano.function([],rv_n,no_default_updates=True)#每次调用不会改变值
nearly_zeros=theano.function([],rv_u+rv_u-2*rv_u)

f_val0=f()
f_val1=f()

g_val0=g()
g_val1=g()

z_val0=nearly_zeros()
z_val1=nearly_zeros()
print f_val0,f_val1,g_val0,g_val1,z_val0,z_val1