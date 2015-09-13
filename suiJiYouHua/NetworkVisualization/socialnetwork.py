#coding:gbk
'''
Created on 2015��8��30��

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
    #����������ת��Ϊperson:(x,y)���ֵ�
    loc=dict([(people[i],(v[i*2],v[i*2+1])) for i in range(0,len(people))])
    total=0
    
    #����ÿһ������
    for i in range(len(links)):
        for j in range(i+1,len(links)):
            
            #��ȡ����λ��
            (x1,y1),(x2,y2)=loc[links[i][0]],loc[links[i][1]]
            (x3,y3),(x4,y4)=loc[links[j][0]],loc[links[j][1]]
            
            den=(y4-y3)*(x2-x1)-(x4-x3)*(y2-y1)
            
            #�������ƽ����den==0
            if den==0:
                continue
            ua=((x4-x3)*(y1-y3)-(y4-y3)*(x1-x3)+0.0)/den
            ub=((x2-x1)*(y1-y3)-(y2-y1)*(x1-x3)+0.0)/den
            
            if ua>0 and ua<1 and ub>0 and ub<1:
                total+=1
    for i in range(len(people)):
        for j in range(i+1,len(people)):
            #������ڵ�λ��
            (x1,y1),(x2,y2)=loc[people[i]],loc[people[j]]
            
            #�������ڵ���
            dist=math.sqrt(math.pow(x1-x2, 2)+math.pow(y1-y2, 2))
            #�Լ��С��50�����ص�Ľڵ��з�
            if dist<50:
                total+=(1.0-(dist/50.0))
    print total
    return total

def drawNetWork(sol):
    #����image����
    img=Image.new('RGB',(400,400),(255,255,255))
    draw=ImageDraw.Draw(img)
    
    #������ʾλ�õ��ֵ�
    pos=dict([(people[i],(sol[i*2],sol[i*2+1])) for i in range(0,len(people))])
    
    #��������
    for(a,b)in links:
        draw.line((pos[a],pos[b]), fill=(255,0,0))
        
    #���ƴ����˵Ľڵ�
    for n,p in pos.items():
        draw.text(p, n, (0,0,0))
    img.save('fp.jpg', 'JPEG')
    img.show()
domain=[(10,370)]*(len(people)*2)

