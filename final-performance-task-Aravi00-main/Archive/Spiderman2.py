
import pygame as py
import numpy as np
#setup
py.init()
# windowwidth = 1000
# windowheight = 1000
# #window = py.display.set_mode((windowwidth,windowheight))
clock = py.time.Clock()
#loop
# window.fill("white")
class Spiderman:
    def __init__(self,x):
        self.yspeed = 2
        self.xspeed = 2
        self.rect = py.Rect(x,50,30,40)
        self.movedx = 0
        self.movedy = 0
    def run(self,windowwidth,windowheight):
        reyt = self.rect.y
        rext = self.rect.x
        #rext = windowwidth
        self.yspeed+=0.05
        reyt+=self.yspeed
        self.xspeed+=1/10000000000
        rext+=self.xspeed
        if self.rect.y >= windowheight-50:
            reyt = windowheight-50
            self.yspeed = -0.4*self.yspeed # die here
        self.getmove(rext,reyt)
    def swing_init(self,x,y,rext):
        self.mousex = x
        self.mousey = y
        self.angle = np.arctan2(self.mousey-self.rect.y,self.mousex-(self.rect.x-30))
        self.length = np.sqrt((self.mousex-self.rect.x+30)**2+(self.mousey-self.rect.y)**2)
        self.opx = "-" if self.mousex>self.rect.x else "+"
        self.opy = "+" if self.mousex>self.rect.x else "+"
        self.anglespeed= 0
        print(self.angle)
        
    def swing(self,mouse):
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