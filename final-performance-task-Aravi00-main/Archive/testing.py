import pygame as py
import numpy as np

# Setup
py.init()
windowwidth = 1000
windowheight = 600
window = py.display.set_mode((windowwidth, windowheight))
clock = py.time.Clock()

# Loop
rext = 50
reyt = 50
yspeed = 0
pressed = False
angle = 0
angular_speed = 0


while True:
    ev = py.event.poll()
    if ev.type == py.QUIT:
        break
    key = py.key.get_pressed()
    window.fill((255, 255, 255))
    if ev.type == py.MOUSEBUTTONDOWN:
        pressed = not pressed

        x, y = py.mouse.get_pos()
        if pressed:
            angle, length = np.arctan2(y - reyt, x - rext - 30), np.sqrt((x - rext - 30) ** 2 + (y - reyt) ** 2)
            angular_speed = 0
        else:
            angular_speed = -0.1

    # Apply physics simulation
    angular_speed += 0.0005
    angle += angular_speed
    rext = (x - length * np.cos(angle)) if pressed else rext
    reyt = (y + length * np.sin(angle)) if pressed else reyt

    # Draw swinging line
    if pressed:
        py.draw.line(window, (0, 0, 0), (rext + 30, reyt), (x, y), 2)

    # Draw Spiderman
    rect = [rext, reyt, 30, 40]  # x, y, w, h
    py.draw.rect(window, (0, 0, 0), rect)

    # Update the display
    py.display.flip()
    clock.tick(60)

py.quit()
