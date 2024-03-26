import random

from pico2d import *

TUK_WIDTH, TUK_HEIGHT = 1280, 1024
open_canvas(TUK_WIDTH, TUK_HEIGHT)

TUK_ground = load_image('TUK_GROUND.png')
character = load_image('animation_sheet.png')
arrow = load_image('hand_arrow.png')


def handle_events():
    global running
    global x, y, end , mx, my
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_LEFT:
            end.append([event.x, TUK_HEIGHT - 1 - event.y])
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        elif event.type == SDL_MOUSEMOTION:
            mx, my = event.x, TUK_HEIGHT - 1 - event.y


def regenerate_pos():
    global start, end, head
    start = end[0]
    end.pop(0)


def move_character(p1, p2):
    global move, x, y, head
    x1, y1 = p1[0], p1[1]
    x2, y2 = p2[0], p2[1]

    move += 1
    t = move / 300
    x = (1 - t) * x1 + t * x2
    y = (1 - t) * y1 + t * y2

    if len(end) > 0:
        if start[0] < end[0][0]:
            head = 0
        else:
            head = 1
    if move >= 300:
        move = 0
        if len(end) > 0:
            regenerate_pos()



def moving():
    for a in end:
        arrow.draw(a[0], a[1])
    move_character(start, end[0])


running = True
x, y = TUK_WIDTH // 2, TUK_HEIGHT // 2
frame = 0
move = 300
start = [x, y]
end = [[x, y]]
mx, my = TUK_WIDTH // 2, TUK_HEIGHT // 2
head = 0
hide_cursor()

while running:
    clear_canvas()
    TUK_ground.draw(TUK_WIDTH // 2, TUK_HEIGHT // 2)    # 배경 출력
    # 마우스 커서 출력
    arrow.draw(mx, my)
    # 커서가 있을경우 움직임.
    if len(end) > 0:
        moving()
    if head == 0:
        character.clip_draw(frame * 100, 100 * 1, 100, 100, x, y)  # 캐릭터 출력
    else:
        character.clip_composite_draw(frame * 100, 100 * 1, 100, 100, 0, 'h', x, y, 100, 100)
    update_canvas()
    frame = (frame + 1) % 8     # 애니메이션 구현

    handle_events()

close_canvas()




