from pico2d import *
import random

TUK_WIDTH, TUK_HEIGHT = 1280, 1024


def load_resources():
    global TUK_ground, character
    global arrow

    arrow = load_image('hand_arrow.png')
    TUK_ground = load_image('TUK_GROUND.png')
    character = load_image('animation_sheet.png')


def handle_events():
    global running
    global mx, my
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_MOUSEMOTION:
            mx, my = event.x, TUK_HEIGHT - 1 - event.y
        elif event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_LEFT:  # 마우스 클릭이 있으면...
            points.append((event.x, TUK_HEIGHT - 1 - event.y))  # 클릭된 위치를 새로운 점으로 추가.
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
    pass


def reset_world():
    global running, cx, cy, frame
    global t
    global action
    global mx, my
    global points

    mx, my = 0, 0
    running = True
    cx, cy = TUK_WIDTH // 2, TUK_HEIGHT // 2
    frame = 0
    action = 3

    points = [ ]
    set_new_target_arrow()


def set_new_target_arrow():
    global sx, sy, hx, hy, t
    global action
    global frame
    global target_exists

    if points:  # points 리스트안에 남아있는 점이 있으면,
        sx, sy = cx, cy  # p1 : 시작점
        # hx, hy = 50, 50
        hx, hy = points[0]  # p2 : 끝점.
        t = 0.0
        action = 1 if sx < hx else 0
        frame = 0
        target_exists = True
    else:
        action = 3 if action == 1 else 2    # 이전에 소년이 우측으로 이동중이었으면, IDLE 동작시 우측을 바라보도록
        frame = 0
        target_exists = False


def render_world():
    clear_canvas()
    TUK_ground.draw(TUK_WIDTH // 2, TUK_HEIGHT // 2)
    for p in points:
        arrow.draw(p[0], p[1])
    arrow.draw(mx, my)
    character.clip_draw(frame * 100, 100 * action, 100, 100, cx, cy)
    update_canvas()


def update_world():
    global frame
    global cx, cy
    global t

    frame = (frame + 1) % 8

    if target_exists:
        if t <= 1.0:
            cx = (1 - t) * sx + t * hx  # cx 는 시작 x 와 끝 x 를 1-t:t 의 비율로 섞은 위치
            cy = (1 - t) * sy + t * hy
            t += 0.001
        else:   # 목표지점에 도달하면
            cx, cy = hx, hy  # 캐릭터 위치를 기존 목적지 위치와  강제로 정확이 일치시킴.
            del points[0]   # 목표지점에왔기 때문에, 더 이상 필요없는 점을 삭제
            set_new_target_arrow()


open_canvas(TUK_WIDTH, TUK_HEIGHT)
hide_cursor()
load_resources()
reset_world()

while running:
    render_world()  # 월드의 현재 내용을 그린다.
    handle_events()  # 사용자 입력을 받아들인다.
    update_world()  # 월드 안의 객체들의 상호작용을 계산하고 그 결과를 update 한다.

close_canvas()
