from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE, SDLK_SPACE

import game_framework
from pico2d import load_image, delay, clear_canvas, update_canvas, get_events, get_time, load_music

import game_world
import play_mode
from game_world import objects


def init():
    global image
    image = load_image('resource/introduce.png')


def finish():
    global image
    del image

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            game_framework.pop_mode()


def update():
    pass


def draw():
    clear_canvas()
    game_world.render()
    image.draw(400, 300)
    update_canvas()
