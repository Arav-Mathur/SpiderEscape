#https://www.pygame.org/docs/
#https://archive.org/details/spider-man-across-the-spider-verse-soundtrack-from-and-inspired-by-the-motion-instrumental-edition/Spider-Man+Across+The+Spider-Verse/Instrumental+Edition/01-Annihilate+(Instrumental).mp3
import pygame as py
import random
from pygame import mixer
#setup
py.init()
windowwidth = 500
windowheight = 500
window = py.display.set_mode((windowwidth,windowheight))
py.display.set_caption("Arav's Spiderman Game")
clock = py.time.Clock()

jump = py.mixer.Sound("sound/jump2.wav")
jump.set_volume(5.0)
click = py.mixer.Sound("sound/click.wav")
click.set_volume(5.0)
#climb = py.mixer.music.load("climb.mp3")

music = py.mixer.music.load("sound/01-Annihilate (Instrumental).mp3")
py.mixer.music.play(-1)

daybg = py.image.load("img/day bg.png")
#foreground = py.image.load("img/foreground.png")
nightsurface = py.image.load("img/nightbg 3.jpg")
night = True
milesm = py.image.load("img/milesrun.png")
milesj = py.image.load("img/miles4.png")
milesclimb = py.image.load("img/miles_morales.png")
startBack = py.image.load("img/cover.jpg")
endBack = py.image.load("img/cover2.png")

font1 = py.font.SysFont("Bernard MT",60)
font2 = py.font.SysFont("Bernard MT",25)
font4 = py.font.SysFont("Bernard MT",40)

font3 = py.font.Font("spiderfont.ttf",80)

gray = py.Color(15, 42, 60)
white = py.Color(242, 242, 242)
#fsurface = py.transform.scale_by(foreground,1)
size = 1191
buildings = [py.image.load("img/building1.png"),py.image.load("img/building2.png"),py.image.load("img/building3.png"),py.image.load("img/building4.png")]
mybuild = [random.choice(buildings),random.choice(buildings)]

gamestate = 0
mytime = 0
distance = 0
time = 0
timelimit = 30
highscore = 0
def animate(img,framewidth,numframes,framerate):
    global framecount,milesnum
    if framecount % framerate ==0:
        if(milesnum<numframes-1):
            milesnum+=1
            img.x += framewidth
        else:
            milesnum=0
            img.x =0
    framecount+=1
def build(rectangle,build):
    buildw,buildh = py.Surface.get_size(build)
    return py.transform.smoothscale(build,(buildw*(rectangle.width/buildw),buildh*(rectangle.height/buildh)))
def button(x,y,w,h,text):
    global mousepos
    button = py.draw.rect(window,gray,(x,y,w,h),0,10)
    window.blit(font1.render(text,1,white),(button.x+5,button.y+5))
    if pressed and button.collidepoint(mousepos):
            click.play()
            return True
def reset():
    global nightx,nightx2,size,yspeed,rect,milesloc,milesnum,framecount,air,edge,blockpos,blockpos2,blocks,mytime,distance,time,timeover#,frontx,frontx2
    #frontx = 0
    #frontx2 = size
    nightx = 0
    nightx2 = size
    yspeed = 2.0
    rect = py.Rect(100,150,30,44)
    milesloc = py.Rect(0,0,40,44)
    milesnum = 0
    framecount = 0
    air = False
    edge = False
    blocks = []
    blocks.clear()
    blockpos = py.Rect(0,random.randint(300,400),random.randint(250,400),200)#left,top,width,height
    blockpos.height = windowheight-blockpos.top
    blockpos2 = py.Rect(blockpos.right+random.randint(100,300),random.randint(250,400),random.randint(250,500),200)
    blockpos2.height = windowheight-blockpos2.top
    blocks = [blockpos,blockpos2]
    mytime = 0
    distance = 0
    time = 0
    timeover = False
reset()
while True:
    ev = py.event.poll()
    if ev.type == py.QUIT:
        break
    key = py.key.get_pressed()
    mousepos = py.mouse.get_pos()
    if ev.type == py.MOUSEBUTTONDOWN:
        pressed = True
    else:
        pressed = False
    window.fill("white")
    if gamestate == 0:#start
        if night:
            window.blit(startBack,(0,0))
        else:
            window.blit(endBack,(0,0))
        window.blit(font3.render("SPIDER JUMPER",1,white), (25,25))
        
        start = button((windowwidth-110)/2,170, 110,50,"Start")
        settings = button((windowwidth-180)/2,240, 180,50,"Settings")
        howtoplay = button((windowwidth-255)/2,300, 255,50,"How To Play")
        if start == True:
            reset()
            gamestate = 1
        elif settings == True:
            gamestate = 4
        elif howtoplay == True:
            gamestate = 3
    elif gamestate == 1: #play
        if key[py.K_d] == True and edge == False:
            nightx -=1
            nightx2 -=1
            #frontx-=3
            #frontx2-=3
            for i in range(len(blocks)):
                blocks[i].left -=10
            animate(milesloc,50,6,8)
            distance +=0.5
        yspeed+=0.2
        rect.top+=yspeed
        
        for i in range(len(blocks)):
            if rect.bottom+1 > blocks[i].top  and rect.left > blocks[i].left and rect.left < blocks[i].right:#and rect.bottom+1 < blocks[i].top +20
                yspeed = 0
                air = False
                edge = False
                rect.bottom = blocks[i].top           
                if (key[py.K_SPACE]):
                    yspeed = -5.5
                    jump.play()
                break
            elif rect.right > blocks[i].left and rect.right < blocks[i].right and rect.bottom > blocks[i].top+20:#and rect.right < blocks[i].left + 10
                yspeed = 0
                air = False
                edge = True
                if key[py.K_w] and key[py.K_SPACE] != True:
                    yspeed = -4.5
            elif rect.bottom< blocks[i].top:
                air = True
                edge = False
                break
        
        if blocks[0].right < 0:
            blocks.append(py.Rect(blocks[-1].right+random.randint(50,400),random.randint(250,400),random.randint(250,500),200))
            blocks[-1].height = windowheight-blocks[-1].top
            mybuild.append(random.choice(buildings))
            mybuild.pop(0)
            blocks.pop(0)
            
        if nightx < -size:
            nightx = size
        if nightx2 < -size:
            nightx2 = size
#         if frontx < -size:
#             frontx = size
#         if frontx2 < -size:
#             frontx2 = size
        if key[py.K_SPACE] == False and key[py.K_d] == False:
            milesloc.y = 0
            milesloc.x = 0
            animate(milesloc,50,1,10)
        
        if rect.bottom > windowheight:
            gamestate = 2
        if mytime > timelimit:
            gamestate = 2
            timeover = True
        elif time % 60 ==0:
            mytime +=1
            print(mytime,int(distance))
        time+=1
        #draw here
        if night:
            window.blit(nightsurface,(nightx,0))
            window.blit(nightsurface,(nightx2,0))
        else:
            window.blit(daybg,(nightx,0))
            window.blit(daybg,(nightx2,0))
#         window.blit(fsurface,(frontx,226))
#         window.blit(fsurface,(frontx2,226))
        for i in range(len(blocks)):
            block = build(blocks[i],mybuild[i])
            window.blit(block,blocks[i])
            py.draw.rect(window,(15, 42, 60),(blocks[i].left,blocks[i].top+20,10,blocks[i].height))
            py.draw.rect(window,(0,0,0),(blocks[i].left,blocks[i].top,blocks[i].width,20))
        if air:
            window.blit(milesj,(rect.x,rect.y))
        elif edge:
            window.blit(milesclimb,(rect.x,rect.y))
        else:
            window.blit(milesm,(rect.x,rect.y),milesloc)
        window.blit(font2.render("Time:",1,white),(10,10))
        window.blit(font2.render("Distance:",1,white),(10,30))
        window.blit(font2.render(str(timelimit-mytime)+ " s",1,white),(100,10))
        window.blit(font2.render(str(int(distance))+ " m",1,white),(100,30))
    elif gamestate == 2:#end screen
        print("endscreen")
        if night:
            window.blit(startBack,(0,0))
        else:
            window.blit(endBack,(0,0))
        window.blit(font3.render("GAME OVER",1,white), (80,25))
        speed = distance/mytime
        if speed >= highscore:
            highscore = speed
            window.blit(font2.render("New High Score!!",1,white),(100,200))
        if timeover:
            window.blit(font2.render("Time's Up!",1,white),(100,120))
        else:
            window.blit(font2.render("You Died!",1,white),(100,120))
        window.blit(font2.render("Distance:",1,white),(100,150))
        window.blit(font2.render("Speed:",1,white),(300,150))
        window.blit(font2.render("High Score:",1,white),(100,170))
        window.blit(font2.render(str(int(distance)) + " m",1,white),(200,150))
        window.blit(font2.render(str(int(speed)) + " m/s",1,white),(400,150))
        window.blit(font2.render(str(int(highscore))+ " m/s",1,white),(200,170))
        
        end = button((windowwidth-125)/2,240, 125,50,"Home")
        end2 = button((windowwidth-225)/2,300, 225,50,"Play Again")
        if end:
            gamestate = 0
        elif end2:
            reset()
            gamestate = 1
            
    elif gamestate == 3:
        print("how to play")
        if night:
            window.fill("black")
        else:
            window.fill("white")
        f = open("HowToPlay.txt", "r")
        window.blit(font2.render(f.read(),1,white),(15,15))
        f.close()
        
        back = button((windowwidth-110)/2,370, 110,50,"Back")
        if back:
            gamestate = 0

    elif gamestate == 4:
        print("Settings")
        if night:
            window.fill("black")
        else:
            window.fill("white")
        window.blit(font1.render("Settings",1,white),(50,20))
        window.blit(font4.render("Time Limit:",1,white),(50,100))
        window.blit(font1.render(str(timelimit),1,white),(325,100))
        
        plus = button(400,90, 40,50,"+")
        minus = button(250,90, 40,50,"-")
        back = button(100,370, 110,50,"Back")
        
        window.blit(font4.render("Background:",1,white),(50,150))
        #window.blit(font1.render(str(timelimit),1,white),(325,100))
        
        daybutton = button(380,150, 85,50,"Day")
        nightbutton = button(250,150, 120,50,"Night")
        if back:
            gamestate = 0
        elif plus and timelimit <99:
            timelimit+=1
        elif minus and timelimit >1:
            timelimit-=1
        elif daybutton:
            night = False
            gray = py.Color(242, 242, 242)
            white = py.Color(15, 42, 60)
        elif nightbutton:
            night = True
            gray = py.Color(15, 42, 60)
            white = py.Color(242, 242, 242)
    py.display.flip()
    clock.tick(60)
py.quit()