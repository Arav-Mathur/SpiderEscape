import pygame as py
import numpy as np
#setup
py.init()
clock = py.time.Clock()
class Spiderman:
    def __init__(self,myrext): #initialize object variables
        self.yspeed = 2.0
        self.xspeed = 1.0
        self.rect = py.Rect(myrext,50,30,40)
        self.movedx,self.movedy = 0,0
        self.anglestate= False
        self.angle,self.anglespeed, self.length = 0, 0,0
        self.mousex, self.mousey = 0,0
        
    def run(self): # allows him to stay in the air
        reyt = float(self.rect.y)
        rext = float(self.rect.x)
        self.yspeed+=0.05 # increasing gravity
        reyt+=self.yspeed
        self.xspeed+=1/10000000000 # increasing x position by very small amount
        rext+=self.xspeed 
        self.getmove(rext,reyt)
    def swing_init(self, x, y): #initialize swinging (runs once)
        self.yspeed = 0
        self.mousex = x
        self.mousey = y
        self.angle_init = np.arctan2(self.mousey - self.rect.y, self.mousex - self.rect.x - 30) # get angle between point and rectangle
        self.angle = self.angle_init
        self.length = np.sqrt((self.mousex - self.rect.x - 30) ** 2 + (self.mousey - self.rect.y) ** 2) # get initial length 
        self.anglespeed = 0.0
        self.anglestate = (self.mousex>self.rect.x)
        self.rect.x = self.mousex - self.length * np.cos(self.angle) # set it in that initial state in both x and y 
        self.rect.y = self.mousey - self.length * np.sin(self.angle)

    def swing(self):
        self.anglespeed = self.anglespeed-0.0001 if self.anglestate else self.anglespeed+0.0001 # switch left and right
        self.angle += self.anglespeed
        rext = self.mousex - self.length * np.cos(self.angle) # recalculate x value based on new angle
        reyt = self.mousey - self.length * np.sin(self.angle) # recalculate y value based on new angle 
        self.getmove(rext,reyt)
        
    def getmove(self,rext,reyt): # gets change in motion 
        self.movedx = rext-self.rect.x
        self.movedy = self.rect.y - reyt
        self.rect.x = rext
        self.rect.y = reyt
class Webshooter: #webshooter object
    def __init__(self,x,y,w,h): # initialize the rectangle when first created
        self.web = py.Rect(x,y,w,h)
    def mousestart(self,mousex,mousey):
        self.angle = np.arctan2(mousey - self.web.y, mousex - self.web.right)# get initial angle between mouse and rect
    def go(self):
        self.web.x += 10*np.cos(self.angle)# Keep increasing x value in that angle
        self.web.y += 10*np.sin(self.angle)# keep increasing y value in that angle