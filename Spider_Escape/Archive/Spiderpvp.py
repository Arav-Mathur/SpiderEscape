#https://www.programiz.com/python-programming/methods/built-in/enumerate 
import pygame as py
from Spiderman3 import Spiderman
from Spiderman3 import Webshooter
import random
#setup
py.init()
windowwidth = 1000
windowheight = 760
window = py.display.set_mode((windowwidth,windowheight))
clock = py.time.Clock()
#loop
window.fill("white")
pressed = False
webpressed = [False,"up"]
botpresses = []
bots = []
spider = Spiderman(windowwidth/2)
count = 0
gamestate = 1
lives = 3
touching = False
def mybot(i):
    global count,botpresses
    if count % int(random.randint(60,180)) == 0:
        botpresses[i] = not botpresses[i]
        count=0
        if botpresses[i]:
            bots[i].swing_init(random.randint(bots[i].rect.x-100,bots[i].rect.x+100),random.randint(100,windowheight-400))
        else:
            bots[i].yspeed = -0.2*bots[i].yspeed
    if bots[i].rect.x> windowwidth-100:
        botpresses[i] = True
    bots[i].run()
    if botpresses[i]:
        bots[i].swing()
        py.draw.line(window,(0,0,0),(bots[i].rect.x+30,bots[i].rect.y),(bots[i].mousex,bots[i].mousey))
    py.draw.rect(window,(0,0,0),bots[i].rect)

while True:
    ev = py.event.poll()
    if ev.type == py.QUIT:
        break
    key = py.key.get_pressed()
    window.fill("white")
    if gamestate == 1:
        #####player#####
        if ev.type == py.MOUSEBUTTONDOWN:
            if py.mouse.get_pressed()[0]:
                pressed = not pressed
                x,y = py.mouse.get_pos()
                if pressed:
                    spider.swing_init(x,y)
                else:
                    spider.yspeed = -0.2*spider.yspeed
            elif py.mouse.get_pressed()[2] and not webpressed[0]:
                print("otherone")
                x2,y2 = py.mouse.get_pos()
                webpressed[0]=True
                myweb = Webshooter(spider.rect.x,spider.rect.y,30,10)
                myweb.mousestart(x2,y2)
        spider.run()
        if pressed:
            spider.swing()
            py.draw.line(window,(255,0,0),(spider.rect.x+30,spider.rect.y),(spider.mousex,spider.mousey))
        if spider.rect.right>windowwidth-20 or spider.rect.x < 20:
            pressed = False
            spider.yspeed = 0
            spider.xspeed = -spider.xspeed
        touch=spider.rect.collidelistall(bots)
        if len(touch)>0:
            bots.pop(touch[0])
            pressed = False
            spider.yspeed = 0
            print("urded")
            lives-=1
            print(lives)
        if lives<=0 or spider.rect.y> windowheight:
            gamestate = 2
        py.draw.rect(window,(255,0,0),spider.rect)
        
        #####webs####
        if webpressed[0]:
            myweb.go()
            py.draw.rect(window,(255,0,0),myweb.web)
            if myweb.web.x>windowwidth or myweb.web.x<0 or myweb.web.y>windowheight or myweb.web.y<0:
                webpressed[0] = False
            x=myweb.web.collidelistall(bots)
            if len(x)>0:
                bots.pop(x[0])
                print("urded")
                webpressed[0] = False
                del myweb
                
        #####bot#####
        count+=1
        if count % 120 == 0:
            bots.append(Spiderman(random.randint(windowwidth/2-200,windowwidth/2+200)))
            count = 0
            botpresses.append(random.choice([True, False]))
        for i,bot in enumerate(bots):
            if bots[i].rect.y> windowheight:
                bots.remove(bots[i])
                continue
            mybot(i)
    elif gamestate ==2:
        print("ouch")
        del spider
        bots.clear()
        gamestate = 0
    py.display.flip()
    clock.tick(60)     
py.quit()