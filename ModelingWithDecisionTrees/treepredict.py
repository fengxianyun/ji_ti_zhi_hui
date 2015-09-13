#coding:gbk
'''
Created on 2015年9月5日

@author: fxy
'''
def divideSet(rows,column,value):
        #在某一列上，对数据集合进行拆分
        
        #定义一个函数，令其告诉我们我们数据行数与第一组还是第二组
        split_function=None
        if isinstance(value, int)or isinstance(value, float):
            split_function=lambda row:row[column]>=value
        else:
            split_function=lambda row:row[column]==value
            
        #将数据集拆分为两个集合，并返回
        set1=[row for row in rows if split_function(row)]
        set2=[row for row in rows if not split_function(row)]
        
        return (set1,set2)

def uniqueCount(rows):
    #对各种可能的结果进行计数（每一行数据的最后一列，记录了这一计数结果）
    results={}
    for row in rows:
        #计数结果放在最后一列（即最终是否要达成结果，如果是购买物品，就代表最终到底买了没）
        r=row[len(row)-1]
        if r not in results:
            results[r]=0
        results[r]+=1
    return results

def giniImpurity(rows):
    #计算基尼不纯度，即随机放置的数据项出现于错误分类中的概率(假设有p1,p2,p3三种分类，基尼不纯度为1-p1^2-p2^2-p3^2)
    
    total=len(rows)
    counts=uniqueCount(rows)
    imp=1
    for k1 in counts:
        p1=float(counts[k1])/total
        imp=imp-p1*p1
    return imp

def entropy(rows):
    #计算熵，熵是遍历所有可能结果后所得到的p(x)log(p(x))之和
    #熵，代表了集合的无序程度，熵越高越混乱
    
    from math import log
    log2=lambda x:log(x)/log(2)
    results=uniqueCount(rows)
    
    #此处开始计算熵的值
    ent=0.0
    for r in results:
        p=float(results[r])/len(rows)
        ent=ent-p*log2(p)
    return ent 

def countVariance(rows):
    #计算方差
    if len(rows)==0:
        return 0
    data=[float(row[len(row)-1]) for row in rows]
    mean=sum(data)/len(data)
    variance=sum([(d-mean)**2 for d in data])/len(data)
    return variance

def buildTree(rows,scoref=entropy):
    #以递归方法构建决策树
    
    if len(rows)==0:
        return DecisionNode()
    current_score=scoref(rows)
    
    #定义一些变量以记录最佳拆分条件
    best_gain=0.0
    best_criteria=None
    best_sets=None
    
    column_count=len(rows[0])-1
    for col in range(0,column_count):
        #在当前列中生成一个由不同列构成的序列
        column_value={}
        for row in rows:
            column_value[row[col]]=1
        
        #接下来，根据这一列中的每个值，尝试对数据集进行拆分
        for value in column_value:
            (set1,set2)=divideSet(rows, col, value)
            
            #信息增益
            p=float(len(set1))/len(rows)
            gain=current_score-p*scoref(set1)-(1-p)*scoref(set2)
            if gain>best_gain and len(set1)>0 and len(set2)>0:
                best_gain=gain
                best_criteria=(col,value)
                best_sets=(set1,set2)
    #创建子分支
    if best_gain>0:
        trueBranch=buildTree(best_sets[0])
        falseBranch=buildTree(best_sets[1])
        return DecisionNode(col=best_criteria[0],value=best_criteria[1],tb=trueBranch,fb=falseBranch)
    else:
        return DecisionNode(resultes=uniqueCount(rows))
     
def classify(observation,tree):
    #根据以构建好的树，进行分类   
    
    
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
    #对于classify的修改，使其可以接受不完整的数据
    
    
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
    #剪枝函数
    #mingain为剪枝的阈值，小于此阈值会被剪枝
    
    #如果分支不是叶子节点，对其进行剪枝操作
    if tree.tb.results==None:
        prune(tree.tb, mingain)
    if tree.fb.results==None:
        prune(tree.fb, mingain)
        
    #如果两分支都是叶子节点，判断是否要合并
    if tree.tb.results!=None and tree.fb.results!=None:
        #构造合并后的数据集
        tb,fb=[],[]
        for v,c in tree.tb.results.items():
            tb+=[[v]]*c
        for v,c in tree.fb.results.items():
            fb+=[[v]]*c
        
        #检查熵的变化情况
        detal=entropy(tb+fb)-(entropy(tb)+entropy(fb))/2
        
        if detal<mingain:
            #合并分支
            tree.tb,tree.fb=None,None
            tree.results=uniqueCount(tb+fb)
                
        
class DecisionNode():
    def __init__(self,col=-1,value=None,resultes=None,tb=None,fb=None):
        #col 为 待检验的判断条件所对应的索引值
        #value对应为了使结果为true，当前列必须匹配的值
        #tb和fb也是DecisionNode，它们分别对应于结果为true或false时的子节点
        #results保存针对于当前分支的结果，他是一个字典，除叶子节点外，都改为None
        
        self.col=col
        self.value=value
        self.results=resultes
        self.tb=tb
        self.fb=fb
    
    