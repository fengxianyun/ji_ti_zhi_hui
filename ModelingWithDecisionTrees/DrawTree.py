#coding:gbk
'''
Created on 2015��9��5��

@author: fxy
'''
from PIL import Image,ImageDraw
class DrawTree():
    '''
    classdocs
    '''


    def __init__(self, tree,path):
        '''
        Constructor
        '''
        self.tree=tree
        self.path=path
        
    
    def getWidth(self,tree):
        if tree==None:
            return 0
        if tree.tb==None and tree.fb==None:
            return 1
        return self.getWidth(tree.tb)+self.getWidth(tree.fb)
    
    def getDepth(self,tree):
        if tree==None:
            return 0
        if tree.tb==None and tree.fb==None:
            return 0
        return max(self.getDepth(tree.tb),self.getDepth(tree.tb))+1
    
    def drawTree(self):
        w=self.getWidth(self.tree)*100
        d=self.getDepth(self.tree)*200+120
        
        img=Image.new('RGB', (w,d), (255,255,255))
        draw=ImageDraw.Draw(img)
        
        self.drawNode(draw, self.tree, w/2, 20)
        img.save(self.path, 'JPEG')
        
    def drawNode(self,draw,tree,x,y):
        if tree.results==None:
            #�õ�ÿ����֧�Ŀ��
            w1=self.getWidth(tree.tb)*100
            w2=self.getWidth(tree.fb)*100
            
            #ȷ���˽ڵ���Ҫռ�ݵĿռ�
            left=x-(w1+w2)/2
            right=x+(w1+w2)/2
            
            #�����ж������ַ���
            draw.text((x-20,y-10),str(tree.col)+':'+str(tree.value),(0,0,0))
            
            #���Ƶ���֧������
            draw.line((x,y,left+w1/2,y+100),fill=(255,0,0))
            draw.line((x,y,right-w2/2,y+100),fill=(255,0,0))
            
            #���Ʒ�֧�ڵ�
            self.drawNode(draw, tree.tb, left+w1/2, y+100)
            self.drawNode(draw, tree.fb, right-w2/2, y+100)
        else:
            txt=' \n'.join(['%s:%d'%v for v in tree.results.items()])
            draw.text((x-20,y),txt,(0,0,0))