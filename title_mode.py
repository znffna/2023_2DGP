from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE

import game_framework
from pico2d import load_image, delay, clear_canvas, update_canvas, get_events, get_time, load_music

import play_mode


def init():
    global image
    global music
    image = load_image('resource/title.png')
    music = load_music('resource/title.mp3')
    music.set_volume(32)
    music.repeat_play()

def finish():
    global image
    global music
    del image
    del music

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            game_framework.change_mode(play_mode)


def update():
    pass


def draw():
    clear_canvas()
    image.clip_draw(0, 0, 800, 600, 400, 300)
    update_canvas()
