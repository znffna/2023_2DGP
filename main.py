from pico2d import *

import game_world
from player import Player


def create_world():
    global running
    global player
    running = True

    player = Player()
    game_world.add_object(player)

    pass


def handle_events():
    global running
    global player
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        else:
            player.handle_event(event)
            pass
    pass


def update_world():
    # player.update()
    game_world.update()
    pass


def render_world():
    clear_canvas()

    # player.draw()
    game_world.render()

    update_canvas()
    pass


# 게임 시작

open_canvas()
create_world()

while running:
    handle_events()

    update_world()
    render_world()

    delay(0.05)

close_canvas()
