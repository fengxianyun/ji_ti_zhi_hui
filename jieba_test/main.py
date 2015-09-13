#coding:gbk
'''
Created on 2015年7月19日

@author: fxy
'''

import jieba
if __name__ == '__main__':
    pass

seg_list=jieba.cut("去掉右边空格     去掉所有的空格 手机号码的正则表达式   (l;}")
#print ",".join(seg_list)
print 1
seg=[i for i in seg_list if i!=" "]
print 2
print "#".join(seg)
print 3