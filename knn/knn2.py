#coding:gbk
'''
Created on 2015年9月11日

@author: fxy
'''
import csv
import numpy
import operator
from _imaging import path
from _mysql import result

def getTrainImageAndNum():
    csvfile=file('E:\\编程\\数字\\train.csv','rb')
    reader=csv.reader(csvfile)
    num_list=[]
    image_list=[]
    string2num=[]
    i=0
    for line in reader:
        if i==0:
            i=i+1
            continue
        string2num=[]
        for num in line:
            string2num.append(int(num))
        num_list.append(string2num[0])
        image_list.append(string2num[1:])
    return (num_list,image_list)

def getTextImage():
    csvfile=file('E:\\编程\\数字\\test.csv','rb')
    reader=csv.reader(csvfile)
    image_list=[]
    i=0
    string2num=[]
    for line in reader:
        if i==0:
            i=i+1
            continue
        string2num=[]
        for num in line:
            string2num.append(int(num))
        image_list.append(string2num)
    return image_list

def changeImage(images):
    length_images=len(images)
    length_image=len(images[0])
    for i in range(length_images):
        for j in range(length_image):
            if images[i][j]!=0:
                images[i][j]=1
    return images

def classify(train_images,test_images,num_list,n):
    train_images=changeImage(train_images)
    test_images=changeImage(test_images)
    train_images=numpy.array(train_images)
    test_images=numpy.array(test_images)
    result=[]
    listnum=0
    for test_line in test_images:
        poor=train_images-test_line
        sqr=poor**2
        sqDistance=sqr.sum(axis=1)
        distance=sqDistance**0.5
        sortedDistIndicies=distance.argsort()
        classCount={}
        for i in range(n):
            index=num_list[sortedDistIndicies[i]]
            classCount[index]=classCount.get(index,0)+1
        sortedClassCount=sorted(classCount.iteritems(),key=operator.itemgetter(1),reverse=True)
        result.append([sortedClassCount[0][0]])
        print listnum,':\n'
        print sortedClassCount[0][0]
        print '\n'
        listnum+=1
    return result

def write2File(list,path):
    csvfile = file(path, 'wb')
    writer = csv.writer(csvfile)
    writer.writerows(list)
    
def dowith():
    result=[]
    csvfile=file('E:\\编程\\数字\\llll.csv','rb')
    reader=csv.reader(csvfile)
    csvfile = file('E:\\编程\\数字\\lllll.csv', 'wb')
    writer = csv.writer(csvfile)
    i=1
    for line in reader:
        result.append((i,line[0][0]))
        i=i+1
    writer.writerows(result)
    
        
        
    
    
    