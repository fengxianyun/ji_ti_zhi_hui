#coding:gbk
'''

@author: fxy
'''
from pysqlite2 import dbapi2
import searchengine
import searcher
import sys  
import neuralNetWork
from searchengine import crawler
reload(sys)
#��Ȼ������ʵ��û��  
sys.setdefaultencoding("utf8")  

if __name__ == '__main__':
    pass
# #��ʼ���棬���������ݿ�
# pagelist=['http://www.acfun.tv']
# crawler=searchengine.crawler('searchindex.db')
# crawler.createindextables()
# crawler.crawl(pagelist)
# print '############################'

# #����
# e=searcher.searcher('searchindex.db')
# print e.query("acfun��Ƶ")

#pagerank
# crawler=searchengine.crawler('searchindex.db')
# crawler.calculatePageRank()

# #���ɴ����������ʺ�urlid�����ؽڵ�
# mynet=nn.searchnet('nn.db')
# mynet.makeDataBase()
# wWorld,wRiver,wBank=101,102,103
# uWordBank,uRiver,uEarth=201,202,203
# mynet.generateHiddenNode([wWorld,wBank], [uWordBank,uRiver,uEarth])
# 
# 
#ʵ��������
mynet=neuralNetWork.searchnet('nn.db')
wWorld,wRiver,wBank,wEarth=101,102,103,104
uWordBank,uRiver,uEarth,uWorldRiver=201,202,203,204
print mynet.getResult([wWorld,wBank], [uWordBank,uRiver,uEarth])
mynet.trainQuery([wWorld,wBank], [uWordBank,uRiver,uEarth],uWordBank)
mynet.trainQuery([wWorld,wBank], [uWordBank,uRiver,uEarth],uWordBank)
mynet.trainQuery([wWorld,wRiver], [uWordBank,uWorldRiver,uEarth],uWorldRiver)
mynet.trainQuery([wRiver,wEarth], [uWordBank,uWorldRiver,uEarth],uEarth)
print mynet.getResult([wWorld,wBank], [uWordBank,uRiver,uEarth,uWorldRiver])



