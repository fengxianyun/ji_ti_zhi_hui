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
#虽然报错但其实并没错  
sys.setdefaultencoding("utf8")  

if __name__ == '__main__':
    pass
# #开始爬虫，并存入数据库
# pagelist=['http://www.acfun.tv']
# crawler=searchengine.crawler('searchindex.db')
# crawler.createindextables()
# crawler.crawl(pagelist)
# print '############################'

# #搜索
# e=searcher.searcher('searchindex.db')
# print e.query("acfun视频")

#pagerank
# crawler=searchengine.crawler('searchindex.db')
# crawler.calculatePageRank()

# #生成带有样例单词和urlid的隐藏节点
# mynet=nn.searchnet('nn.db')
# mynet.makeDataBase()
# wWorld,wRiver,wBank=101,102,103
# uWordBank,uRiver,uEarth=201,202,203
# mynet.generateHiddenNode([wWorld,wBank], [uWordBank,uRiver,uEarth])
# 
# 
#实验神经网络
mynet=neuralNetWork.searchnet('nn.db')
wWorld,wRiver,wBank,wEarth=101,102,103,104
uWordBank,uRiver,uEarth,uWorldRiver=201,202,203,204
print mynet.getResult([wWorld,wBank], [uWordBank,uRiver,uEarth])
mynet.trainQuery([wWorld,wBank], [uWordBank,uRiver,uEarth],uWordBank)
mynet.trainQuery([wWorld,wBank], [uWordBank,uRiver,uEarth],uWordBank)
mynet.trainQuery([wWorld,wRiver], [uWordBank,uWorldRiver,uEarth],uWorldRiver)
mynet.trainQuery([wRiver,wEarth], [uWordBank,uWorldRiver,uEarth],uEarth)
print mynet.getResult([wWorld,wBank], [uWordBank,uRiver,uEarth,uWorldRiver])



