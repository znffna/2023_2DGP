from math import radians, cos, sin

from pico2d import *

import game_framework
import play_mode


def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE


def time_out(e):
    return e[0] == 'TIME_OUT'


def bt_swing(e):
    return e[0] == 'bt_swing'


# 상태에 대한 클래스
SWING_TIME = 0.4  # 1번 스윙에 걸리는 시간
SWING_PER_SECOND = 1 / SWING_TIME  # 초당 스윙 횟수


class Idle:  # 가만히 있음
    @staticmethod
    def enter(racket, e):
        pass

    @staticmethod
    def exit(racket, e):
        pass

    @staticmethod
    def do(racket):
        pass

    @staticmethod
    def draw(racket):
        Racket.image.clip_composite_draw(0, 0, 512, 512, radians(racket.default_rad), ''
                                         , racket.x + 35 * cos(radians(racket.default_rad + 45.0))
                                         , racket.y + racket.height + 35 * sin(radians(racket.default_rad + 45.0)),
                                         70, 70);


class Swing:  # 라켓을 휘두름.
    @staticmethod
    def enter(racket, e):
        racket.wait_time = get_time()  # pico2d import 필요
        if racket.default_rad == 90.0:
            racket.swing_dir = -1 if play_mode.shuttle.y + play_mode.shuttle.z > racket.y else 1
        else:
            racket.swing_dir = -1 if play_mode.shuttle.y + play_mode.shuttle.z < racket.y else 1
        Racket.swing_sound.play()
        pass

    @staticmethod
    def exit(racket, e):
        racket.racket_rad = 0
        # play_mode.shuttle.last_touch = None
        pass

    @staticmethod
    def do(racket):
        racket.racket_rad += racket.swing_dir * 360.0 * SWING_PER_SECOND * game_framework.frame_time  # 0.75초에 1바퀴 회전이 되도록.
        if get_time() - racket.wait_time > SWING_TIME:
            racket.state_machine.handle_event(('TIME_OUT', 0))
        pass

    @staticmethod
    def draw(racket):
        Racket.image.clip_composite_draw(0, 0, 512, 512, radians(racket.racket_rad + racket.default_rad), ''
                                         , racket.x + 35 * cos(radians(racket.racket_rad + racket.default_rad + 45.0))
                                         , racket.y + racket.height + 35 * sin(
                radians(racket.racket_rad + racket.default_rad + 45.0) )
                                         , 70, 70);
        pass


class StateMachine:
    def __init__(self, racket):
        self.racket = racket
        self.cur_state = Idle
        self.transitions = {
            Idle: {space_down: Swing, bt_swing: Swing},
            Swing: {time_out: Idle}
        }

    def start(self):
        self.cur_state.enter(self.racket, ('NONE', 0))

    def update(self):
        self.cur_state.do(self.racket)

    def handle_event(self, e):
        for check_event, next_state in self.transitions[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.racket, e)
                self.cur_state = next_state
                self.cur_state.enter(self.racket, e)
                return True

        return False

    def draw(self):
        self.cur_state.draw(self.racket)


class Racket:
    image = None
    swing_sound = None

    def __init__(self, rad=0.0):
        self.x, self.y = 0, 0
        self.height = 0.0
        self.default_rad = rad
        self.racket_rad = 0.0
        self.racket_swing = False
        self.state_machine = StateMachine(self)

        if Racket.image == None:
            Racket.image = load_image('resource/badmintonRacket.png')
            Racket.swing_sound = load_wav('resource/swing.wav')
            Racket.swing_sound.set_volume(32)

    def update(self):
        self.state_machine.update()
        pass

    def handle_event(self, e):
        self.state_machine.handle_event(('INPUT', e))

    def draw(self):
        self.state_machine.draw()
        draw_rectangle(*self.get_bb())
        pass

    def get_bb_center_len():
        return 35

    def get_bb(self):
        now_x = self.x + 1.5 * 35 * cos(radians(self.racket_rad + self.default_rad + 45.0))
        now_y = self.y + self.height + 1.5 * 35 * sin(radians(self.racket_rad + self.default_rad + 45.0))

        return now_x - 20, now_y - 20, now_x + 20, now_y + 20

    def handle_collision(self, group, other):
        if group == 'racket:shuttle':
            pass
        pass
