import pygame as py
import numpy as np
from Spiderman import Spiderman
#setup
py.init()
windowwidth = 1000
windowheight = 760
window = py.display.set_mode((windowwidth,windowheight))
clock = py.time.Clock()
#loop
window.fill("white")
pressed = False  
spider = Spiderman()
while True:
    ev = py.event.poll()
    if ev.type == py.QUIT:
        break
    key = py.key.get_pressed()
    if ev.type == py.MOUSEBUTTONDOWN:
        pressed = not pressed
        x,y = py.mouse.get_pos()
        if pressed:
            spider.swing_init(x,y)
        else:
            spider.yspeed = -0.2*spider.yspeed
    window.fill("white")
    spider.run(windowheight)
    if pressed:
        spider.swing()
        py.draw.line(window,(0,0,0),(spider.rect.x+30,spider.rect.y),(spider.mousex,spider.mousey))
    py.draw.rect(window,(0,0,0),spider.rect)
    py.display.flip()
    clock.tick(60)     
py.quit()