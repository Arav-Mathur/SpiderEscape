#-----------------------------------------------------------------------------
# Program Name: Spiderman Jumper
# Purpose: You are running away from Spiderman 2099 and need to get back home.
# Run and jump as far as possible before getting caught. You have 30 seconds. 
#
# Author:      Arav Mathur
# Created:     20/11/2023
# Updated:     02/12/2023
#-----------------------------------------------------------------------------
#I think this project deserves a level 4+ because ...
#Features Added Above Level 3 Expectations:
# well polished + common theme
# The game has no bugs.
# The game has some elements of randomness and replayability.
# The game uses animated sprites
# File IO to store a high score or other game data
# The game has settings for creating a better user experience including increasing time limit + dark/light mode
# The student has created all code themselves
#-----------------------------------------------------------------------------
#References:
#https://www.pygame.org/docs/
#https://archive.org/details/spider-man-across-the-spider-verse-soundtrack-from-and-inspired-by-the-motion-instrumental-edition/Spider-Man+Across+The+Spider-Verse/Instrumental+Edition/01-Annihilate+(Instrumental).mp3
#Credit: Spiderman Into the spiderverse, Spiderman Across the Spiderverse
import pygame as py
import random # for rooftop generation
from pygame import mixer # sound

#*********SETUP**********
py.init()

#variables to set the size of the window
windowwidth = 500
windowheight = 500
window = py.display.set_mode((windowwidth,windowheight))#create the window
py.display.set_caption("Arav's Spiderman Game") 
clock = py.time.Clock()  #will allow us to set framerate

#Load all sounds + music
jump = py.mixer.Sound("sound/jump2.wav")
jump.set_volume(5.0)
click = py.mixer.Sound("sound/click.wav")
click.set_volume(5.0)

music = py.mixer.music.load("sound/01-Annihilate (Instrumental).mp3")
py.mixer.music.play(-1)

#Load all images
daybg = py.image.load("img/day bg.png") #all images are within image folder
#foreground = py.image.load("img/foreground.png") (unused feature) (may uncomment if you want to check it out)
nightsurface = py.image.load("img/nightbg 3.jpg")
size = 1191 # size of background image
night = True # used for determining dark/light mode
milesm = py.image.load("img/milesrun.png")
milesj = py.image.load("img/milesjump.png")
milesclimb = py.image.load("img/milesclimb.png")
startBack = py.image.load("img/cover.jpg")
endBack = py.image.load("img/cover2.png")


# load possible building sprites + create array containing all of them
buildings = [py.image.load("img/building1.png"),py.image.load("img/building2.png"),py.image.load("img/building3.png"),py.image.load("img/building4.png")]
mybuild = [random.choice(buildings),random.choice(buildings)] # creates an array of 2 random building sprites
#load all fonts
font1 = py.font.SysFont("Bernard MT",60)
font2 = py.font.SysFont("Bernard MT",25)
font4 = py.font.SysFont("Bernard MT",40)
font3 = py.font.Font("spiderfont.ttf",80)

#Load colors
gray = py.Color(15, 42, 60)
white = py.Color(242, 242, 242)
#fsurface = py.transform.scale_by(foreground,1) (unused feature)

#initialize variables that stay constant despite the replaying of the game. (remaining are in reset function)
gamestate = 0
timelimit = 30
highscore = 0
def reset(): #initialize all the variables in a function (make sure it is global otherwise cannot use elsewhere) (maybe next time create an object)
    global nightx,nightx2,size,yspeed,rect,milesloc,milesnum,framecount,air,edge,blockpos,blockpos2,blocks,mytime,distance,time,timeover#,frontx,frontx2
    #frontx = 0 (unused feature)
    #frontx2 = size (unused feature)
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
    blockpos = py.Rect(0,random.randint(300,400),random.randint(250,400),200)#randomly creates building size (x2)
    blockpos.height = windowheight-blockpos.top # make sure bottom touches ground
    blockpos2 = py.Rect(blockpos.right+random.randint(100,300),random.randint(250,400),random.randint(250,500),200)
    blockpos2.height = windowheight-blockpos2.top
    blocks = [blockpos,blockpos2] # places into array
    mytime = 0
    distance = 0
    time = 0
    timeover = False
reset() # run function initially

def button(x,y,w,h,text):# creates a button with text inside using given parameters
    global mousepos 
    button = py.draw.rect(window,gray,(x,y,w,h),0,10) # creates button rectangle using <x,y,w,h>
    window.blit(font1.render(text,1,white),(button.x+5,button.y+5)) # adds <text> to the center
    if pressed and button.collidepoint(mousepos): # collidepoint checks if the mouse pointer is inside the rectangle
            click.play() # play clicking sound
            return True # button = true, this can be used for what happens when button is clicked
        
def animate(img,framewidth,numframes,framerate): # used for running animation 
    global framecount,milesnum 
    if framecount % framerate ==0: # this allows it to run every <framerate> seconds 
        if(milesnum<numframes-1): # if the current frame is inside the sprite sheet,
            milesnum+=1
            img.x += framewidth # move on to the next frame of animation
        else: #else, reset back to the first frame of animation
            milesnum=0 
            img.x =0
    framecount+=1 # count the time
    
#*********GAME LOOP**********
while True:
    #*********INITIAL EVENTS**********
    ev = py.event.poll() #checks latest event
    if ev.type == py.QUIT: # if X b utton clicked on top right, close the program
        break
    key = py.key.get_pressed() # gets latest keyboard presses
    mousepos = py.mouse.get_pos() # gats latest mouselocation
    if ev.type == py.MOUSEBUTTONDOWN: # if mouse is clicked
        pressed = True
    else:
        pressed = False
    window.fill("white")
    if gamestate == 0:#start menu
        if night: # if setting is dark, make background a black image, else make it a white image
            window.blit(startBack,(0,0))
        else:
            window.blit(endBack,(0,0))
        window.blit(font3.render("SPIDER JUMPER",1,white), (25,25)) # title of the game
        start = button((windowwidth-110)/2,170, 110,50,"Start") # stores new button in variable
        settings = button((windowwidth-180)/2,240, 180,50,"Settings")
        howtoplay = button((windowwidth-255)/2,300, 255,50,"How To Play")
        if start == True: # if the button is clicked, gamestate = play
            reset()
            gamestate = 1 # play state
        elif settings == True: 
            gamestate = 4 # go to settings screen
        elif howtoplay == True:
            gamestate = 3 # go to how to play screen
    
    elif gamestate == 1: #play
        #*********EVENTS**********
        if key[py.K_d] == True and edge == False: # if d is clicked on keyboard, run forward. (also if not touching edge of building)
            nightx -=1 # background moves backwards to create a parralax effect
            nightx2 -=1
            #frontx-=3 (unused feature)
            #frontx2-=3
            for i in range(len(blocks)): # move all the buildings backward to create an illusion that the player is moving forward
                blocks[i].left -=10 
            animate(milesloc,50,6,8) # play running animation
            distance +=0.5 # increasing score
         #*********GAME LOGIC**********
        yspeed+=0.2 # gravity variable
        rect.top+=yspeed # increase y location by gravity
         #*********GAME LOGIC: COllISION DETECTION**********
        for i in range(len(blocks)): # for every building, 
            if rect.bottom+1 > blocks[i].top  and rect.left > blocks[i].left and rect.left < blocks[i].right:#if you are touching the top of the building
                yspeed = 0
                air = False
                edge = False
                rect.bottom = blocks[i].top           
                if (key[py.K_SPACE]): # only if you are touching the building can you press space to jump
                    yspeed = -5.5 # simulate an upward thrust
                    jump.play() # play jumping sound
                break
            elif rect.right > blocks[i].left and rect.right < blocks[i].right and rect.bottom > blocks[i].top+20:#touching left edge of the building
                yspeed = 0 # stop the charecter to simulate sticking onto the building
                air = False # you cannot fall down
                edge = True # you cannot move forward at this time
                if key[py.K_w] and key[py.K_SPACE] != True: # if you are not pressing space and are trying to climb
                    yspeed = -4.5 # simulate a climbing animation 
            elif rect.bottom< blocks[i].top: # you are in the air, not touching the building
                air = True
                edge = False
                break
         #*********SCROLLING BACKGROUND/SPRITES**********
        if blocks[0].right < 0: # if the last block goes off screen
            blocks.append(py.Rect(blocks[-1].right+random.randint(50,400),random.randint(250,400),random.randint(250,500),200)) # generate a new block after the furthest block
            blocks[-1].height = windowheight-blocks[-1].top # make sure building touches ground
            mybuild.append(random.choice(buildings)) # also make a new random sprite for the building
            mybuild.pop(0) # remove the last building
            blocks.pop(0) # remove the last building
            
        if nightx < -size: # if background goes off the screen, loop back to the end
            nightx = size
        if nightx2 < -size:# if background goes off the screen, loop back to the end
            nightx2 = size
#         if frontx < -size: (unused feature)
#             frontx = size
#         if frontx2 < -size:
#             frontx2 = size
        if key[py.K_SPACE] == False and key[py.K_d] == False: # if you are idle, have a set frame. 
            milesloc.y = 0
            milesloc.x = 0
            animate(milesloc,50,1,10)
         #*********DEATH**********
        if rect.bottom > windowheight: # if you reach the floor
            gamestate = 2 # end state
        if mytime > timelimit: # if you run out of time/ spiderman 2099 has caught up
            gamestate = 2
            timeover = True
        elif time % 60 ==0: # increase mytime every 1 second
            mytime +=1
        time+=1
        #*********DRAW THE FRAME**********
        if night: # depending on light/dark setting, change background
            window.blit(nightsurface,(nightx,0))
            window.blit(nightsurface,(nightx2,0))
        else:
            window.blit(daybg,(nightx,0))
            window.blit(daybg,(nightx2,0))
#         window.blit(fsurface,(frontx,226)) (unused feature)
#         window.blit(fsurface,(frontx2,226))
        for i in range(len(blocks)): # display all the blocks  
            window.blit(py.transform.smoothscale(mybuild[i],(blocks[i].width,blocks[i].height)),blocks[i]) #scales the image to be the same size as rectangle
            py.draw.rect(window,(15, 42, 60),(blocks[i].left,blocks[i].top+20,10,blocks[i].height)) # display top border to make it easier to identify
            py.draw.rect(window,(0,0,0),(blocks[i].left,blocks[i].top,blocks[i].width,20))# display edge to make it easier to identify
        if air:
            window.blit(milesj,(rect.x,rect.y)) #air sprite
        elif edge:
            window.blit(milesclimb,(rect.x,rect.y)) # climbing sprite
        else:
            window.blit(milesm,(rect.x,rect.y),milesloc) # animated running sprite
        window.blit(font2.render("Time:",1,white),(10,10)) # display current player stats
        window.blit(font2.render("Distance:",1,white),(10,30))
        window.blit(font2.render("Speed:",1,white),(10,50))
        window.blit(font2.render(str(timelimit-mytime)+ " s",1,white),(100,10))# display remaining time
        window.blit(font2.render(str(int(distance))+ " m",1,white),(100,30))# display distance travelled
        speed = distance/(time/60)
        window.blit(font2.render(str(int(speed)) + " m/s",1,white),(100,50))# display speed
        
    elif gamestate == 2:#end screen
        if night: # depending on light/dark setting, change background
            window.blit(startBack,(0,0))
        else:
            window.blit(endBack,(0,0))
        window.blit(font3.render("GAME OVER",1,white), (80,25))
        
        if speed >= highscore:# if the new score beat the previos score, this sets a new high score!
            highscore = speed
            window.blit(font2.render("New High Score!!",1,white),(100,200))
        if timeover: # shows whether you died or was time up
            window.blit(font2.render("Time's Up!",1,white),(100,120))
        else:
            window.blit(font2.render("You Died!",1,white),(100,120))
        window.blit(font2.render("Distance:",1,white),(100,150))# display user stats similar to in game
        window.blit(font2.render("Speed:",1,white),(300,150))
        window.blit(font2.render("High Score:",1,white),(100,170))
        window.blit(font2.render(str(int(distance)) + " m",1,white),(200,150))
        window.blit(font2.render(str(int(speed)) + " m/s",1,white),(400,150))
        window.blit(font2.render(str(int(highscore))+ " m/s",1,white),(200,170))
        
        end = button((windowwidth-125)/2,240, 125,50,"Home") 
        end2 = button((windowwidth-225)/2,300, 225,50,"Play Again")
        if end:
            gamestate = 0 # go back to start screen
        elif end2:
            reset()
            gamestate = 1 # play again
            
    elif gamestate == 3:
        if night: # depending on light/dark setting, change background
            window.fill("black")
        else:
            window.fill("white")
        with open("HowToPlay.txt", "r") as f: #open the text file that the game instructions are written 
            window.blit(font2.render(f.read(),1,white),(15,15)) # read out the entire text file
        
        back = button((windowwidth-110)/2,370, 110,50,"Back")
        if back:
            gamestate = 0 # go back to start menu

    elif gamestate == 4:
        if night: # depending on light/dark setting, change background
            window.fill("black")
        else:
            window.fill("white")
        window.blit(font1.render("Settings",1,white),(50,20))
        window.blit(font4.render("Time Limit:",1,white),(50,100))
        window.blit(font1.render(str(timelimit),1,white),(325,100)) # displays current time limit
        plus = button(400,90, 40,50,"+") 
        minus = button(250,90, 40,50,"-") 
        back = button(100,370, 110,50,"Back")
        
        window.blit(font4.render("Background:",1,white),(50,150))        
        daybutton = button(380,150, 85,50,"Day")
        nightbutton = button(250,150, 120,50,"Night")
        
        if back:# go back to start menu
            gamestate = 0
        elif plus and timelimit <99:#increase the time limit/ how long the game lasts as long as it is not too high
            timelimit+=1 
        elif minus and timelimit >1: # decrease the time limit/ how long the game lasts as long as within range
            timelimit-=1
        elif daybutton: # if button is pressed, make it light mode
            night = False # allows us to make changes to background in other places
            gray = py.Color(242, 242, 242) # inverse dark and light colors for increased readibility
            white = py.Color(15, 42, 60)
        elif nightbutton: # make it dark mode
            night = True # allows us to make changes to background in other places
            gray = py.Color(15, 42, 60) # inverse dark and light colors for increased readibility
            white = py.Color(242, 242, 242)
    py.display.flip()  #shows the frame
    clock.tick(60)#Force frame rate to 60fps or lower
py.quit()