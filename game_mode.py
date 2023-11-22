from pico2d import get_events, clear_canvas, update_canvas
from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE, SDLK_s

import game_framework
import game_world
from player import Player
from racket import Racket
from shuttle import Shuttle
from stadium import Stadium


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
            shuttle.x = 300
            shuttle.y = 30
            shuttle.z = 300
        else:
            player.handle_event(event)
            pass
    pass


def init():
    global running
    global player
    global rackets
    global shuttle
    running = True

    stadium = Stadium()
    game_world.add_object(stadium)
    game_world.add_collision_pair('player:net', None, stadium)
    game_world.add_collision_pair('shuttle:net', None, stadium)

    rackets = [Racket(90 * (1-i)) for i in range(2)]
    for racket in rackets:
        game_world.add_object(racket, 1)
        game_world.add_collision_pair('racket:shuttle', racket, None)

    player = Player(rackets[0], '오른쪽')
    game_world.add_object(player, 1)
    game_world.add_collision_pair('player:net', player, None)

    ai_player = Player(rackets[1], '왼쪽')
    game_world.add_object(ai_player, 1)
    game_world.add_collision_pair('player:net', ai_player, None)

    shuttle = Shuttle()
    game_world.add_object(shuttle, 2)
    game_world.add_collision_pair('racket:shuttle', None, shuttle)
    game_world.add_collision_pair('shuttle:net', shuttle, None)

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
    update_canvas()


def pause():
    pass


def resume():
    pass
