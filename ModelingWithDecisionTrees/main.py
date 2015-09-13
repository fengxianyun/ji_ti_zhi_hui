#coding:gbk
'''
Created on 2015年9月5日

@author: fxy
'''
import treepredict
import data
import DrawTree

# #测试divideSet
# print treepredict.divideSet(data.my_data, 2, "yes")

# #测试经过训练后，基尼不纯度和熵的变化
# print treepredict.giniImpurity(data.my_data)
# print treepredict.entropy(data.my_data)
# set1,set2=treepredict.divideSet(data.my_data, 2, "yes")
# print treepredict.giniImpurity(set1)
# print treepredict.entropy(set1)

# #测试buildTree
# tree=treepredict.buildTree(data.my_data)
# draw=DrawTree.DrawTree(tree,'treeview.jpg')
# draw.drawTree()

# #使用classify函数进行预测
# tree=treepredict.buildTree(data.my_data)
# print treepredict.classify(['(direct)','USA','yes',5], tree)

#尝试剪枝函数，并绘图
tree=treepredict.buildTree(data.my_data)
treepredict.prune(tree, 1.0)
draw=DrawTree.DrawTree(tree,'treeview2.jpg')
draw.drawTree()

# #使用mdclassify函数进行预测
tree=treepredict.buildTree(data.my_data)
print treepredict.classify(['(direct)','USA','yes',5], tree)
print treepredict.mdclassify(['google',None,'yes',None], tree)
print treepredict.mdclassify(['google','France',None,None], tree)