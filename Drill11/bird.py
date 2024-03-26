# 이것은 각 상태들을 객체로 구현한 것임.
import random

from pico2d import get_time, load_image, load_font, clamp,  SDL_KEYDOWN, SDL_KEYUP, SDLK_SPACE, SDLK_LEFT, SDLK_RIGHT
from ball import Ball, BigBall
import game_world
import game_framework

# state event check
# ( state event type, event value )

def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT


def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT


def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT


def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT

def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE

def time_out(e):
    return e[0] == 'TIME_OUT'

# time_out = lambda e : e[0] == 'TIME_OUT'




# Boy Run Speed
# fill here
PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 40.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# Boy Action Speed
# fill here
TIME_PER_ACTION = 0.7   # 한번의 애니메이션에 걸리는 시간
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION  # 1초에 반복되는 애니메이션 횟수
FRAMES_PER_ACTION = 14  # 한번의 애니메이션에 사용되는 프레임수









class Idle:

    @staticmethod
    def enter(boy, e):
        if boy.face_dir == -1:
            boy.action = 2
        elif boy.face_dir == 1:
            boy.action = 3
        boy.dir = 0
        boy.frame = 0
        boy.wait_time = get_time() # pico2d import 필요
        pass

    @staticmethod
    def exit(boy, e):
        if space_down(e):
            boy.fire_ball()
        pass

    @staticmethod
    def do(boy):
        # boy.frame = (boy.frame + 1) % 8
        boy.frame = (boy.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 8
        if get_time() - boy.wait_time > 2:
            boy.state_machine.handle_event(('TIME_OUT', 0))

    @staticmethod
    def draw(boy):
        boy.image.clip_draw(int(boy.frame) * 100, boy.action * 100, 100, 100, boy.x, boy.y)



class Run:

    @staticmethod
    def enter(bird, e):
        if right_down(e) or left_up(e): # 오른쪽으로 RUN
            bird.dir, bird.action, bird.face_dir = 1, 1, 1
        elif left_down(e) or right_up(e): # 왼쪽으로 RUN
            bird.dir, bird.action, bird.face_dir = -1, 0, -1

    @staticmethod
    def exit(bird, e):
        if space_down(e):
            bird.fire_ball()

        pass

    @staticmethod
    def do(bird):
        bird.frame = (bird.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        bird.x += bird.dir * RUN_SPEED_PPS * game_framework.frame_time
        # print(f'Bird.dir:{bird.dir},Bird.RUN_SPEED_PPS:{RUN_SPEED_PPS},  Bird.x:{bird.x}')
        if bird.x < 90:
            bird.dir, bird.action, bird.face_dir = 1, 1, 1
        elif bird.x > 1600 - 90:
            bird.dir, bird.action, bird.face_dir = -1, 0, -1

        # bird.x = clamp(25, bird.x, 1600 - 25)


    @staticmethod
    def draw(bird):
        if bird.face_dir == -1:
            bird.image.clip_composite_draw(int(bird.frame) % 5 * 184, (2 - (int(bird.frame) // 5)) * 169, 180, 169,
                                           0, 'h', bird.x + 30, bird.y - 30, 60, 60)
        else:
            bird.image.clip_composite_draw(int(bird.frame) % 5 * 184, (2 - (int(bird.frame) // 5)) * 169, 180, 169,
                                           0, '', bird.x - 30, bird.y - 30, 60, 60)
        # bird.image.clip_draw(int(bird.frame) % 5 * 180, (2 - int(bird.frame) // 5) * 167, 179, 166, bird.x, bird.y)




class StateMachine:
    def __init__(self, bird):
        self.bird = bird
        self.cur_state = Run
        self.transitions = {
            Idle: {right_down: Run, left_down: Run, left_up: Run, right_up: Run, space_down: Idle},
            Run: {right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle, space_down: Run}
        }

    def start(self):
        self.cur_state.enter(self.bird, ('NONE', 0))

    def update(self):
        self.cur_state.do(self.bird)

    def handle_event(self, e):
        pass

    def draw(self):
        self.cur_state.draw(self.bird)





class Bird:
    def __init__(self):
        self.x, self.y = random.randint(50, 450 - 50), 290
        self.frame = 0
        self.action = 3
        self.face_dir = 1
        self.dir = 1
        self.image = load_image('bird_animation.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start()
        self.item = 'Ball'
        # self.font = load_font('ENCR10B.TTF', 16)

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
        # self.font.draw(self.x - 60, self.y + 50, f'(Time :{get_time():.2f})', (255, 255, 0))
