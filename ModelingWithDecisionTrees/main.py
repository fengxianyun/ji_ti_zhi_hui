#coding:gbk
'''
Created on 2015��9��5��

@author: fxy
'''
import treepredict
import data
import DrawTree

# #����divideSet
# print treepredict.divideSet(data.my_data, 2, "yes")

# #���Ծ���ѵ���󣬻��᲻���Ⱥ��صı仯
# print treepredict.giniImpurity(data.my_data)
# print treepredict.entropy(data.my_data)
# set1,set2=treepredict.divideSet(data.my_data, 2, "yes")
# print treepredict.giniImpurity(set1)
# print treepredict.entropy(set1)

# #����buildTree
# tree=treepredict.buildTree(data.my_data)
# draw=DrawTree.DrawTree(tree,'treeview.jpg')
# draw.drawTree()

# #ʹ��classify��������Ԥ��
# tree=treepredict.buildTree(data.my_data)
# print treepredict.classify(['(direct)','USA','yes',5], tree)

#���Լ�֦����������ͼ
tree=treepredict.buildTree(data.my_data)
treepredict.prune(tree, 1.0)
draw=DrawTree.DrawTree(tree,'treeview2.jpg')
draw.drawTree()

# #ʹ��mdclassify��������Ԥ��
tree=treepredict.buildTree(data.my_data)
print treepredict.classify(['(direct)','USA','yes',5], tree)
print treepredict.mdclassify(['google',None,'yes',None], tree)
print treepredict.mdclassify(['google','France',None,None], tree)