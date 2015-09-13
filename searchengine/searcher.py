#coding:gbk
'''
Created on 2015��7��19��

@author: fxy
'''
from pysqlite2 import dbapi2
import jieba
from audioop import reverse
import neuralNetWork
mynet=neuralNetWork.searchnet('nn.db')

class searcher(object):
    '''
    classdocs
    '''


    def __init__(self, dbname):
        '''
        Constructor
        '''
        self.con=dbapi2.connect(dbname)
    
    
    def __del__(self):
        self.con.close()
    

    def getmatchchrows(self,q):
        #�����ѯ�ַ���
        fieldlist='w0.urlid'
        tablelist=''
        clauselist=''
        wordids=[]
         
        #��ֵ��� 
        temp=jieba.cut(q)
        words=[word for word in temp]
        tablenumber=0
         
        #�������ݿ��ѯ��� 
        for word in words:
            wordrow=self.con.execute("select rowid from wordlist where word='%s' " %word).fetchone()
            if wordrow!=None:
                wordid=wordrow[0]
                wordids.append(wordid)
                if tablenumber>0:
                    tablelist+=','
                    clauselist+='  and  '
                    clauselist+='w%d.urlid=w%d.urlid and '%(tablenumber-1,tablenumber)
                fieldlist+=',w%d.location'%tablenumber
                tablelist+='wordlocation w%d'%tablenumber
                clauselist+='w%d.wordid=%d'%(tablenumber,wordid)
                tablenumber+=1
                 
                 
        #���ݸ������飬������ѯ
        fullquery='select %s from %s where %s'%(fieldlist,tablelist,clauselist)
        print fullquery
        cur=self.con.execute(fullquery)
        rows=[row for row in cur]
        
        #����  
        return rows,wordids
    
    #����Ȩֵ                
    def getscoredlist(self,rows,wordids):
        totalscores=dict([(row[0],0)for row in rows])
        
        #�˴����Ժ�������ۺ����ĵط�
        weights=[
                 (1.0,self.frequencyscore(rows)),
                 (1.5,self.locationscore(rows)),
                 (1.0,self.distancescore(rows)),
                 (1.0,self.pagerankscore(rows)),
                 (1.0,self.linkTextScore(rows, wordids)),
                 (5,self.nnscore(rows, wordids))]
        
        for (weight,scores) in weights:
            for url in totalscores:
                totalscores[url]+=weight*scores[url]
        
        return totalscores
    
    def geturlname(self,id):
        return self.con.execute('select url from urllist where rowid=%d' % id).fetchone()[0]
    
    def query(self,q):
        rows,wordids=self.getmatchchrows(q)
        scores=self.getscoredlist(rows, wordids)
        rankedscores=sorted([(score,url) for (url,score) in scores.items()],reverse=1)
        for (score,urlid) in rankedscores[0:]:
            print '%f\t%s' % (score,self.geturlname(urlid))
        return wordids,[r[1] for r in rankedscores[0:10]]
    
    #��һ������
    def normalizescorse(self,scores,smallIsBetter=0):
        vsmall=0.00001#���ⱻ0����
        if smallIsBetter:
            minscore=min(scores.values())
            return dict([(u,float(minscore)/max(vsmall,l)) for(u,l) in scores.items()])
        else:
            maxscore=max(scores.values())
            if maxscore==0:maxscore=vsmall
            return dict([(u,float(c)/maxscore)for (u,c) in scores.items()])
    
    
    #����Ƶ�Ⱥ���
    def frequencyscore(self,rows):
        counts=dict([(row[0],0)for row in rows])
        for row in rows:
            counts[row[0]]+=1
        return self.normalizescorse(counts)
    
    
    
    #�ĵ�λ��
    def locationscore(self,rows):
        locations=dict([(row[0],1000000)for row in rows])
        for row in rows:
            loc=sum(row[1:])
            if loc<locations[row[0]]:
                locations[row[0]]=loc
        return self.normalizescorse(locations, smallIsBetter=1)
    
    
    #���ʾ���
    def distancescore(self,rows):
        #�������һ�����ʣ���÷ֶ�һ��
        if len(rows[0])<=2:
            return dict([(row[0],1.0)for row in rows])
        #��ʼ���ֵ䣬������һ���ܴ����
        mindistance=dict([(row[0],1000000)for row in rows])
        for row in rows:
            dist=sum([abs(row[i]-row[i-1]) for i in range(2,len(row))])
            if dist<mindistance[row[0]]:
                mindistance[row[0]]=dist
        return self.normalizescorse(mindistance, smallIsBetter=1)
    #�����ⲿ��ָ����
    def inBoundLinkScore(self,rows):
        uniqueurs=set([row[0] for row in rows])
        inBoundCount=dict([(u,self.con.execute('select count(*) from link where toid=%d' %u).fetchone()[0])\
                           for u in uniqueurs])
        return self.normalizescorse(inBoundCount)
        
        
    #����pagwrank
    def pagerankscore(self,rows):
        pageranks=dict([(row[0],self.con.execute('select score from pagerank where urlid=%d' % row[0]
                                                 ).fetchone()[0])for row in rows])
        maxrank=max(pageranks.values())
        normalizedscores=dict([(u,float(l)/maxrank)for (u,l)in pageranks.items()])
        return normalizedscores
    
    #���������ı�
    def linkTextScore(self,rows,wordids):
        linkscores=dict([(row[0],0)for row in rows])
        for wordid in wordids:
            cur=self.con.execute('select link.fromid,link.toid from linkwords,link where wordid=%d and linkwords.linkid=link.rowid' %wordid)
            for(fromid,toid) in cur:
                if toid in linkscores:
                    pr=self.con.execute('select score from pagerank where urlid=%d'%fromid).fetchone()[0]
                    linkscores[toid]+=pr
        maxscore=max(linkscores.values())
        if maxscore!=0:
            normalizedscores=dict([(u,float(l)/maxscore) for (u,l) in linkscores.items()])
        else:
            normalizedscores=dict([(u,float(l)/1000000) for (u,l) in linkscores.items()])
        return normalizedscores
    
    def nnscore(self,rows,wordids):
        #���һ����Ψһurl id���ɵ������б�
        urlids=[urlid for urlid in set([row[0] for row in rows])]
        nnres=mynet.getResult(wordids, urlids)
        scores=dict([(urlids[i],nnres[i])for i in range(len(urlids))])
        return self.normalizescorse(scores)
        