from math import radians, cos, sin

from pico2d import *

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


def up_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_UP


def up_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_UP


def down_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_DOWN


def down_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_DOWN


def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE


def a_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_a


def time_out(e):
    return e[0] == 'TIME_OUT'


# Player Run Speed
# 배드민턴 길이 = 13.4m, 출력할 캔버스 크기 : 800 * 600
# PIXEL_PER_METER = (8000 / 1340)  # 800 pixel 1340 cm
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# Player Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8

# Player Jump Speed
JUMP_SPEED_MPS = 30.0
JUMP_SPEED_PPS = (JUMP_SPEED_MPS * PIXEL_PER_METER)
TIME_PER_JUMP = 0.7
JUMP_PER_TIME = 1.0 / TIME_PER_JUMP



# 상태에 대한 클래스

class Idle:  # 가만히 있음
    @staticmethod
    def enter(player, e):
        if player.face_dir == '왼쪽':
            player.move_dir = 2
        elif player.face_dir == '오른쪽':
            player.move_dir = 1
        elif player.face_dir == '위쪽':
            player.move_dir = 0
        elif player.face_dir == '아래쪽':
            player.move_dir = 3
        # player.move_dir -= 4

        player.LR_dir = 0
        player.TB_dir = 0
        player.frame = 6
        # player.wait_time = get_time()  # pico2d import 필요
        pass

    @staticmethod
    def exit(player, e):
        pass

    @staticmethod
    def do(player):
        player.frame = (player.frame - 6 + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 6 + 6
        pass

    @staticmethod
    def draw(player):
        player.image.clip_draw(int(player.frame) * 70, player.move_dir * 80, 50, 80, player.x, player.y);
        pass


class MoveHorizon:  # 좌우 이동 중
    @staticmethod
    def enter(player, e):
        player.frame = 0
        if right_down(e) or left_up(e):  # 오른쪽으로 RUN
            player.LR_dir, player.move_dir, player.face_dir = 1, 5, '오른쪽'
        elif left_down(e) or right_up(e):  # 왼쪽으로 RUN
            player.LR_dir, player.move_dir, player.face_dir = -1, 6, '왼쪽'
        elif up_down(e) or down_up(e) or down_down(e) or up_up(e):
            if player.LR_dir == 1:
                player.move_dir, player.face_dir = 5, '오른쪽'
            else:
                player.move_dir, player.face_dir = 6, '왼쪽'

        pass

    @staticmethod
    def exit(player, e):
        pass

    @staticmethod
    def do(player):
        # 이동하는 코드 작성
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3
        player.x += player.LR_dir * RUN_SPEED_PPS * game_framework.frame_time
        player.x = clamp(player.y - 30, player.x, 800 + 30 - player.y)
        # player.x = clamp(35, player.x, 800 - 35)

        pass

    @staticmethod
    def draw(player):
        player.image.clip_draw(int(player.frame) * 70, player.move_dir * 80, 50, 80, player.x, player.y);
        pass


class MoveVertical:  # 상하 이동 중
    @staticmethod
    def enter(player, e):
        player.frame = 0
        if up_down(e) or down_up(e):  # 위쪽으로 RUN
            player.TB_dir, player.move_dir, player.face_dir = 1, 4, '위쪽'
        elif down_down(e) or up_up(e):  # 아래로 RUN
            player.TB_dir, player.move_dir, player.face_dir = -1, 7, '아래쪽'
        elif right_down(e) or left_up(e) or left_down(e) or right_up(e):
            if player.TB_dir == 1:
                player.move_dir, player.face_dir = 4, '위쪽'
            else:
                player.move_dir, player.face_dir = 7, '아래쪽'

    @staticmethod
    def exit(player, e):
        pass

    @staticmethod
    def do(player):
        # 이동하는 코드 작성
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3
        player.y += player.TB_dir * RUN_SPEED_PPS * game_framework.frame_time
        player.y = clamp(35, player.y, 145 - 35)
        player.x = clamp(player.y - 30, player.x, 800 + 30 - player.y)
        pass

    @staticmethod
    def draw(player):
        player.image.clip_draw(int(player.frame) * 70, player.move_dir * 80, 50, 78, player.x, player.y);
        pass


class MoveDiagonal:  # 대각선 이동 중
    @staticmethod
    def enter(player, e):
        player.frame = 0
        if right_down(e) or left_up(e):  # 오른쪽으로 RUN
            player.LR_dir, player.move_dir, player.face_dir = 1, 5, '오른쪽'
        elif left_down(e) or right_up(e):  # 왼쪽으로 RUN
            player.LR_dir, player.move_dir, player.face_dir = -1, 6, '왼쪽'
        elif up_down(e) or down_up(e):  # 위쪽으로 RUN
            player.TB_dir, player.move_dir, player.face_dir = 1, 4, '위쪽'
        elif down_down(e) or up_up(e):  # 아래로 RUN
            player.TB_dir, player.move_dir, player.face_dir = -1, 7, '아래쪽'
        pass

    @staticmethod
    def exit(player, e):
        pass

    @staticmethod
    def do(player):
        # 이동하는 코드 작성
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3
        player.x += player.LR_dir * RUN_SPEED_PPS * game_framework.frame_time
        player.x = clamp(player.y - 30, player.x, 800 + 30 - player.y)
        # player.x = clamp(35, player.x, 800 - 35)
        player.y += player.TB_dir * RUN_SPEED_PPS * game_framework.frame_time
        player.y = clamp(35, player.y, 145 - 35)

        # if player.height > 0:
        #     player.height += player.velocity * game_framework.frame_time
        #     player.velocity += player.accelate * game_framework.frame_time
        #     player.accelate -= 0.0098 * game_framework.frame_time
        # else:
        #     player.accelate = 0
        #     player.velocity = 0
        #     player.height = 0
        pass

    @staticmethod
    def draw(player):
        player.image.clip_draw(int(player.frame) * 70, player.move_dir * 80, 50, 80, player.x, player.y);
        pass


class Jump:
    @staticmethod
    def enter(player, e):
        player.jump_time = get_time()  # pico2d import 필요
        player.current_time = player.jump_time
        pass

    @staticmethod
    def exit(player, e):
        player.height = 0
        pass

    @staticmethod
    def do(player):
        current_time = get_time() - player.jump_time

        if current_time > TIME_PER_JUMP:
            player.state_machine.handle_event(('TIME_OUT', 0))
        if player.current_time < TIME_PER_JUMP / 2.0:
            player.height += JUMP_SPEED_PPS * game_framework.frame_time

        player.current_time = current_time
        pass

    @staticmethod
    def draw(player):
        player.image.clip_draw(int(player.frame) * 70, player.move_dir * 80, 50, 80, player.x, player.y);
        pass


class StateMachine:
    def __init__(self, player):
        self.player = player
        self.cur_state = Idle
        self.transitions = {
            Idle: {right_down: MoveHorizon, left_down: MoveHorizon, right_up: MoveHorizon, left_up: MoveHorizon,
                   up_down: MoveVertical, down_up: MoveVertical, down_down: MoveVertical, up_up: MoveVertical
                , a_down: Jump},
            MoveHorizon: {right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle
                , up_down: MoveDiagonal, down_up: MoveDiagonal, down_down: MoveDiagonal, up_up: MoveDiagonal,
                          a_down: Jump},
            MoveVertical: {right_down: MoveDiagonal, left_down: MoveDiagonal, right_up: MoveDiagonal,
                           left_up: MoveDiagonal
                , up_down: Idle, down_up: Idle, down_down: Idle, up_up: Idle, a_down: Jump},
            MoveDiagonal: {right_down: MoveVertical, left_down: MoveVertical, right_up: MoveVertical,
                           left_up: MoveVertical
                , up_down: MoveHorizon, down_up: MoveHorizon, down_down: MoveHorizon, up_up: MoveHorizon, a_down: Jump},
            Jump: {time_out : Idle}
        }

    def start(self):
        self.cur_state.enter(self.player, ('NONE', 0))

    def update(self):
        self.cur_state.do(self.player)

    def handle_event(self, e):
        for check_event, next_state in self.transitions[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.player, e)
                self.cur_state = next_state
                self.cur_state.enter(self.player, e)
                return True

        return False

    def draw(self):
        self.cur_state.draw(self.player)


class Player:
    image = None

    def __init__(self, racket):
        self.racket = racket
        self.x, self.y = 300, 60
        self.height = 0
        self.frame = 0
        self.state_machine = StateMachine(self)
        self.LR_dir = 0  # 좌우 이동하는 방향 (로직)
        self.TB_dir = 0  # 상하 이동하는 방향 (로직)
        self.face_dir = '오른쪽'  # 바라보는 방향 (방향 파악)
        self.move_dir = 0  # 바라보는 방향 (이미지 위치)

        if Player.image == None:
            Player.image = load_image('resource/character.png')  # 70 x 80 크기 스프라이트

    def update(self):
        self.state_machine.update()
        self.racket.x = self.x
        self.racket.y = self.y

    def handle_event(self, e):
        self.state_machine.handle_event(('INPUT', e))
        self.racket.state_machine.handle_event(('INPUT', e))

    def draw(self):
        self.state_machine.draw()
        draw_rectangle(*self.get_bb())
        pass

    def get_bb(self):
        return self.x - 35, self.y - 40, self.x + 35, self.y + 40

    def handle_collision(self, group, other):
        if group == 'player:net':
            if self.x < other.x:
                self.x = clamp(0, self.x, other.x - 20)
            else:
                self.x = clamp(other.x + 10, self.x, 800)
            pass
