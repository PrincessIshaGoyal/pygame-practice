import pygame
from random import choice as choose
from numpy import genfromtxt,savetxt
from time import sleep

pygame.init()
special_fonts=['pristina','dubai','mvboli','mistral','juiceitc','timesnewroman','papyrus']
fonts=pygame.font.SysFont('arial',16)
fontn=pygame.font.SysFont('mvboli',30)
fontm=pygame.font.SysFont('arial',44)
fontb=pygame.font.SysFont('arial',70)
fontr=pygame.font.SysFont(choose(special_fonts),choose(range(20,80,10)))

def icon(name,size=[150,150],angle=0):
    image=pygame.image.load(r'C:\Users\ISHA\Desktop\mainig\{}.png'.format(name))
    image=pygame.transform.scale(image,size)
    image=pygame.transform.rotate(image,angle)
    return image

def block(size=[300,100],color=[255,255,255,120]):
    surf=pygame.Surface(size)
    surf=surf.convert_alpha()
    surf.fill(color)
    return surf

def write(sent,num,u=False):
    if(num>=0 and num<=130):
        if(num==13 or num==8):
            pass
        else:
            if(u):
                sent=sent+chr(num).upper()
            else:
                sent=sent+chr(num)
    return sent

def str_2_list(s,delimiter=' '):
    l=['']
    x=0
    for i in range(0,len(s)):
        if(s[i]==delimiter or s[i]=='\n'):
            x+=1
            l.append('')
        else:
            l[x]+=s[i]
    return l

class writelines:
    def __init__(self,multiline=False,font=['pristina',40,[0,0,0]],align='left',gap=5,uv=False):
        self.l=multiline
        self.gap=5
        self.align=align
        self.font=pygame.font.SysFont(font[0],font[1])
        self.font_size=font[1]
        self.color=font[2]
        self.text=['']
        self.ti=0
        self.u=uv

    def append(self,num):
        if(num==1073741881):
            self.u = not self.u
        elif(num==13 and self.l):
            self.ti+=1
            self.text.append('')
        elif(num==8 and len(self.text[self.ti])>0):
            t=self.text[self.ti]
            self.ti=''
            for i in range(0,len(t)-1):
                self.ti+=t[i]
        elif(num==8 and self.l and self.ti>0):
            self.ti-=1
        else:
            self.text[self.ti]=write(self.text[self.ti],num,self.u)

        if(self.l):
            self.size=[0,0]
            m=len(self.text[0])
            for i in range(0,self.ti+1):
                if(m<len(self.text[i])):
                    m=len(self.text[i])
            self.size[0]=m*self.font_size
            self.size[1]=(self.ti+1)*(self.font_size+(gap*2))
        else:
            self.size=[len(self.text[0])*self.font_size, self.font_size+(gap*2)]

        self.surf=pygame.Surface(self.size).convert_alpha()
        self.surf.fill([0,0,0,0])
        y=gap
        for i in range(0,self.ti+1):
            temp=font.render(self.text[i],True,self.color)
            if(align=='right'):
                self.surf.blit(temp,[self.size[0]-(len(self.text[i])*self.font_size),y])
            elif(align=='middle'):
                self.surf.blit(temp,[(self.size[0]-(len(self.text[i])*self.font_size))/2,y])
            else:
                self.surf.blit(temp,[0,y])
            y+=self.font_size+(gap*2)

    def see(self,size=[0,0]):
        if(size==[0,0]):
            size=self.size
        srf=pygame.Surface(size).convert_alpha()
        srf.fill([0,0,0,0])
        srf.blit(self.surf,[size[0]-self.size[0],size[1]-self.size[1]])
        return srf

class book:
    def __init__(self,name,cover_image='pink book cover',heading_text='timesnewroman',
                 write_name_on_cover=[True,[0,0,0]],size=[500,250]):
        self.size=size
        self.name=[name,write_name_on_cover[0],write_name_on_cover[1]]
        self.cover=icon(cover_image,[size[0]/2,size[1]])
        self.font=pygame.font.SysFont(heading_text,int(size[1]/10),bold=True)
        if(self.name[1]):
            txt=self.font.render(self.name[0],True,self.name[2])
            self.cover.blit(txt,[(size[0]/4)-(len(self.name[0])*len(self.name[2])/2),(size[0]/4)-(len(self.name[2])/2)])
        self.surf=pygame.Surface(size).convert_alpha()
##        self.surf.fill([0,0,0,0])
##        self.surf.blit(self.cover,[size[0]/2,size[1]])
        self.status='cover formed'

    def set_pages(self,design='plain',lines_per_page=10,page_color=[255,255,255],text_color=[0,0,0],text=['arial',16],
                     header={'left':'book name','middle':'empty','right':'chapter number','line':True},
                     footer={'middle':'page number','left':'chapter name','right':'empty','line':True}):
        self.page_number=0
        self.chapter=[0,'Index']
        self.page_size=[self.size[0]/2,self.size[1]]
        self.page_lines=lines_per_page
        self.page_design=design
        self.page_color=page_color
        self.text_color=text_color
        self.font2=pygame.font.SysFont(text[0],text[1])
        self.font2_size=text[1]
        self.header=header
        self.footer=footer
        self.status='ready to insert pages'
        
        self.x=int(self.page_size[0]/self.page_lines)
        self.y=int(self.page_size[1]/(self.page_lines+4))
        self.hfl={'left':self.x,'middle':self.page_size[0]/2,'right':self.page_size[0]-self.x,
                  'top':self.y,'bottom':self.page_size[1]-(self.y*2)+5,
                  'book name':self.name[0],'page number':self.page_number,'chapter number':self.chapter[0],'chapter name':self.chapter[1]
                  }

        if(design=='plain'):
            self.page=pygame.Surface(self.page_size)
            self.page.fill(self.page_color)
        elif(design=='lined'):
            self.page=pygame.Surface(self.page_size)
            self.page.fill(self.page_color)
            for i in range(0,self.page_lines):
                pygame.draw.line(self.page,self.text_color,[self.x,self.y*(i+2)],[self.page_size[0]-self.x,self.y*(i+2)],1)
        else:
            self.page=pygame.Surface(self.page_size)
            self.page.fill(self.page_color)
            self.page_design=icon(design,self.page_size)
            self.page.blit(self.page_design,[0,0])

        if(self.header['line']):
            pygame.draw.line(self.page,self.text_color,[self.x,self.y*2],[self.page_size[0]-self.x,self.y*2],3)

        if(self.footer['line']):
            pygame.draw.line(self.page,self.text_color,[self.x,self.y*(self.page_lines+3)],[self.page_size[0]-self.x,self.y*(self.page_lines+3)],3)

        self.cover_inside=pygame.transform.scale(self.cover,[(self.size[0]/2)+20,self.size[1]+20])
        temp=block([self.page_size[0]-self.x,self.page_size[1]-(self.y*2)],[255,255,255,200])
        self.cover_inside.blit(temp,[self.x+20,self.y+10])

    def get_index(self,design='plain',names=[]):
        self.surf.fill([0,0,0,0])
        self.status='at index'
        self.surf.blit(self.cover_inside,[-20,-10])

        if(design=='plain'):
            pg=pygame.Surface(self.page_size)
            pg.fill(self.page_color)
        else:
            pg=pygame.Surface(self.page_size)
            pg.fill(self.page_color)
            temp=icon(design,self.page_size)
            pg.blit(temp,[0,0])

        temp=self.font.render('Index',True,self.text_color)
        pg.blit(temp,[self.hfl['middle']-int((self.size[1]/40)*5),self.y+10])

        for i in range(len(names)):
            temp=self.font2.render(str(i+1)+'.'+' '*(4-len(str(i+1)))+names[i],True,self.text_color)
            pg.blit(temp,[self.x*2,self.y*(i+5)])

        self.surf.blit(pg,[self.size[0]/2,0])
        b=icon('b',[20,self.size[1]])
        self.surf.blit(b,[(self.size[0]/2)-10,0])
        return self.surf

    def chapter_up(self,name):
        self.chapter=[self.chapter[0]+1,name]
        self.hfl['chapter number']=self.chapter[0]
        self.hfl['chapter name']=self.chapter[1]
        self.status='at chapter '+str(self.chapter[0])

    def get_pages(self,headings=[None,None],description=[None,None],cost=[None,None],rewards=[None,None],completed=['y','n']):
        vl=0
        pg=self.page.copy()
        if(self.header['left'] in self.hfl):
            temp=fonts.render(str(self.hfl[self.header['left']]),True,self.text_color)
            pg.blit(temp,[self.hfl['left'],self.hfl['top']])
        if(self.header['middle'] in self.hfl):
            temp=fonts.render(str(self.hfl[self.header['middle']]),True,self.text_color)
            pg.blit(temp,[self.hfl['middle']-(4*len(str(self.hfl[self.header['middle']]))),self.hfl['top']])
        if(self.header['right'] in self.hfl):
            temp=fonts.render(str(self.hfl[self.header['right']]),True,self.text_color)
            pg.blit(temp,[self.hfl['right']-(8*len(str(self.hfl[self.header['right']]))),self.hfl['top']])

        if(self.footer['left'] in self.hfl):
            temp=fonts.render(str(self.hfl[self.footer['left']]),True,self.text_color)
            pg.blit(temp,[self.hfl['left'],self.hfl['bottom']])
        if(self.footer['middle'] in self.hfl):
            temp=fonts.render(str(self.hfl[self.footer['middle']]),True,self.text_color)
            pg.blit(temp,[self.hfl['middle']-(4*len(str(self.hfl[self.footer['middle']]))),self.hfl['bottom']])
        if(self.footer['right'] in self.hfl):
            temp=fonts.render(str(self.hfl[self.footer['right']]),True,self.text_color)
            pg.blit(temp,[self.hfl['right']-(8*len(str(self.hfl[self.footer['right']]))),self.hfl['bottom']])

        if(headings[vl]!=None):
            temp=self.font.render(headings[vl],True,self.text_color)
            pg.blit(temp,[self.hfl['middle']-int((self.size[1]/40)*len(headings[vl])),self.y-10])
        if(description[vl]!=None):
            text=str_2_list(description[vl])
            t=''
            x=0
            i=0
            while(i<len(text)):
                if(len(text[i]+t)<=(self.page_size[0]-(4*self.x))/(self.font2_size*2)):
                    t+=' '+text[i]
                    i+=1
                    continue
                temp=self.font2.render(t,True,self.text_color)
                pg.blit(temp,[2*self.x,self.y*(3+x)])
                x+=1
                t=''
            temp=self.font2.render(t,True,self.text_color)
            pg.blit(temp,[2*self.x,self.y*(3+x)])
            x+=1
            t=''
        if(rewards[vl]!=None):
            p=item_poster(rewards[vl])
            pg.blit(p,[self.x,self.page_size[1]-200])
            if(completed[vl]=='y'):
                pygame.draw.line(pg,[50,250,50],[self.x,self.page_size[1]-50],[self.x+50,self.page_size[1]-10],2)
                pygame.draw.line(pg,[50,250,50],[self.x+50,self.page_size[1]-10],[self.x+100,self.page_size[1]-100],2)
        if(cost[vl]!=None):
            h=block(self.page_size,[0,0,0,100])
            pg.blit(h,[0,0])
            p=item_poster(cost[vl])
            pg.blit(p,[self.page_size[0]-200,self.page_size[1]-200])

        self.page_number+=1
        self.hfl['page number']=self.page_number
        self.surf.blit(pg,[0,0])
        vl+=1

        pg=self.page.copy()
        if(self.header['left'] in self.hfl):
            temp=fonts.render(str(self.hfl[self.header['left']]),True,self.text_color)
            pg.blit(temp,[self.hfl['left'],self.hfl['top']])
        if(self.header['middle'] in self.hfl):
            temp=fonts.render(str(self.hfl[self.header['middle']]),True,self.text_color)
            pg.blit(temp,[self.hfl['middle']-(4*len(str(self.hfl[self.header['middle']]))),self.hfl['top']])
        if(self.header['right'] in self.hfl):
            temp=fonts.render(str(self.hfl[self.header['right']]),True,self.text_color)
            pg.blit(temp,[self.hfl['right']-(8*len(str(self.hfl[self.header['right']]))),self.hfl['top']])

        if(self.footer['left'] in self.hfl):
            temp=fonts.render(str(self.hfl[self.footer['left']]),True,self.text_color)
            pg.blit(temp,[self.hfl['left'],self.hfl['bottom']])
        if(self.footer['middle'] in self.hfl):
            temp=fonts.render(str(self.hfl[self.footer['middle']]),True,self.text_color)
            pg.blit(temp,[self.hfl['middle']-(4*len(str(self.hfl[self.footer['middle']]))),self.hfl['bottom']])
        if(self.footer['right'] in self.hfl):
            temp=fonts.render(str(self.hfl[self.footer['right']]),True,self.text_color)
            pg.blit(temp,[self.hfl['right']-(8*len(str(self.hfl[self.footer['right']]))),self.hfl['bottom']])

        if(headings[vl]!=None):
            temp=self.font.render(headings[vl],True,self.text_color)
            pg.blit(temp,[self.hfl['middle']-int((self.size[1]/40)*len(headings[vl])),self.y-10])
        if(description[vl]!=None):
            text=str_2_list(description[vl])
            t=''
            x=0
            i=0
            while(i<len(text)):
                if(len(text[i]+t)<=(self.page_size[0]-(4*self.x))/self.font2_size):
                    t+=' '+text[i]
                    i+=1
                    continue
                temp=self.font2.render(t,True,self.text_color)
                pg.blit(temp,[2*self.x,self.y*(3+x)])
                x+=1
                t=''
            temp=self.font2.render(t,True,self.text_color)
            pg.blit(temp,[2*self.x,self.y*(3+x)])
            x+=1
            t=''
        if(rewards[vl]!=None):
            p=item_poster(rewards[vl])
            pg.blit(p,[self.x,self.page_size[1]-200])
            if(completed[vl]=='y'):
                pygame.draw.line(pg,[50,250,50],[self.x,self.page_size[1]-50],[self.x+50,self.page_size[1]-10],2)
                pygame.draw.line(pg,[50,250,50],[self.x+50,self.page_size[1]-10],[self.x+100,self.page_size[1]-100],2)
        if(cost[vl]!=None):
            h=block(self.page_size,[0,0,0,100])
            pg.blit(h,[0,0])
            p=item_poster(cost[vl])
            pg.blit(p,[self.page_size[0]-200,self.page_size[1]-200])

        self.page_number+=1
        self.hfl['page number']=self.page_number
        self.surf.blit(pg,[self.size[0]/2,0])
        pygame.draw.line(self.surf,[230,230,230],[self.size[0]/2,0],[self.size[0]/2,self.size[1]],3)
        return self.surf

screen=pygame.display.set_mode([600,600],pygame.RESIZABLE)
screen.fill([255,100,100])
loading=fontr.render('Loading...',True,[255,255,255])
screen.blit(loading,[0,0])
pygame.display.flip()
pygame.display.set_caption('Mainig')
imge=pygame.image.load(r'C:\Users\ISHA\Desktop\mainig\Butterfly.png')
pygame.display.set_icon(imge)
pygame.display.flip()

a=book('My First Book')
a.set_pages()
p=a.get_index(names=['One','Two','Three'])
screen.blit(p,[20,20])
pygame.display.flip()

a.chapter_up('One')
p=a.get_pages(['One',None],["Welcome to my first book's page 'One'","Have a nice day"])
screen.blit(p,[20,20])
pygame.display.flip()
