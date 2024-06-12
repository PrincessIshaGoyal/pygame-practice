done=['Food sheet','Candy sheet','Beverage sheet','Gift boxes','Sweet boxes','Remaining food','Specials']

# Handle with care ;) #
name=''
itemid=000

from numpy import savetxt
import pygame
pygame.init()

def box(size):
    size=list(size)
    if(size[0]<0):
        size[0]*=-1
    if(size[1]<0):
        size[1]*=-1
    surf=pygame.Surface(size).convert_alpha()
    surf.fill([50,50,250,100])
    return surf

font=pygame.font.SysFont('arial',20)
screen=pygame.display.set_mode([600,600])
image=pygame.image.load(r'C:\Users\ISHA\Desktop\mainig\{}.png'.format(name))
image=pygame.transform.scale(image,[600,600])
screen.blit(image,[0,0])
pygame.display.update()

ls=[]
clicks=0
pos_p=(0,0)
rect_p=(0,0)
rect_s=(0,0)
ds=0
pe=0
run=True
while run:
    screen.fill([0,0,0])
    screen.blit(image,[0,0])
    b=box(rect_s)
    screen.blit(b,rect_p)
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False
        elif event.type==pygame.MOUSEBUTTONDOWN:
            clicks+=1
            pos_n=pygame.mouse.get_pos()
            if(pos_n!=pos_p):
                if(clicks>1):
                    pe=1
                else:
                    pe=0
                ds=0
                clicks=0
                pos_p=pos_n
            else:
                if(clicks>0):
                    rect_p=pos_n
                    ds=1
        elif event.type==pygame.KEYDOWN and event.key==13 and pe==1:
            pe=0
            ls.append([itemid,rect_p[0],rect_p[1],rect_s[0],rect_s[1]])
            itemid+=1
    if(ds==1):
        pos=pygame.mouse.get_pos()
        rect_s=(pos[0]-rect_p[0],pos[1]-rect_p[1])
    
pygame.quit()
savetxt('{}.csv'.format(name),ls,fmt='%d',delimiter=',')
