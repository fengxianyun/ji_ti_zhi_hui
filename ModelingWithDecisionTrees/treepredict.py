#coding:gbk
'''
Created on 2015��9��5��

@author: fxy
'''
def divideSet(rows,column,value):
        #��ĳһ���ϣ������ݼ��Ͻ��в��
        
        #����һ����������������������������������һ�黹�ǵڶ���
        split_function=None
        if isinstance(value, int)or isinstance(value, float):
            split_function=lambda row:row[column]>=value
        else:
            split_function=lambda row:row[column]==value
            
        #�����ݼ����Ϊ�������ϣ�������
        set1=[row for row in rows if split_function(row)]
        set2=[row for row in rows if not split_function(row)]
        
        return (set1,set2)

def uniqueCount(rows):
    #�Ը��ֿ��ܵĽ�����м�����ÿһ�����ݵ����һ�У���¼����һ���������
    results={}
    for row in rows:
        #��������������һ�У��������Ƿ�Ҫ��ɽ��������ǹ�����Ʒ���ʹ������յ�������û��
        r=row[len(row)-1]
        if r not in results:
            results[r]=0
        results[r]+=1
    return results

def giniImpurity(rows):
    #������᲻���ȣ���������õ�����������ڴ�������еĸ���(������p1,p2,p3���ַ��࣬���᲻����Ϊ1-p1^2-p2^2-p3^2)
    
    total=len(rows)
    counts=uniqueCount(rows)
    imp=1
    for k1 in counts:
        p1=float(counts[k1])/total
        imp=imp-p1*p1
    return imp

def entropy(rows):
    #�����أ����Ǳ������п��ܽ�������õ���p(x)log(p(x))֮��
    #�أ������˼��ϵ�����̶ȣ���Խ��Խ����
    
    from math import log
    log2=lambda x:log(x)/log(2)
    results=uniqueCount(rows)
    
    #�˴���ʼ�����ص�ֵ
    ent=0.0
    for r in results:
        p=float(results[r])/len(rows)
        ent=ent-p*log2(p)
    return ent 

def countVariance(rows):
    #���㷽��
    if len(rows)==0:
        return 0
    data=[float(row[len(row)-1]) for row in rows]
    mean=sum(data)/len(data)
    variance=sum([(d-mean)**2 for d in data])/len(data)
    return variance

def buildTree(rows,scoref=entropy):
    #�Եݹ鷽������������
    
    if len(rows)==0:
        return DecisionNode()
    current_score=scoref(rows)
    
    #����һЩ�����Լ�¼��Ѳ������
    best_gain=0.0
    best_criteria=None
    best_sets=None
    
    column_count=len(rows[0])-1
    for col in range(0,column_count):
        #�ڵ�ǰ��������һ���ɲ�ͬ�й��ɵ�����
        column_value={}
        for row in rows:
            column_value[row[col]]=1
        
        #��������������һ���е�ÿ��ֵ�����Զ����ݼ����в��
        for value in column_value:
            (set1,set2)=divideSet(rows, col, value)
            
            #��Ϣ����
            p=float(len(set1))/len(rows)
            gain=current_score-p*scoref(set1)-(1-p)*scoref(set2)
            if gain>best_gain and len(set1)>0 and len(set2)>0:
                best_gain=gain
                best_criteria=(col,value)
                best_sets=(set1,set2)
    #�����ӷ�֧
    if best_gain>0:
        trueBranch=buildTree(best_sets[0])
        falseBranch=buildTree(best_sets[1])
        return DecisionNode(col=best_criteria[0],value=best_criteria[1],tb=trueBranch,fb=falseBranch)
    else:
        return DecisionNode(resultes=uniqueCount(rows))
     
def classify(observation,tree):
    #�����Թ����õ��������з���   
    
    
    if tree.results!=None:
        return tree.results
    else:
        v=observation[tree.col]
        branch=None
        if isinstance(v, int) or isinstance(v, float):
            if v>=tree.value:
                branch=tree.tb
            else:
                branch=tree.fb
        else:
            if v==tree.value:
                branch=tree.tb
            else:
                branch=tree.fb
    return classify(observation, branch)

def mdclassify(observation,tree):
    #����classify���޸ģ�ʹ����Խ��ܲ�����������
    
    
    if tree.results!=None:
        return  tree.results
    else:
        v=observation[tree.col]
        if v==None:
            tr,fr=mdclassify(observation, tree.tb),mdclassify(observation, tree.fb)
            tcount=sum(tr.values())
            fcount=sum(fr.values())
            tw=float(tcount)/(tcount+fcount)
            fw=float(fcount)/(tcount+fcount)
            result={}
            for k,v in tr.items():
                result[k]=v*tw
            for k,v in fr.items():
                if k not in result:
                    result[k]=0
                result[k]+=v*fw
            return result
        else:
            if isinstance(v, int) or isinstance(v, float):
                if v>=tree.value:
                    branch=tree.tb
                else:
                    branch=tree.fb
            else:
                if v==tree.value:
                    branch=tree.tb
                else:
                    branch=tree.fb
            return mdclassify(observation, branch)
            
    

def prune(tree,mingain):
    #��֦����
    #mingainΪ��֦����ֵ��С�ڴ���ֵ�ᱻ��֦
    
    #�����֧����Ҷ�ӽڵ㣬������м�֦����
    if tree.tb.results==None:
        prune(tree.tb, mingain)
    if tree.fb.results==None:
        prune(tree.fb, mingain)
        
    #�������֧����Ҷ�ӽڵ㣬�ж��Ƿ�Ҫ�ϲ�
    if tree.tb.results!=None and tree.fb.results!=None:
        #����ϲ�������ݼ�
        tb,fb=[],[]
        for v,c in tree.tb.results.items():
            tb+=[[v]]*c
        for v,c in tree.fb.results.items():
            fb+=[[v]]*c
        
        #����صı仯���
        detal=entropy(tb+fb)-(entropy(tb)+entropy(fb))/2
        
        if detal<mingain:
            #�ϲ���֧
            tree.tb,tree.fb=None,None
            tree.results=uniqueCount(tb+fb)
                
        
class DecisionNode():
    def __init__(self,col=-1,value=None,resultes=None,tb=None,fb=None):
        #col Ϊ ��������ж���������Ӧ������ֵ
        #value��ӦΪ��ʹ���Ϊtrue����ǰ�б���ƥ���ֵ
        #tb��fbҲ��DecisionNode�����Ƿֱ��Ӧ�ڽ��Ϊtrue��falseʱ���ӽڵ�
        #results��������ڵ�ǰ��֧�Ľ��������һ���ֵ䣬��Ҷ�ӽڵ��⣬����ΪNone
        
        self.col=col
        self.value=value
        self.results=resultes
        self.tb=tb
        self.fb=fb
    
    