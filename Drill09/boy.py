# 이것은 각 상태들을 객체로 구현한 것임.

from pico2d import load_image, get_time
from sdl2 import SDL_KEYDOWN, SDLK_SPACE, SDLK_RIGHT, SDLK_LEFT, SDL_KEYUP, SDLK_a


def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE


def time_out(e):
    return e[0] == 'TIME_OUT'


def time_out_5(e):
    return e[0] == 'TIME_OUT' and e[1] == 5.0


def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT


def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT


def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT


def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT


def a_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_a


class Autorun:
    @staticmethod
    def enter(boy, e):
        print('Autorun Enter')
        boy.start_time = get_time()
        if boy.action % 2 == 1:
            boy.dir, boy.action = 1, 1
        else:
            boy.dir, boy.action = -1, 0

    @staticmethod
    def exit(boy, e):
        print('Autorun Exit')
        pass

    @staticmethod
    def do(boy):
        print('Autorun do')
        boy.progress_time = get_time() - boy.start_time
        boy.frame = (boy.frame + 1) % 8
        boy.x += boy.dir * (5 + boy.progress_time)
        if boy.x > 800:
            boy.dir, boy.action = -1, 0
        elif boy.x < 0:
            boy.dir, boy.action = 1, 1
        if boy.progress_time > 5:
            boy.state_machine.handle_event(('TIME_OUT', 0))

    @staticmethod
    def draw(boy):
        boy.image.clip_composite_draw(boy.frame * 100, boy.action * 100, 100, 100, 0, '',
                                      boy.x, boy.y, 100 + boy.progress_time * 20,
                                      100 + boy.progress_time * 20)


class Run:
    @staticmethod
    def enter(boy, e):
        if right_down(e) or left_up(e):  # 오른쪽으로 RUN
            boy.dir, boy.action = 1, 1
        elif left_down(e) or right_up(e):  # 왼쪽으로 RUN
            boy.dir, boy.action = -1, 0

    @staticmethod
    def exit(boy, e):
        print('RUN EXIT')

    @staticmethod
    def do(boy):
        print('RUN~~')
        boy.frame = (boy.frame + 1) % 8
        boy.x += boy.dir * 5

    @staticmethod
    def draw(boy):
        boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100, boy.x, boy.y)
        pass


class Sleep:

    @staticmethod
    def enter(boy, e):
        boy.frame = 0
        print('눕기')

    @staticmethod
    def exit(boy, e):
        print('일어서기')

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
        print('드르렁')

    @staticmethod
    def draw(boy):
        if boy.action == 2:
            boy.image.clip_composite_draw(boy.frame * 100, 300, 100, 100,
                                          -3.141592 / 2, 'h', boy.x + 25, boy.y - 25, 100, 100)
        else:
            boy.image.clip_composite_draw(boy.frame * 100, 300, 100, 100,
                                          3.141592 / 2, '', boy.x - 25, boy.y - 25, 100, 100)


class Idle:

    @staticmethod
    def enter(boy, e):
        if boy.action == 0:
            boy.action = 2
        elif boy.action == 1:
            boy.action = 3
        boy.dir = 0
        boy.frame = 0
        boy.start_time = get_time()  # pico2d import 필요
        print('Idle Enter')

    @staticmethod
    def exit(boy, e):
        print('Idle Exit')

    @staticmethod
    def do(boy):
        print('Idle Do')
        boy.frame = (boy.frame + 1) % 8
        if get_time() - boy.start_time > 3:
            boy.state_machine.handle_event(('TIME_OUT', 0))

    @staticmethod
    def draw(boy):
        boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100, boy.x, boy.y)
        pass


class StateMachine:
    def __init__(self, boy):
        self.boy = boy
        self.cur_state = Idle
        self.table = {
            Sleep: {right_down: Run, right_up: Run, left_down: Run, left_up: Run, space_down: Idle, a_down: Autorun},
            Idle: {right_down: Run, right_up: Run, left_down: Run, left_up: Run, time_out: Sleep, a_down: Autorun},
            Run: {right_down: Idle, right_up: Idle, left_down: Idle, left_up: Idle},
            Autorun: {right_down: Run, right_up: Run, left_down: Run, left_up: Run, time_out: Idle}
        }

    def start(self):
        self.cur_state.enter(self.boy, ('START', 0))

    def handle_event(self, e):
        for check_event, next_state in self.table[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.boy, e)
                self.cur_state = next_state
                self.cur_state.enter(self.boy, e)
                return True
        return False
        pass

    def update(self):
        self.cur_state.do(self.boy)

    def draw(self):
        self.cur_state.draw(self.boy)


class Boy:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.action = 3
        self.image = load_image('animation_sheet.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start()

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))
        pass

    def draw(self):
        self.state_machine.draw()
