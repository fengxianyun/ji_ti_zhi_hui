#coding:gbk
'''
Created on 2015��7��19��

@author: fxy
'''

import jieba
if __name__ == '__main__':
    pass

seg_list=jieba.cut("ȥ���ұ߿ո�     ȥ�����еĿո� �ֻ������������ʽ   (l;}")
#print ",".join(seg_list)
print 1
seg=[i for i in seg_list if i!=" "]
print 2
print "#".join(seg)
print 3