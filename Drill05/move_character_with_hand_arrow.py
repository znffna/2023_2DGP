import random

from pico2d import *

TUK_WIDTH, TUK_HEIGHT = 1280, 1024
open_canvas(TUK_WIDTH, TUK_HEIGHT)

TUK_ground = load_image('TUK_GROUND.png')
character = load_image('animation_sheet.png')
arrow = load_image('hand_arrow.png')


def handle_events():
    global running
    global x, y
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False


def regenerate_pos():
    global start, end
    start = end
    end = [random.randint(0, TUK_WIDTH), random.randint(0, TUK_HEIGHT)]


def move_character(p1, p2):
    global move, x, y
    x1, y1 = p1[0], p1[1]
    x2, y2 = p2[0], p2[1]

    move += 1
    t = move / 300
    x = (1 - t) * x1 + t * x2
    y = (1 - t) * y1 + t * y2
    if move >= 300:
        move = 0
        regenerate_pos()


running = True
x, y = TUK_WIDTH // 2, TUK_HEIGHT // 2
frame = 0
move = 0
start = [x, y]
end = [random.randint(0, TUK_WIDTH), random.randint(0, TUK_HEIGHT)]
hide_cursor()

while running:
    clear_canvas()
    TUK_ground.draw(TUK_WIDTH // 2, TUK_HEIGHT // 2)    #배경 출력
    arrow.draw(end[0], end[1])
    move_character(start, end)
    if start[0] < end[0]:
        character.clip_draw(frame * 100, 100 * 1, 100, 100, x, y)  # 캐릭터 출력
    else:
        character.clip_composite_draw(frame * 100, 100 * 1, 100, 100, 0, 'h', x, y, 100, 100)
    update_canvas()
    frame = (frame + 1) % 8 #애니메이션 구현

    handle_events()

close_canvas()




