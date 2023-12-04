from pico2d import get_events, clear_canvas, update_canvas, load_font
from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE, SDLK_s

import game_framework
import game_world
from player import Player
from racket import Racket
from shuttle import Shuttle
from background import BackGround


def handle_events():
    global running
    global player
    global shuttle

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_s:
            shuttle.x = 200
            shuttle.y = 30
            shuttle.z = 300
            shuttle.last_touch = None
        else:
            player.handle_event(event)
            pass
    pass


def init():
    global running
    global player
    global rackets
    global shuttle
    global ai_player
    global font
    running = True

    stadium = BackGround()
    game_world.add_object(stadium)
    game_world.add_collision_pair('player:net', None, stadium)
    game_world.add_collision_pair('shuttle:net', None, stadium)

    shuttle = Shuttle()
    game_world.add_object(shuttle, 2)
    game_world.add_collision_pair('racket:shuttle', None, shuttle)
    game_world.add_collision_pair('shuttle:net', shuttle, None)

    player = Player('오른쪽')
    game_world.add_object(player, 1)
    game_world.add_collision_pair('player:net', player, None)

    ai_player = Player('왼쪽')
    game_world.add_object(ai_player, 1)
    game_world.add_collision_pair('player:net', ai_player, None)

    font = load_font('resource/SevenSegment.ttf', 40)

    pass


def finish():
    game_world.clear()
    pass


def update():
    game_world.update()
    game_world.handle_collisions()
    # fill here


def draw():
    clear_canvas()
    game_world.render()
    font.draw(350, 550, f'{player.point}  -  {ai_player.point}', (255, 0, 0))
    update_canvas()


def pause():
    pass


def resume():
    pass
