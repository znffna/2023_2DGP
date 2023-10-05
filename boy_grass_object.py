from pico2d import *

# Game object class here

def handle_events():
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False



def reset_world():
    global running

    running = True


def update_world():
    pass


def render_world():
    clear_canvas()
    update_canvas()
    pass


open_canvas()

# initialization code
reset_world()

# game main loop code
while running:
    handle_events()
    update_world()
    render_world()
    delay(0.05)



# finalization code

close_canvas()
