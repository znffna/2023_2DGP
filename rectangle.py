from pico2d import *
import math

open_canvas()

grass = load_image('grass.png')
character = load_image('character.png')

def render_frame(x,y):
    clear_canvas_now()
    grass.draw_now(400,30)
    character.draw_now(x,y)
    delay(0.01)  

def run_circle():
    print('CIRCLE')
    
    # 일단 그림을 그리자

    cx, cy, r = 400, 300, 200
    
    for deg in range(0,360,1):
        x = cx + r * math.cos(math.radians(deg))
        y = cy + r * math.sin(math.radians(deg))
        render_frame(x,y)

def run_rectangle():
    print('RECTANGLE')

    for x in range(50, 750 + 1, 10):
        render_frame(x,90)    
        
#    for x in range(750, 50 - 1, -10):
#        render_frame(x,90)

    
    pass


while True:
    run_circle()
    run_rectangle()   
    break

close_canvas()
