#coding:gbk
'''
Created on 2015年8月30日

@author: fxy
'''
import math
import PIL.Image as Image,PIL.ImageDraw as ImageDraw
people=['Charlie','Augustus','Veruca','Violet','Mike','Joe','Willy','Miranda']

links=[('Augustus', 'Willy'), 
       ('Mike', 'Joe'), 
       ('Miranda', 'Mike'), 
       ('Violet', 'Augustus'), 
       ('Miranda', 'Willy'), 
       ('Charlie', 'Mike'), 
       ('Veruca', 'Joe'), 
       ('Miranda', 'Augustus'), 
       ('Willy', 'Augustus'), 
       ('Joe', 'Charlie'), 
       ('Veruca', 'Augustus'), 
       ('Miranda', 'Joe')]

def crosscount(v):
    #将数字序列转换为person:(x,y)的字典
    loc=dict([(people[i],(v[i*2],v[i*2+1])) for i in range(0,len(people))])
    total=0
    
    #遍历每一对连线
    for i in range(len(links)):
        for j in range(i+1,len(links)):
            
            #获取坐标位置
            (x1,y1),(x2,y2)=loc[links[i][0]],loc[links[i][1]]
            (x3,y3),(x4,y4)=loc[links[j][0]],loc[links[j][1]]
            
            den=(y4-y3)*(x2-x1)-(x4-x3)*(y2-y1)
            
            #如果两线平行则den==0
            if den==0:
                continue
            ua=((x4-x3)*(y1-y3)-(y4-y3)*(x1-x3)+0.0)/den
            ub=((x2-x1)*(y1-y3)-(y2-y1)*(x1-x3)+0.0)/den
            
            if ua>0 and ua<1 and ub>0 and ub<1:
                total+=1
    for i in range(len(people)):
        for j in range(i+1,len(people)):
            #获得两节点位置
            (x1,y1),(x2,y2)=loc[people[i]],loc[people[j]]
            
            #计算两节点间距
            dist=math.sqrt(math.pow(x1-x2, 2)+math.pow(y1-y2, 2))
            #对间距小于50个像素点的节点判罚
            if dist<50:
                total+=(1.0-(dist/50.0))
    print total
    return total

def drawNetWork(sol):
    #建立image对象
    img=Image.new('RGB',(400,400),(255,255,255))
    draw=ImageDraw.Draw(img)
    
    #建立标示位置的字典
    pos=dict([(people[i],(sol[i*2],sol[i*2+1])) for i in range(0,len(people))])
    
    #绘制连线
    for(a,b)in links:
        draw.line((pos[a],pos[b]), fill=(255,0,0))
        
    #绘制代表人的节点
    for n,p in pos.items():
        draw.text(p, n, (0,0,0))
    img.save('fp.jpg', 'JPEG')
    img.show()
domain=[(10,370)]*(len(people)*2)

