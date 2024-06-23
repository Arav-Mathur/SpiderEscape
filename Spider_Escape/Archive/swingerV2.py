
import pygame as py
import numpy as np
#setup
py.init()
windowwidth = 1000
windowheight = 1000
window = py.display.set_mode((windowwidth,windowheight))
clock = py.time.Clock()
#loop
rext = 50
reyt = 50
yspeed = 2
xspeed = 2
pressed = False
window.fill("white")
while True:
    ev = py.event.poll()
    if ev.type == py.QUIT:
        break
    key = py.key.get_pressed()
    if ev.type == py.MOUSEBUTTONDOWN:
        pressed = not pressed
        x,y = py.mouse.get_pos()
        if pressed:
            angle = np.arctan2(y-reyt,x-rext-30)
            length = np.sqrt((x-rext-30)**2+(y-reyt)**2)
            opx = "-" if x>rext else "+"
            opy = "+" if x>rext else "+"
            anglespeed= 0
        else:
            yspeed = -0.2*yspeed
    window.fill("white")
    yspeed+=0.05
    reyt+=yspeed
    xspeed+=1/10000000000
    rext+=xspeed
    if reyt >= windowheight-50:
        reyt = windowheight-50
        yspeed = -0.4*yspeed # die here
    if pressed:
        rext = eval(str(x) + opx + str(length*(np.cos(np.radians(angle)))))
        reyt = eval(str(y) + opy + str(length*np.sin(np.radians(angle))))
        anglespeed+=0.005
        angle+=anglespeed
        py.draw.line(window,(0,0,0),(rext+30,reyt),(x,y))
        print(rext,reyt,angle)
    rect = [rext,reyt,30,40] #x,y,w,h
    py.draw.rect(window,(0,0,0),rect)
    py.display.flip()
    clock.tick(60)     
    
py.quit()

