#coding:gbk
'''
Created on 2015年9月10日

@author: fxy
'''

import operator
from numpy import *
from dircache import listdir

dir='E:\\编程\\机器学习实战及配套代码\\MLiA_SourceCode\\machinelearninginaction\\Ch02'

def createDataSet():
    group =array([[1.0,1.1],[1.0,1.0],[0,0],[0,0.1]])
    labels=['A','A','B','B']
    return group,labels

def classify0(inX,dataSet,labels,k):
    dataSetSize=dataSet.shape[0]
    diffMat=dataSet-inX
    sqDiffMat=diffMat**2
    sqDistances=sqDiffMat.sum(axis=1)
    distances=sqDistances**0.5
    #第n小的数所对应的位置
    sortedDistIndicies=distances.argsort()
    classCount={}
    for i in range(k):
        voteIlabel=labels[sortedDistIndicies[i]]
        classCount[voteIlabel]=classCount.get(voteIlabel,0)+1
    sortedClassCount=sorted(classCount.iteritems(),key=operator.itemgetter(1),reverse=True)
    return sortedClassCount[0][0]

def image2vector(filename):
    returnVect=zeros((1,1024))
    fr=open(filename)
    for i in range(32):
        lineStr=fr.readline()
        for j in range(32):
            returnVect[0,32*i+j]=int(lineStr[j])
    return returnVect

def handWritingClassTest():
    hwLabels=[]
    training_file_list=listdir('%s\\trainingDigits'%dir)
    m=len(training_file_list)
    training_mat=zeros((m,1024))
    for i in range(m):
        file_name_string=training_file_list[i]
        file_str=file_name_string.split('.')[0]
        class_num_str=int(file_str.split('_')[0])
        hwLabels.append(class_num_str)
        training_mat[i,:]=image2vector('%s\\trainingDigits\\%s'%(dir,file_name_string))
    test_file_list=listdir('%s\\testDigits'%dir)
    error_count=0.0
    mTest=len(test_file_list)
    for i in range(mTest):
        file_name_string=test_file_list[i]
        file_str=file_name_string.split('.')[0]
        class_num_str=int(file_str.split('_')[0])
        vector_under_test=image2vector('%s\\testDigits\\%s'%(dir,file_name_string))
        classifier_result=classify0(vector_under_test, training_mat, hwLabels, 3)
        print "the classifier came back with： %d, the real answer is: %d"% (classifier_result, class_num_str)
        if(classifier_result!=class_num_str):
            error_count+=1.0
    print "\nthe total number of errors is: %d" %error_count
    print "\nthe total error rate is: %f" % (error_count/float(mTest))
 
        
    

