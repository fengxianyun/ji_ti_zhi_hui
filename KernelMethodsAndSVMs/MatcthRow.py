#coding:gbk
'''
Created on 2015年9月23日

@author: fxy
'''

class MatchRow:
    '''
    classdocs
    '''


    def __init__(self, row,allnum=False):
        '''
        Constructor
        '''
        if allnum:
            self.data=[float(row[i])for i in range(len(row)-1)]
        else:
            self.data=row[0:len(row)-1]
        self.match=int(row[len(row)-1])
        