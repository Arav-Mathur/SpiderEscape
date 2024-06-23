#-----------------------------------------------------------------------------
# Program Name: SPIDER ESCAPE
# Purpose: Create a spiderman game to swing around in! 
#
# Author:      Arav Mathur
# Created:     01/24/2024
# Updated:     01/24/2024
#-----------------------------------------------------------------------------
#I think this project deserves a level 4+ because ...
#Features Added Above Level 3 Expectations:
# well polished + common theme
# The game has no bugs.
# The game has elements of randomness and replayability.
# The game has animated sprites
# The game has advanced coding techniques
# The game has multiple game modes
# The game has settings for creating a better user experience including increasing time limit + lives + dark/light mode
# The student has created all code themselves
#-----------------------------------------------------------------------------
#References:
#https://www.pygame.org/docs/
#https://www.programiz.com/python-programming/methods/built-in/enumerate 
#https://archive.org/details/spider-man-across-the-spider-verse-soundtrack-from-and-inspired-by-the-motion-instrumental-edition/Spider-Man+Across+The+Spider-Verse/Instrumental+Edition/01-Annihilate+(Instrumental).mp3
#Credit: Spiderman Into the spiderverse, Spiderman Across the Spiderverse
import pygame as py # initialize pygame
from Spiderman3 import Spiderman # import spiderman object from file
from Spiderman3 import Webshooter# import webshooter object from file
import random, math # import basic python libraries
#*********SETUP**********
py.init() #init pygame
#variables to set the size of the window

windowwidth = 1000 
windowheight = 760
window = py.display.set_mode((windowwidth,windowheight))#create the window
py.display.set_caption("Spider Escape")  
clock = py.time.Clock()  #will allow us to set framerate

# load possible backgrounds + create array containing all of them
backgrounds = [py.transform.scale_by(py.image.load("assets/img/daybg2.jpg"),windowheight/900),
               py.transform.scale_by(py.image.load("assets/img/nightbg2.jpg"),windowheight/1442),
               py.transform.scale_by(py.image.load("assets/img/day bg.png"),windowheight/500),
               py.transform.scale_by(py.image.load("assets/img/nightbg 3.jpg"),windowheight/500)]
night = True # used for determining dark/light mode
#Load all images #all images are within assets/img folder
webimg = py.image.load("assets/img/web.png")
webshotimg = py.image.load("assets/img/webshot.png")
cover = py.transform.scale_by(py.image.load("assets/img/cover.jpg"),windowwidth/500) #scale background size fit the screen
cover2 = py.transform.scale_by(py.image.load("assets/img/cover2.png"),windowwidth/500)
milesj = py.image.load("assets/img/milesjump.png")
miless = py.image.load("assets/img/mileswing2.png")
botj = py.image.load("assets/img/spiderj.png")
botswing = py.image.load("assets/img/spiderswing.png")
#load all fonts
font1 = py.font.SysFont("Calibri",20)
font2 = py.font.Font("assets/spiderfont.ttf",120)
font4 = py.font.Font("assets/spiderfont.ttf",60)
font3 = py.font.SysFont("Calibri",40)
 #Load all sounds + music
thwip = py.mixer.Sound("assets/sound/click.wav")
thwip.set_volume(1.0)
shoot = py.mixer.Sound("assets/sound/climb.wav")
shoot.set_volume(1.0)
py.mixer.pre_init(44100,-16,2,2048)
py.mixer.init()
music = py.mixer.music.load("assets/sound/01-Annihilate (Instrumental).mp3")
py.mixer.music.play(-1)
#Load colors
white = py.Color(255,255,255)
black = py.Color(0,0,0)
#initialize variables that stay constant despite the replaying of the game. (remaining are in reset function)
gamestate = 0
mode = "shooter"
timelimit = 30
maxlives = 3
highscore = 0
hightime =0
playmusic = False
playsound = True
def reset(): #initialize all the variables in a function (make sure it is global otherwise cannot use elsewhere)
    global pressed,webpressed,botpresses,bots,spider,count,touching,webreload,webs,trapped,time,mytime,lives
    pressed = False
    webpressed = False
    botpresses = []
    bots = []
    spider = Spiderman(windowwidth/2) # creates an instance of my main spiderman
    count = 0
    touching = False
    webreload = 0
    webs = []
    trapped = 0
    time = 0
    mytime = 0
    lives = maxlives
reset() # run function initially
def button(x,y,w,h,text,font):# creates a button with text inside using given parameters
    global mousepos,gamestate,white
    button = py.draw.rect(window,white,(x,y,w,h),0,10) # creates button rectangle using <x,y,w,h>
    mytext = font.render(text,1,black) # render text onto screen
    loc = mytext.get_rect(center=(button.right-(button.width/2),button.top+23)) # centers the text on the button
    window.blit(mytext,loc) # adds text to the center
    if ev.type == py.MOUSEBUTTONDOWN and button.collidepoint(mousepos): # collidepoint checks if the mouse pointer is inside the rectangle
        if text == "Back": # a special case that is built in so that i dont have to program back button all the time
            gamestate = 0 # start screen
        return True # button = true, this can be used for what happens when button is clicked
def mybot(i): # generates all the bots and runs calculations for each one 
    global count,botpresses
    if count % int(random.randint(60,180)) == 0: # every few seconds, stop or start swinging
        botpresses[i] = not botpresses[i] # switch between true and false
        count=0 #reset
        if botpresses[i]: # if true : initialize swinging, look at object
            bots[i].swing_init(random.randint(bots[i].rect.x-100,bots[i].rect.x+100),random.randint(100,windowheight-400)) 
        else:
            bots[i].yspeed = -0.2*bots[i].yspeed # gives it a jump release effect
    if bots[i].rect.right>windowwidth or bots[i].rect.x < 0: # if collides with side walls, bounce off
        bots[i].yspeed = -0.2*bots[i].yspeed # gives an upward jumping effect
        bots[i].xspeed = -bots[i].xspeed # switch direction of movement
        botpresses[i] = False # stop swinging 
        
    bots[i].run() # maintain air when not swinging
    if botpresses[i]:
        bots[i].swing() # swinging, look at object
        py.draw.line(window,(255,255,255),(bots[i].rect.x+5,bots[i].rect.y),(bots[i].mousex,bots[i].mousey),2) #draw the swinging line
        if not bots[i].anglestate: # change image whether swinging or jumping. also flip the image if swinging left/right to face correctly
            window.blit(py.transform.flip(botswing,True,False),(bots[i].rect.topleft))
        else:
            window.blit(botswing,(bots[i].rect.topleft))
    else:
        window.blit(botj,(bots[i].rect.topleft)) # jumping image
def myweb(): # runs all code for webshooter look at object also
    global webs,bots,trapped,windowwidth,windowheight,webpressed,webreload
    for i,web in enumerate(webs):
        webs[i].go() # makes it move, look at object
        rotate = py.transform.rotate(webimg, 180 - math.degrees(webs[i].angle)) # rotates image based on angle shooting at
        webrect = rotate.get_rect(center=webs[i].web.center) # re-center the image
        window.blit(rotate, webrect.topleft) #show image
        x=webs[i].web.collidelistall(bots) # if collides with any rect in the bots list
        if len(x)>0 and bots[x[0]] in bots: # if collides and bot exists
            trapped+=1 # you shot one 
            window.blit(webshotimg,webs[i].web.center) # shows a web image for a second to show they were captured
            webs.pop(i) # delete the object
            if x[0] < len(bots):# recheck if bot exists because there were many errors
                bots.pop(x[0]) # delete the bot object
        elif webs[i].web.x>windowwidth or webs[i].web.x<0 or webs[i].web.y>windowheight or webs[i].web.y<0: # if collides with ends
            webs.pop(i) #delete the object
            continue # next web in array
    if webpressed:
        webreload+=1
        if webreload%30 == 0: # so you cannot click forever
            webpressed = False #can click again
            webreload =0 #reset
while True:
    ev = py.event.poll() #checks latest event
    if ev.type == py.QUIT: # if X b utton clicked on top right, close the program
        break
    key = py.key.get_pressed() # gets latest keyboard presses
    mousepos = py.mouse.get_pos() # gats latest mouselocation
    if gamestate == 0: # start screen
        window.blit(cover,(0,-100)) if night else window.blit(cover2,(0,-100)) # switch background based on dark/lightmode
        window.blit(font2.render("SPIDER ESCAPE!",1,white),(100,100))#main game text
        survive = button((windowwidth/2)-(150/2)- 200,windowheight/2-50,150,50,"Survival",font3) # changes game mode
        shooter = button((windowwidth/2)-(150/2),windowheight/2-50,150,50,"Shooter",font3)
        free = button((windowwidth/2)-(150/2) + 200,windowheight/2-50,150,50,"Free Play",font3)
        settings = button((windowwidth/2)-(150/2),windowheight/2+80,150,50,"Settings",font3) # go to settings gamestate 
        htp = button((windowwidth/2)-(200/2),windowheight/2+160,200,50,"How To Play",font3) # go to how to play gamestate
        if survive:
            reset()
            mode = "survival"
            gamestate = 1
        elif shooter:
            mode = "shooter"
            reset()
            gamestate = 1
        elif free:
            mode = "free"
            reset()
            gamestate = 1
        if settings:
            reset()
            gamestate =3
        if htp:
            gamestate = 4
    elif gamestate == 1: # main game 
        #####Events###
        window.blit(backgrounds[1],(-350,0)) if night else window.blit(backgrounds[0],(0,0)) # switch background based on dark/lightmode
        if ev.type == py.MOUSEBUTTONDOWN: # if any mousebutton is clicked
            if py.mouse.get_pressed()[0]: # left click
                pressed = not pressed # turn on/off swinging
                x,y = py.mouse.get_pos() # get the pos of the swinging web
                thwip.play() if playsound else print("nosound") # play sound if setting is on
                if pressed:
                    spider.swing_init(x,y) #start swinging calculation look at object
                else:
                    spider.yspeed = -0.2*spider.yspeed # jump up a little bit 
            elif py.mouse.get_pressed()[2] and not webpressed: # right click
                shoot.play() if playsound else print("nosound") # play sound if setting is on 
                x2,y2 = py.mouse.get_pos() # get the direction that the shot should go towards
                webs.append(Webshooter(spider.rect.x,spider.rect.y,30,10)) # create new webshooter object
                webs[-1].mousestart(x2,y2) # start calculation for mouse 
                webpressed = True 
        ####Stats###     
        window.blit(font1.render("Close Encounters Left:",1,white),(25,50))
        py.draw.rect(window,(255,0,0),(210,50,maxlives*50,20),10)
        py.draw.rect(window,white,(210,50,lives*50,20),10)
        if time % 60 ==0: # increase mytime every 1 second
            mytime +=1 
        time+=1
        # determine what stats to show 
        if mode == "shooter": 
            window.blit(font1.render("Trapped: "+str(trapped),1,white),(25,90))
            gamestate = 2 if mytime > timelimit else gamestate # game ends in the time limit
        elif mode == "free":
            window.blit(font1.render("Trapped: "+str(trapped),1,white),(25,90)) 
            window.blit(font1.render("Time(sec): "+str(mytime),1,white),(25,70)) 
        elif mode == "survival":
            window.blit(font1.render("Time(sec): "+str(mytime),1,white),(25,70))
            
        #####player#####
        spider.run() # stay in the air code, look at object
        if pressed:
            spider.swing() # increment the motion, look at object
            py.draw.line(window,(255,255,255),(spider.rect.x+25,spider.rect.y),(spider.mousex,spider.mousey),5) # draw swinging line
            if abs(math.degrees(spider.angle)-math.degrees(spider.angle_init)) > 150: # stop swinging for too long
                # increment of angle is too high
                spider.yspeed = -0.2*spider.yspeed # jump effect
                pressed = False # stop swinging
        if spider.rect.right>windowwidth: # if hit wall then switch direction of travel
            spider.rect.right = windowwidth
            spider.yspeed = -0.2*spider.yspeed
            spider.xspeed = -spider.xspeed
            pressed = False # stop swinging
        elif spider.rect.x<0: # same thing
            spider.rect.x = 0
            spider.yspeed = -0.2*spider.yspeed
            spider.xspeed = -spider.xspeed
            pressed = False
        touch=spider.rect.collidelistall(bots) # check if the spider is colliding with any of the bots on the screen
        if len(touch)>0: # if collision 
            bots.pop(touch[0]) # delete object
            pressed = False 
            spider.yspeed = 0
            lives-=1 
        if lives<=0 or spider.rect.y> windowheight: # if fall or die
            gamestate = 2 # endgame
        if pressed: # logic for images for spiderman similar to bot
            if not spider.anglestate:
                window.blit(py.transform.flip(miless,True,False),(spider.rect.topleft))
            else:
                window.blit(miless,(spider.rect.topleft))
        else:
            window.blit(milesj,(spider.rect.topleft))
        #####webs####
        if mode == "shooter" or mode == "free": # what modes to run web on
            myweb()
        #####bot#####
        count+=1
        if count % 120 == 0: # every 2 seconds, a new bot is created
            bots.append(Spiderman(random.randint(windowwidth/2-200,windowwidth/2+200)))
            count = 0
            botpresses.append(random.choice([True, False])) # whether or not it is swinging is random 
        for i,bot in enumerate(bots): # for every bot in bots
            if bots[i].rect.y> windowheight: # if fall to the floor then delete it
                bots.remove(bots[i]) 
                break
            else:
                mybot(i) # run the bot code for each instance 
    elif gamestate ==2: # end game
        window.blit(cover,(0,-100)) if night else window.blit(cover2,(0,-100)) # todo add leaderboard (extra feature)
        spider=0 # delete spiderman
        bots.clear() # delete all bots
        
        
        if mode == "shooter":
            highscore = trapped if trapped > highscore else highscore # calculate highscore
            window.blit(font4.render("Times Up!",1,white),(350,100))
            window.blit(font1.render("You Trapped: "+str(trapped),1,white),(400,200))
            window.blit(font1.render("Highscore - Trapped: "+str(highscore),1,white),(400,300))
        elif mode == "free":
            highscore = trapped if trapped > highscore else highscore # calculate highscore
            hightime = mytime if mytime > hightime else hightime # calculate highest time survived
            window.blit(font1.render("You Trapped: "+str(trapped),1,white),(400,200))
            window.blit(font1.render("Highscore - Trapped: "+str(highscore),1,white),(400,300))
            window.blit(font1.render("Time(sec): "+str(mytime),1,white),(400,250))
            window.blit(font1.render("Highscore - Time(sec): "+str(hightime),1,white),(400,330))
            window.blit(font4.render("YOU WERE CAPTURED!",1,white),(250,100)) if mytime < timelimit else window.blit(font4.render("YOU ESCAPED!",1,white),(250,100))
        else:
            hightime = mytime if mytime > hightime else hightime # calculate highest time survived
            window.blit(font4.render("YOU WERE CAPTURED!",1,white),(250,100))
            window.blit(font1.render("Time(sec): "+str(mytime),1,white),(400,250))
            window.blit(font1.render("Highscore - Time(sec): "+str(hightime),1,white),(400,330))
        start = button(windowwidth/2-(100/2),windowheight/2,200,50,"Try Again",font3)
        home = button(windowwidth/2-(100/2),windowheight/2+75,200,50,"Home",font3)
        if start: # try same mode again
            reset()
            gamestate = 1
        elif home: # go back to home screen
            reset()
            gamestate = 0
    elif gamestate == 3:#settings
        window.blit(cover,(0,-100)) if night else window.blit(cover2,(0,-100)) # switch background based on dark/lightmode
        window.blit(font3.render("Settings:",1,white),(50,25))
        window.blit(font1.render("Close Encounters:",1,white),(50,110+50))
        plus = button(370-50,105+50, 40,30,"  +",font1) 
        minus = button(270-50,105+50, 40,30,"   -",font1)
        window.blit(font1.render(str(lives),1,white),(230+50,110+50))
        #increment max lives if plus else decrease as long as withing range
        maxlives = maxlives+1 if plus and maxlives < 9 else maxlives-1 if minus and maxlives>1 else maxlives 
        lives = maxlives
        window.blit(font1.render("Theme:",1,white),(50,200-30+50))
        theme = button(170,200-30+50,100,30,"Dark/Light",font1)
        night = not night if theme else night # switch between dark and light mode
        window.blit(font1.render("Music:",1,white),(50,300-60+50))
        music = button(170,300-60+50,150,30,"Mute/Unmute",font1)
        playmusic = not playmusic if music else playmusic # switch between mute and unmute
        py.mixer.music.pause() if playmusic else py.mixer.music.unpause()
        window.blit(font1.render("Time:",1,white),(50,30+50)) # time limit
        plus2 = button(270,30+50, 40,30,"  +",font1) 
        minus2 = button(170,30+50, 40,30,"   -",font1)
        window.blit(font1.render(str(timelimit),1,white),(230,30+50))
        #increment time if plus else decrease as long as withing range
        timelimit = timelimit+1 if plus2 else timelimit-1 if minus2 and timelimit>1 else timelimit
        window.blit(font1.render("Sound Effects:",1,white),(50,400-90+50))
        sound = button(170,400-90+50,150,30,"Mute/Unmute",font1) 
        playsound = not playsound if sound else playsound # switch between mute and unmute
        
        back = button(50,400, 110,50,"Back",font3)
    elif gamestate ==4:# how to play screen 
        window.fill("black") if night else window.fill("white")
        with open("assets/HowToPlay.txt", "r") as f: #open the text file that the game instructions are written 
            window.blit(font1.render(f.read(),1,white),(15,15)) # read out the entire text file
        back = button(50,400, 110,50,"Back",font3)
    if night: # invert button and text colors for maximum readibility
        white = py.Color(255,255,255)
        black = py.Color(0,0,0)
    else:
        white = py.Color(0,0,0)
        black = py.Color(255,255,255)
    py.display.flip()
    clock.tick(60)

py.quit()