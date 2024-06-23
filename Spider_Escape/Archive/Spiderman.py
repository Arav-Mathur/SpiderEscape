
import pygame as py
import numpy as np
#setup
py.init()
clock = py.time.Clock()
class Spiderman:
    def __init__(self,myrext):
        self.yspeed = 2
        self.xspeed = 2
        self.rect = py.Rect(myrext,50,30,40)
        self.movedx = 0
        self.movedy = 0
    def run(self,windowheight):
        reyt = self.rect.y
        rext = self.rect.x
        self.yspeed+=0.05
        reyt+=self.yspeed
        self.xspeed+=1/10000000000
        rext+=self.xspeed
        if self.rect.y >= windowheight-50:
            reyt = windowheight-50
            self.yspeed = -0.4*self.yspeed # die here
        self.getmove(rext,reyt)
    def checkcollide(self,windowheight):
        if spider.rect.y> windowheight:
            return 2
    def swing_init(self,x,y):
        self.yspeed = 0
        self.mousex = x
        self.mousey = y
        self.angle = np.arctan2(self.mousey-self.rect.y,self.mousex-self.rect.x-30)
        self.length = np.sqrt((self.mousex-self.rect.x-30)**2+(self.mousey-self.rect.y)**2)
        self.opx = "-" if self.mousex>self.rect.x else "+"
        self.opy = "+" if self.mousex>self.rect.x else "+"
        self.anglespeed= 0
    def swing(self):
        rext = eval(str(self.mousex) + self.opx + str(self.length*(np.cos(np.radians(self.angle)))))
        reyt = eval(str(self.mousey) + self.opy + str(self.length*np.sin(np.radians(self.angle))))
        self.getmove(rext,reyt)
        self.anglespeed+=0.005
        self.angle+=self.anglespeed
        #self.angle+=1
    def getmove(self,rext,reyt):
        self.movedx = rext-self.rect.x
        self.movedy = self.rect.y - reyt
        self.rect.x = rext
        self.rect.y = reyt
        self.rect.y = reyt

class Webshooter:
    def __init__(self,x,y,w,h):
        self.web = py.Rect(x,y,w,h)
    def start(self,direction):
        if direction == "up":
            self.web.y-=10
        elif direction == "down":
             self.web.y+=10
        elif direction == "left":
             self.web.x-=10
        elif direction == "right":
             self.web.x+=10        