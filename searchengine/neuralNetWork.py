#coding:gbk
'''
Created on 2015��8��1��

@author: fxy
'''
# ʵ���������ѯԭ������������Ϊ����
# 1 �����ѯ����
# 
# 2 �ִʣ�����
# 
# 3 �����ݿ�����ȡ�������������������ϵ�Ĵ���id���м�ڵ�id��������id
#     a.������id���м�ڵ�id��������id֮��û����ϵ���򲻻᷵���κζ���
#     ����˵���������п������ӣ�����ֵ��Ϊ0
#     b.ֻ�о�����ѵ�����񾭽ڵ���п�����Ч�ķ���ֵ
# 
# 4 ��һά�����һά�����洢����id���м�ڵ�id��������id
#     a.������Ϊÿ��idΪһ���ڵ㣬����idΪ�����ڵ㣬�м�ڵ�idΪ���ز�ڵ㣬����idΪ�����ڵ�
# 
# 5 �������������ڵ㵽���ز�ڵ㣬�����ز�ڵ㵽�����ڵ��ǿ��
#     a.�����ö�ά��������ʾ��ÿһ�л��б�ʾһ���ڵ㵽��һ���ڵ��ǿ��
#     b.������������ڵ�����һ���������ز�ڵ���ô��һ�������ڵ�������ز�ڵ��ǿ��
#     ���Է���һ��С��ֵ
# 
# 6 �����������ڵ㵽��һ�����ز�ڵ�ǿ��֮�ͣ�����tanh����ĳһ��s�ͺ����������Ż����õ�
# һ��һά����
# 
# 7 ʹ��6�õ���һά���飬��Ȩ���������ز�ڵ㵽�����ڵ�ĺͣ�����s�ͺ����Ż����õ�һ��һά����
#  
# 8 ����7�Ľ��
# 
# ʵ��������ѵ��ԭ������������Ϊ����
# 
# 1 �����û����ܲ�ѯ����䣬��Ҫ��ϵ�Ľ������������ȷ�Ĳ�ѯ������������ѵ���󣬿������Ժ��û��Ĳ�ѯѡ��ֱ��������ѵ����
# 
# 2 �ִʣ�����
# 
# 3 ��飬����֮���Ƿ��Ѿ����ɹ��ڵ㣬û���ɵĻ������ɣ������ز�ڵ㣩���������ڵ㣬
# ���ز�ڵ㣬��Ҫ��ϵ�������ڵ�䣬����Ĭ��ǿ��
# 
# 4 ���в�ѯԭ��3-8
# 
# 5 ���÷��򴫲�������ѵ��
# 
# 6 �������ݿ�
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
        #�ж�����ǿ�ȣ������ӱ�Ҫʱ�Żᴴ�������������Ӳ�����ʱ����һ��Ĭ��ֵ
        #���ʲ㵽���ز�Ϊ-0.2�����ز㵽�����Ϊ0
        
        
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
        #�ж������Ƿ��Ѵ��ڣ��������µ�ǿ��ֵ�������ӻ򴴽�����
        #�ú�������Ϊѵ��������Ĵ�������
        
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
        #���������¹���������ʱ�����нڵ㶼��Ԥ�Ƚ����õģ����ǿ��Խ���һ�����ز�������ǧ�ڵ�
        #����ȫ�����Ӿ����ľ޴����磬����������ֻ����Ҫʱ�����ڵ㣬����Ч��Ҳ����
    
        #ÿ����һ���δδ�����ĵ�����ϣ��ú����ͻ������ز����½�һ���ڵ㡣�������Ϊ���������ؽڵ�֮��
        #�Լ���ѯ�ڵ����ѯ�����ص�url֮�佨�������Ĭ��Ȩ�ص�����
        
        if len(wordids)>3:
            return None
        #����Ƿ��Ѿ�Ϊ���鵥�ʽ�����һ���ڵ�
        create_key='_'.join(sorted([str(wi) for wi in wordids]))
        res=self.con.execute("select rowid from hiddennode where create_key='%s'" %create_key).fetchone()
        #���û������
        if res==None:
            cur=self.con.execute("insert into hiddennode (create_key) values('%s')"
                                 %create_key)
            hidden_id=cur.lastrowid
            #����Ĭ��Ȩ��
            for wordid in wordids:
                self.setStrength(wordid, hidden_id, 0, 1.0/len(wordids))
            for urlid in urls:
                self.setStrength(hidden_id, urlid, 1, 0.1)
            self.con.commit()
            
            
    def getAllHiddenIds(self,wordids,urlids):
        #��дһ�������������ز����ҳ���ĳ���ѯ��ص���һ��������
        #��������Щ�ڵ㣬��������ڲ�ѯ�����е�ĳ�����ʣ���������ѯ����е�ĳ��url
        
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
        #�������ݿ��б������Ϣ���������е�ǰȨֵ���ڵ���Ӧ���磬�����˶��ʵ������
        #���������б���ѯ�ڵ㼰url��ÿ���ڵ��������𣬼�ÿ���ڵ�������Ȩ��
        
        #ֵ�б�
        self.wordids=wordids
        self.hiddenids=self.getAllHiddenIds(wordids, urlids)
        self.urlids=urlids
        
        #�ڵ����
        self.ai=[1.0]*len(self.wordids)
        self.ah=[1.0]*len(self.hiddenids)
        self.ao=[1.0]*len(self.urlids)
        
        #����Ȩ�ؾ���
        self.wi=[[self.getStrength(wordid, hiddenid, 0)
                  for hiddenid in self.hiddenids]
                 for wordid in self.wordids]
        self.wo=[[self.getStrength(hiddenid, urlid, 1)
                  for urlid in self.urlids]
                 for hiddenid in self.hiddenids]
    
    
    
    def feedForward(self):
        #����ǰ���㷨���㷨����һ�����룬�����������磬Ȼ�󷵻����������ڵ��������
        
        #��ѯ�����ǽ��е�����
        for i in range(len(self.wordids)):
            self.ai[i]=1.0
        
        #���ز�ڵ�Ļ�Ծ�̶�
        for j in range(len(self.hiddenids)):
            sum=0.0
            for i in range(len(self.wordids)):
                sum=sum+self.ai[i]*self.wi[i][j]
            self.ah[j]=tanh(sum)
            
        #�����ڵ�Ļ�Ծ�̶�
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
    #���÷��򴫲�������ѵ��
    #����������ÿ���ڵ�
#     1 ���������������������Ĳ��
#     2 ����dtanh����ȷ���ڵ����������Ҫ��θı�
#     3 �ı�ÿ���ⲿ��ָ��ǿ��ֵ����ֵ�뵱ǰǿ�Ⱥ�ѧϰ������һ����ϵ
    
    #�������ز��е�ÿ���ڵ�
#     1 ��ÿ��������ӵ�ǿ��ֵ����Ŀ��ڵ�����ĸı��������ۼ���ͣ��Ӷ��ı�ڵ�������
#     2 ����dtanh����ȷ���ڵ���������Ҫ��θı�
#     3 �ı�ÿ���������ӵ�ǿ��ֵ����ֵ�뵱ǰǿ�Ⱥ�ѧϰ������һ����ϵ    
        
        #������������
        output_deltas=[0.0]*len(self.urlids)
        for k in range(len(self.urlids)):
            error=targets[k]-self.ao[k]
            output_deltas[k]=self.dtanh(self.ao[k])*error
            
        
        #�������ز����
        hidden_deltas=[0.0]*len(self.hiddenids)
        for j in range(len(self.hiddenids)):
            error=0.0
            for k in range(len(self.urlids)):
                error=error+output_deltas[k]*self.wo[j][k]
            hidden_deltas[j]=self.dtanh(self.ah[j])*error
        
        
        #�������Ȩ��
        for j in range(len(self.hiddenids)):
            for k in range(len(self.urlids)):
                change=output_deltas[k]*self.ah[j]
                self.wo[j][k]=self.wo[j][k]+N*change
        
        
        #��������Ȩ��
        for i in range(len(self.wordids)):
            for j in range(len(self.hiddenids)):
                change=hidden_deltas[j]*self.ai[i]
                self.wi[i][j]=self.wi[i][j]+N*change
    
    
    
    #�������ݿ�
    def updateDatabase(self):
        #��ֵ�������ݿ�
        for i in range(len(self.wordids)):
            for j in range(len(self.hiddenids)):
                self.setStrength(self.wordids[i], self.hiddenids[j], 0, self.wi[i][j])
        
        for j in range(len(self.hiddenids)):
            for k in range(len(self.urlids)):
                self.setStrength(self.hiddenids[j], self.urlids[k], 1, self.wo[j][k])
        self.con.commit()
    
    
    
    def trainQuery(self,wordids,urlids,selectedurl):
        #���������磬����ǰ���㷨�ͷ��򴫲��㷨
        
        #���б�Ҫ����һ�����ؽڵ�
        self.generateHiddenNode(wordids, urlids)
        
        self.setupNetwork(wordids, urlids)
        self.feedForward()
        targets=[0.0]*len(urlids)
        targets[urlids.index(selectedurl)]=1.0
        self.backPropagate(targets)
        self.updateDatabase()
        
                    