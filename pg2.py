import pygame
from time import sleep
pygame.init()
screen=pygame.display.set_mode([600,600])
screen.fill([255,255,255])
image=pygame.image.load(r'C:\Users\ISHA\Desktop\mainig\Art.png')
#image=pygame.transform.scale(image,[500,500])
i=pygame.Surface([500,500]).convert_alpha()
for x in range(255,0,-1):
    screen.fill([255,255,255])
    image=pygame.image.load(r'C:\Users\ISHA\Desktop\mainig\Art.png')
    i.fill([0,0,0,x])
    pygame.draw.line(i,[0,0,0,x],[0,0],[500,500],5)
    image.blit(i,[0,0])
    screen.blit(image,[50,50])
    pygame.display.flip()
    sleep(0.1)
