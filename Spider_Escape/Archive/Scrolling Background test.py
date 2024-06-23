import pygame as py
#setup
py.init()
windowwidth = 500
windowheight = 500
window = py.display.set_mode((windowwidth,windowheight))
clock = py.time.Clock()

bg = py.image.load("images/css-parallax-city-skyline.png")
width = 3154
scalef = 4
x = 0
y = 0
x2 = width/scalef
scale = py.transform.scale_by(bg,1/scalef)

#loop
while True:
    ev = py.event.poll()
    if ev.type == py.QUIT:
        break
    key = py.key.get_pressed()
#     if key[py.K_d]:
#         print("right")
#         x -=10
#     if key[py.K_a]:
#         print("left")
#         x +=10
    if key[py.K_s]:
        print("down")
        y -=10
    if key[py.K_w]:
        print("up")
        y +=10
        
    window.fill("white")
    if x > -width/scalef:
        x-=3
        window.blit(scale, (x,y))
    else:
        x = width/scalef
    if x2> -width/scalef:
        x2-=3
        window.blit(scale,(x2,y))
    else:
        x2 = width/scalef
    
    py.display.flip()
    clock.tick(60)    
py.quit()