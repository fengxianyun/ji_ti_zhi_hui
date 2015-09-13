#coding:gbk
'''
Created on 2015 7 16 

@author: fxy
'''
if __name__ == '__main__':
    pass
from recommendations import  *
from ou_ji_li_de_ju_li import sim_distance
from pi_er_xun_xiang_guan_du import sim_pearson
from tui_jian import *

print(topMatches(transfromPrefs(critics), 'Lady in the Water'))
print(getRecommendations(critics, 'Toby',sim_pearson))
print(topMatches(critics, 'Toby', 3))    
print(sim_distance(critics, 'Lisa Rose', 'Claudia Puig'))
print(sim_pearson(critics, 'Lisa Rose', 'Claudia Puig'))