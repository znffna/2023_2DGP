from pico2d import *


def create_world():
    global running
    running = True
    pass


def handle_events():
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
