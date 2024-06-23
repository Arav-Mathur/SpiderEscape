import pygame as py
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
nightx = 0
nightx2 = size
#loop
window.fill("white")
pressed = False  
spider = Spiderman(windowwidth/2)
axisX,axisY=0,0

while True:
    ev = py.event.poll()
    if ev.type == py.QUIT:
        break
    key = py.key.get_pressed()
    if ev.type == py.MOUSEBUTTONDOWN:
        pressed = not pressed
        x,y = py.mouse.get_pos()
        if pressed:
            axisX=x
            axisy=y
            py.draw.circle(window,(255,0,0),(axisX,axisy),10)
            spider.swing_init(axisX,y,windowwidth/2)
        else:
            spider.yspeed = -0.2*spider.yspeed
    window.fill("white")
    
    #gamestate == 0
#     if night: # if setting is dark, make background a black image, else make it a white image
#         window.blit(startBack,(0,0))
#     else:
#         window.blit(endBack,(0,0))
    #nightx = windowwidth/2 - spider.rect.x
#     nighty+=spider.movedy
    #print(spider.movedx,spider.movedy,spider.rect.x)
    #nightx2=-spider.rect.x
    ####### move background in opposite direction by value not the exact location
    nightx+=spider.movedx
    nightx2+=spider.movedx
    if nightx < -size: # if background goes off the screen, loop back to the end
        nightx = size
        print("hello")
    elif nightx > size:
        print("venom killed you!")
# #     else:
# #         nightx = windowwidth/2 - spider.rect.x
    if nightx2 < -size:# if background goes off the screen, loop back to the end
        nightx2 = size
        print("bye")
#     else:
#         nightx2 = nightx + size
    spider.run(windowwidth/2,windowheight)
    player = py.Rect(windowwidth/2,spider.rect.y,spider.rect.width,spider.rect.height)
    if night: # depending on light/dark setting, change background
         window.blit(nightsurface, (nightx, 0))
         window.blit(nightsurface,(nightx2,0))
         window.blit(nightsurface,(nightx-size,0))
    else:
        window.blit(daybg,(nightx,0))
        window.blit(daybg,(nightx2,0))
    py.draw.rect(window,(0,0,0),player)
    #py.draw.rect(window,(0,0,0),spider.rect)
    if pressed:
        
        spider.swing(nightx+axisX)
        py.draw.line(window,(0,0,0),(player.x+30,spider.rect.y),(nightx+axisX,spider.mousey))
        #py.draw.line(window,(0,0,0),(spider.rect.x,spider.rect.y),(spider.mousex,spider.mousey))
    py.display.flip()
    clock.tick(60)     
py.quit()