import pygame as py
import random
#setup
py.init()
windowwidth = 500
windowheight = 500
window = py.display.set_mode((windowwidth,windowheight))
clock = py.time.Clock()

nightbg = py.image.load("nightbg.jpg")
nightbg2 = py.image.load("nightbg 3.jpg")
daybg = py.image.load("day bg.png")
foreground = py.image.load("foreground.png")
nightsurface = py.transform.scale_by(nightbg2,1)
fsurface = py.transform.scale_by(foreground,2)
size = 1191
nightx = 0
nightx2 = size
nightx3 = -size
#loop
rext = 250
reyt =50
yspeed = 2
touching = False
random = random.randint(100,500)
blockpos = [0,350,random,500-350]
while True:
    ev = py.event.poll()
    if ev.type == py.QUIT:
        break
    key = py.key.get_pressed()
    if ev.type == py.MOUSEBUTTONUP:
        pressed = True
        x,y = py.mouse.get_pos()
        print(x,y)
    else:
        pressed = False
    if (key[py.K_SPACE] or key[py.K_w]) and touching == True:
        print("jump")
        yspeed = -7.5
    if key[py.K_d]:
        print("right")
        rext+=5
    if key[py.K_a]:
        print("left")
        rext -= 5
        
    window.fill("white")
        
    yspeed+=0.25
    reyt+=yspeed
    if reyt+40 > blockpos[1] and rext < blockpos[0]+blockpos[2]:
        yspeed = 0
        reyt = blockpos[1]-40#-blockpos[3]
        touching = True
    else:
        touching = False
    
    if rext > windowwidth:
        rext = 0
    elif rext < 0:
        rext = windowwidth
    
    rect = [rext,reyt,30,40] #x,y,w,h
    #draw here
    py.draw.rect(window,(0,0,0),rect)
    py.draw.rect(window,(255,0,0),blockpos)
    py.display.flip()
    clock.tick(60)
py.quit()