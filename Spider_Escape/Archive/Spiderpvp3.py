#https://www.programiz.com/python-programming/methods/built-in/enumerate 
import pygame as py
from Spiderman4 import Spiderman
from Spiderman4 import Webshooter
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

#foreground = py.image.load("img/foreground.png") (unused feature) (may uncomment if you want to check it out)
daysurface = py.transform.scale_by(py.image.load("assets/img/daybg2.jpg"),windowheight/900)
nightsurface = py.transform.scale_by(py.image.load("assets/img/nightbg2.jpg"),windowheight/1442)
size = 1191 # size of background image
night = False # used for determining dark/light mode
cover = py.transform.scale_by(py.image.load("assets/img/cover.jpg"),windowwidth/500)
cover2 = py.transform.scale_by(py.image.load("assets/img/cover2.png"),windowwidth/500)
milesj = py.image.load("assets/img/milesjump.png")
miless = py.image.load("assets/img/mileswing2.png")
botj = py.image.load("assets/img/spiderj.png")
botswing = py.image.load("assets/img/spiderswing.png")

font1 = py.font.SysFont("Calibri",20)

time = 0
mytime = 0
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
        py.draw.line(window,(0,0,0),(bots[i].rect.x+5,bots[i].rect.y),(bots[i].mousex,bots[i].mousey))
    #py.draw.rect(window,(0,0,0),bots[i].rect)
    if botpresses[i]:
        if not bots[i].anglestate:
            window.blit(py.transform.flip(botswing,True,False),(bots[i].rect.topleft))
        else:
            window.blit(botswing,(bots[i].rect.topleft))
    else:
        window.blit(botj,(bots[i].rect.topleft))
while True:
    ev = py.event.poll()
    if ev.type == py.QUIT:
        break
    key = py.key.get_pressed()
    window.fill("white" )
    if gamestate == 0:
        if night:
            window.blit(cover,(0,-100))
        else:
            window.blit(cover2,(0,-100))
    if gamestate == 1:
        #####player#####
        if night:
            window.blit(nightsurface,(-350,0))
        else:
            window.blit(daysurface,(0,0))
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
        window.blit(font1.render("Lives Left: "+str(lives),1,(0,0,0)),(25,50))
        if time % 60 ==0: # increase mytime every 1 second
            mytime +=1
        time+=1
        window.blit(font1.render("Time(sec): "+str(mytime),1,(0,0,0)),(25,70))
        spider.run()
        if pressed:
            spider.swing()
            py.draw.line(window,(255,0,0),(spider.rect.x+15,spider.rect.y),(spider.mousex,spider.mousey))
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
        if pressed:
            if not spider.anglestate:
                window.blit(py.transform.flip(miless,True,False),(spider.rect.topleft))
            else:
                window.blit(miless,(spider.rect.topleft))
        else:
            window.blit(milesj,(spider.rect.topleft))
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
        window.blit(cover,(0,0))
        print("ouch")
        del spider
        bots.clear()
        gamestate = 0
    py.display.flip()
    clock.tick(60)     
py.quit()
