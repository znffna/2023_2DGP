from pico2d import *


def create_world():
    global running
    running = True
    pass


def handle_events():
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
    pass


def update_world():
    pass


def render_world():
    pass


open_canvas()
create_world()

while running:
    handle_events()
    update_world()
    render_world()
    delay(0.01)

close_canvas()
