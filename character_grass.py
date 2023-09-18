from pico2d import *
import math

open_canvas(800,800)

grass = load_image('grass.png')
character = load_image('character.png')

t = 0
course = 0
x = 400
y = 90
while(True):          
    clear_canvas_now()
    grass.draw_now(400,30)
    character.draw_now(x,y)

    if course == 0: # 원        
        x = 300 * math.cos((t-90) / 360 * 2 * math.pi) + 400
        y = 300 * math.sin((t-90) / 360 * 2 * math.pi) + 400
        
    if course == 1: # 사각형
        if (t + 45)//90 == 0 :
            x = x + 8;
        if (t + 45)//90 == 1 :
            y = y + 7;
        if (t + 45)//90 == 2 :
            x = x - 8;
        if (t + 45)//90 == 3 :
            y = y - 7;
        if (t + 45)//90 == 4 :
            x = x + 8;
            
    t = t + 1
    if t == 360:
        course = course + 1
        course = course % 2
    t = t % 360            
    
    delay(0.01)

close_canvas()
