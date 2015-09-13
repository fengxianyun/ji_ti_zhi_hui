#coding:gbk
'''
Created on 2015年8月1日

@author: fxy
'''
# 实验神经网络查询原理（以搜索引擎为例）
# 1 输入查询内容
# 
# 2 分词，处理
# 
# 3 从数据库中提取出所有与输入词语有联系的词语id，中间节点id，和链接id
#     a.若词语id，中间节点id，和链接id之间没有联系，则不会返回任何东西
#     或者说，对于所有可能链接，返回值都为0
#     b.只有经过了训练的神经节点才有可能有效的返回值
# 
# 4 用一维数组或一维表来存储词语id，中间节点id，和链接id
#     a.可以认为每个id为一个节点，词语id为输入层节点，中间节点id为隐藏层节点，链接id为输出层节点
# 
# 5 遍历所有输入层节点到隐藏层节点，及隐藏层节点到输出层节点的强度
#     a.可以用二维数组来表示，每一行或列表示一个节点到下一个节点的强度
#     b.如果两个输入层节点中有一个连向隐藏层节点那么另一个输入层节点对于隐藏层节点的强度
#     可以返回一个小的值
# 
# 6 计算多个输入层节点到下一个隐藏层节点强度之和，再用tanh（或某一类s型函数）进行优化，得到
# 一个一维数组
# 
# 7 使用6得到的一维数组，加权计算多个隐藏层节点到输出层节点的和，并用s型函数优化，得到一个一维数组
#  
# 8 返回7的结果
# 
# 实验神经网络训练原理（以搜索引擎为例）
# 
# 1 输入用户可能查询的语句，需要联系的结果，并给出正确的查询结果（经过多次训练后，可以用以后用户的查询选择直接来进行训练）
# 
# 2 分词，处理
# 
# 3 检查，词语之间是否已经生成过节点，没生成的话则生成（即隐藏层节点）并在输入层节点，
# 隐藏层节点，需要联系的输出层节点间，设置默认强度
# 
# 4 运行查询原理3-8
# 
# 5 利用反向传播法进行训练
# 
# 6 更新数据库
from math import tanh
from pysqlite2 import dbapi2 as sqlite
from __builtin__ import str
from test.test_threading_local import target
class searchnet:
    '''
    classdocs
    '''


    def __init__(self, database):
        self.con=sqlite.connect(database)
    
    def __del__(self):
        self.con.close()
        
    def dtanh(self,y):
        return 1.0-y*y
    
    def makeDataBase(self):
        self.con.execute('create table hiddennode(create_key)')
        self.con.execute('create table wordhidden(fromid, toid,strength)')
        self.con.execute('create table hiddenurl(fromid,toid,strength)')
        self.con.commit()
        
    def getStrength(self,fromid,toid,layer):
        #判断连接强度，新连接必要时才会创建，所以在连接不存在时返回一个默认值
        #单词层到隐藏层为-0.2，隐藏层到输出层为0
        
        
        if layer==0:
            table='wordhidden'
        else:
            table='hiddenurl'
        res=self.con.execute('select strength from %s where fromid=%d and toid=%d'%(table,fromid,toid)).fetchone()
        if res==None:
            if layer==0:
                return -0.2
            else:
                return 0
        return res[0]
    
    
    def setStrength(self,fromid,toid,layer,strength):
        #判断连接是否已存在，并利用新的强度值更新连接或创建连接
        #该函数将会为训练神经网络的代码所用
        
        if layer==0:
            table='wordhidden'
        else:
            table='hiddenurl'
        res=self.con.execute('select rowid from %s where fromid=%d and toid=%d'%
                             (table,fromid,toid)).fetchone()
        if res==None:
            self.con.execute('insert into %s (fromid,toid,strength) values(%d,%d,%f)'%
                             (table,fromid,toid,strength))
        else:
            rowid=res[0]
            self.con.execute('update %s set strength=%f where rowid=%d'%(table,strength,rowid))
        
            
    def generateHiddenNode(self,wordids,urls):
        #大多数情况下构建神经网络时，所有节点都是预先建立好的，我们可以建立一个隐藏层中有上千节点
        #并且全部连接就绪的巨大网络，不过本例中只在需要时建立节点，更高效，也更简单
    
        #每传入一组从未未见过的单词组合，该函数就会在隐藏层中新建一个节点。随后函数会为单词与隐藏节点之间
        #以及查询节点与查询所返回的url之间建立起具有默认权重的连接
        
        if len(wordids)>3:
            return None
        #检查是否已经为这组单词建好了一个节点
        create_key='_'.join(sorted([str(wi) for wi in wordids]))
        res=self.con.execute("select rowid from hiddennode where create_key='%s'" %create_key).fetchone()
        #如果没有则建立
        if res==None:
            cur=self.con.execute("insert into hiddennode (create_key) values('%s')"
                                 %create_key)
            hidden_id=cur.lastrowid
            #设置默认权重
            for wordid in wordids:
                self.setStrength(wordid, hidden_id, 0, 1.0/len(wordids))
            for urlid in urls:
                self.setStrength(hidden_id, urlid, 1, 0.1)
            self.con.commit()
            
            
    def getAllHiddenIds(self,wordids,urlids):
        #编写一个函数，从隐藏层中找出与某想查询相关的那一部分网络
        #本例中这些节点，必须关联于查询条件中的某个单词，或关联与查询结果中的某个url
        
        l1={}
        for wordid in wordids:
            cur=self.con.execute('select toid from wordhidden where fromid=%d'%wordid)
            for row in cur:
                l1[row[0]]=1
        for urlid in urlids:
            cur=self.con.execute('select fromid from hiddenurl where toid=%d'%urlid)
            for row in cur:
                l1[row[0]]=1
        return l1.keys()
    
    
    def setupNetwork(self,wordids,urlids):
        #利用数据库中保存的信息，包括所有当前权值在内的相应网络，定义了多个实例变量
        #包括单词列表，查询节点及url，每个节点的输出级别，即每个节点间的连接权重
        
        #值列表
        self.wordids=wordids
        self.hiddenids=self.getAllHiddenIds(wordids, urlids)
        self.urlids=urlids
        
        #节点输出
        self.ai=[1.0]*len(self.wordids)
        self.ah=[1.0]*len(self.hiddenids)
        self.ao=[1.0]*len(self.urlids)
        
        #建立权重矩阵
        self.wi=[[self.getStrength(wordid, hiddenid, 0)
                  for hiddenid in self.hiddenids]
                 for wordid in self.wordids]
        self.wo=[[self.getStrength(hiddenid, urlid, 1)
                  for urlid in self.urlids]
                 for hiddenid in self.hiddenids]
    
    
    
    def feedForward(self):
        #构造前馈算法，算法接收一列输入，将其推入网络，然后返回所有输出层节点的输出结果
        
        #查询单词是仅有的输入
        for i in range(len(self.wordids)):
            self.ai[i]=1.0
        
        #隐藏层节点的活跃程度
        for j in range(len(self.hiddenids)):
            sum=0.0
            for i in range(len(self.wordids)):
                sum=sum+self.ai[i]*self.wi[i][j]
            self.ah[j]=tanh(sum)
            
        #输出层节点的活跃程度
        for k in range(len(self.urlids)):
            sum=0.0
            for j in range(len(self.hiddenids)):
                sum=sum+self.ah[j]*self.wo[j][k]
            self.ao[k]=tanh(sum)
            
        return self.ao[:]
    
    def getResult(self,wordids,urlids):
        self.setupNetwork(wordids, urlids)
        return self.feedForward()
    
    def backPropagate(self,targets,N=0.5):
    #利用反向传播法进行训练
    #对于输出层的每个节点
#     1 计算输出结果与期望结果间的差距
#     2 利用dtanh函数确定节点的总输入需要如何改变
#     3 改变每个外部回指的强度值，其值与当前强度和学习速率有一定关系
    
    #对于隐藏层中的每个节点
#     1 将每个输出链接的强度值乘以目标节点所需的改变量，再累加求和，从而改变节点输出结果
#     2 利用dtanh函数确定节点总输入需要如何改变
#     3 改变每个输入链接的强度值，其值与当前强度和学习速率有一定关系    
        
        #计算输出层误差
        output_deltas=[0.0]*len(self.urlids)
        for k in range(len(self.urlids)):
            error=targets[k]-self.ao[k]
            output_deltas[k]=self.dtanh(self.ao[k])*error
            
        
        #计算隐藏层误差
        hidden_deltas=[0.0]*len(self.hiddenids)
        for j in range(len(self.hiddenids)):
            error=0.0
            for k in range(len(self.urlids)):
                error=error+output_deltas[k]*self.wo[j][k]
            hidden_deltas[j]=self.dtanh(self.ah[j])*error
        
        
        #更新输出权重
        for j in range(len(self.hiddenids)):
            for k in range(len(self.urlids)):
                change=output_deltas[k]*self.ah[j]
                self.wo[j][k]=self.wo[j][k]+N*change
        
        
        #更新输入权重
        for i in range(len(self.wordids)):
            for j in range(len(self.hiddenids)):
                change=hidden_deltas[j]*self.ai[i]
                self.wi[i][j]=self.wi[i][j]+N*change
    
    
    
    #更新数据库
    def updateDatabase(self):
        #将值存入数据库
        for i in range(len(self.wordids)):
            for j in range(len(self.hiddenids)):
                self.setStrength(self.wordids[i], self.hiddenids[j], 0, self.wi[i][j])
        
        for j in range(len(self.hiddenids)):
            for k in range(len(self.urlids)):
                self.setStrength(self.hiddenids[j], self.urlids[k], 1, self.wo[j][k])
        self.con.commit()
    
    
    
    def trainQuery(self,wordids,urlids,selectedurl):
        #建立神经网络，运行前馈算法和反向传播算法
        
        #如有必要生成一个隐藏节点
        self.generateHiddenNode(wordids, urlids)
        
        self.setupNetwork(wordids, urlids)
        self.feedForward()
        targets=[0.0]*len(urlids)
        targets[urlids.index(selectedurl)]=1.0
        self.backPropagate(targets)
        self.updateDatabase()
        
                    