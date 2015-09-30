#coding:gbk
'''
Created on 2015��9��29��

@author: fxy
'''
#����ɽ��ܾ���ĺ������Ժ����ڵ�ÿ��ֵ���д˺���
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

#�������ֻ�����Ͳ�ľ���ֵ,����������
a,b=T.dmatrices('a','b')
diff=a-b
abs_diff=abs(diff)
diff_squared=diff**2
f=theano.function([a,b],[diff,abs_diff,diff_squared])
print f([[1, 1], [1, 1]], [[0, 1], [2, 3]])

#ʹ�ó�ʼֵ
x,y=T.dscalars('x','y')
z=x+y
f=theano.function([theano.Param(x,default=1),theano.Param(y,default=2)],z)
print f()
print f(3)
print f(3,4)

#�����
srng=T.shared_randomstreams.RandomStreams(seed=234)
rv_u=srng.uniform((2,2))#�γ�һ��2*2�ķ��Ӿ��ȷֲ��ľ���
rv_n=srng.normal((2,2))#�γ�һ��2*2�ķ�����̬�ֲ��ľ���,
f=theano.function([],rv_u)#ÿ�ε��û�ı�ֵ
g=theano.function([],rv_n,no_default_updates=True)#ÿ�ε��ò���ı�ֵ
nearly_zeros=theano.function([],rv_u+rv_u-2*rv_u)

f_val0=f()
f_val1=f()

g_val0=g()
g_val1=g()

z_val0=nearly_zeros()
z_val1=nearly_zeros()
print f_val0,f_val1,g_val0,g_val1,z_val0,z_val1