# coding:gbk
from sklearn.linear_model.sgd_fast import Regression
import  os
import  numpy as np
from  pandas.io.parsers import read_csv
from  sklearn.utils import  shuffle
from lasagne import layers
from lasagne.updates import nesterov_momentum
from nolearn.lasagne import NeuralNet

__author__ = 'fxy'
TRAIN='E:\\面部识别\\training.csv'
TEST='E:\\面部识别\\test.csv'

net1= NeuralNet(layers=
                [#three layers:one hidden layers
                 ('input',layers.InputLayer),
                 ('hidden',layers.DenseLayer),
                 ('output',layers.DenseLayer) 
                 ],
                # layer parameters
                input_shape=(None,9216),#每张图片大小96*96
                hidden_num_units=100,#隐藏层节点个数
                output_nonlinearity=None,
                output_num_units=30,#30个目标值
                
                #optimization method
                update=nesterov_momentum,
                update_learning_rate=0.01,
                update_momentum=0.9,
                
                regression=True, # flag to indicate we're dealing with regression problem
                max_epochs=400,#训练个数
                verbose=1,
                )

def loads(test=False,cols=None):
    #如果test为true则读取TEST的路径，否则读取TRAIN的路径
    fname=TEST if test else  TRAIN
    df=read_csv(os.path.expanduser(fname))
    df['Image']=df['Image'].apply(lambda im: np.fromstring(im,sep=' '))
    if cols:
        df=df[list(cols)+['image']]
    print(df.count())
    df=df.dropna()
    X=np.vstack(df['Image'].values)/255
    X=X.astype(np.float32)

    if not test:
        y=df[df.columns[:-1]].values
        y=(y-48)/48
        X,y=shuffle(X,y,random_state=42)
        y=y.astype(np.float32)
    else:
        y=None
    return X,y

X,y=loads()
print("X.shape == {}; X.min == {:.3f}; X.max == {:.3f}".format(
X.shape, X.min(), X.max()))
print("y.shape == {}; y.min == {:.3f}; y.max == {:.3f}".format(
y.shape, y.min(), y.max()))
net1.fit(X, y)