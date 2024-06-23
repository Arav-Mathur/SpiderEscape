import pygame as py
import numpy as np
from Spiderman2 import Spiderman
#setup
py.init()
windowwidth = 500
windowheight = 500
window = py.display.set_mode((windowwidth,windowheight))
py.display.set_caption("Arav's Spiderman Game") 
clock = py.time.Clock()

#images
#Load all images
daybg = py.image.load("assets/img/day bg.png") #all images are within image folder
#foreground = py.image.load("img/foreground.png") (unused feature) (may uncomment if you want to check it out)
nightsurface = py.image.load("assets/img/nightbg 3.jpg")
size = 1191 # size of background image
night = True # used for determining dark/light mode
startBack = py.image.load("assets/img/cover.jpg")
endBack = py.image.load("assets/img/cover2.png")
gray = py.Color(15, 42, 60)
white = py.Color(242, 242, 242)
nightx = 0.0
nighty = 0
nightx2 = size
#loop
window.fill("white")
pressed = False  
spider = Spiderman()
axisX,axisY=0.0,0.0

while True:
    ev = py.event.poll()
    if ev.type == py.QUIT:
        break
    key = py.key.get_pressed()
    if ev.type == py.MOUSEBUTTONDOWN:
        pressed = not pressed
        x,y = py.mouse.get_pos()
        if pressed:
            spider.swing_init(x,y,windowwidth/2)
            axisX=x
            axisy=y
        else:
            spider.yspeed = -0.2*spider.yspeed
    window.fill("white")
    #gamestate == 0
#     if night: # if setting is dark, make background a black image, else make it a white image
#         window.blit(startBack,(0,0))
#     else:
#         window.blit(endBack,(0,0))
    nightx+=spider.movedx
    axisX+= spider.movedx
    print("its positive")
    print(spider.movedx,spider.movedy)
    #nightx2=-spider.rect.x
    ####### move background in opposite direction by value not the exact location
#     if nightx < -size: # if background goes off the screen, loop back to the end
#         nightx = size
#     elif nightx > size:
#         nightx = -size
#     if nightx2 < -size:# if background goes off the screen, loop back to the end
#         nightx2 = size
#     elif nightx2 > size:
#         nightx2 = -size

    spider.run(windowheight)
    player = py.Rect(windowwidth/2,spider.rect.y,spider.rect.width,spider.rect.height)
    if night: # depending on light/dark setting, change background
        window.blit(nightsurface,(nightx,nighty))
        #window.blit(nightsurface,(nightx2,0))
    else:
        window.blit(daybg,(nightx,0))
        window.blit(daybg,(nightx2,0))
    py.draw.rect(window,(0,0,0),player)
    #py.draw.rect(window,(0,0,0),spider.rect)
    if pressed:
        spider.swing()
        py.draw.line(window,(0,0,0),(player.x+30,player.y),(axisX,spider.mousey))
    py.display.flip()
    clock.tick(60)     
py.quit()