from math import radians, cos, sin

from pico2d import *

import game_framework
import play_mode
import game_world
from behavior_tree import BehaviorTree, Sequence, Condition, Action, Selector
from racket import Racket, Swing


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
JUMP_SPEED_MPS = 10.0
JUMP_SPEED_PPS = (JUMP_SPEED_MPS * PIXEL_PER_METER)
TIME_PER_JUMP = 0.7
JUMP_PER_TIME = 1.0 / TIME_PER_JUMP


# 상태에 대한 클래스

class Idle:  # 가만히 있음
    @staticmethod
    def enter(player, e):
        player.LR_dir = 0
        player.TB_dir = 0
        player.frame = 6
        player.move_dir = 1  # 바라보는 방향 (이미지 위치)
        # player.wait_time = get_time()  # pico2d import 필요
        pass

    @staticmethod
    def exit(player, e):
        player.move_dir = 5  # 바라보는 방향 (이미지 위치)
        pass

    @staticmethod
    def do(player):
        player.frame = (player.frame - 6 + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 6 + 6
        pass

    @staticmethod
    def draw(player):
        player.image.clip_draw(int(player.frame) * 70, player.move_dir * 80, 50, 80, player.x, player.z);
        pass


class MoveHorizon:  # 좌우 이동 중
    @staticmethod
    def enter(player, e):
        player.frame = 0
        if right_down(e) or left_up(e):  # 오른쪽으로 RUN
            player.LR_dir, player.face_dir = 1, '오른쪽'
        elif left_down(e) or right_up(e):  # 왼쪽으로 RUN
            player.LR_dir, player.face_dir = -1, '왼쪽'

    @staticmethod
    def exit(player, e):
        pass

    @staticmethod
    def do(player):
        # 이동하는 코드 작성
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3
        player.x += player.LR_dir * RUN_SPEED_PPS * game_framework.frame_time
        player.x = clamp(player.z - 30, player.x, 800 + 30 - player.z)
        # player.x = clamp(35, player.x, 800 - 35)

        pass

    @staticmethod
    def draw(player):
        player.image.clip_draw(int(player.frame) * 70, player.move_dir * 80, 50, 80, player.x, player.z);
        pass


class MoveVertical:  # 상하 이동 중
    @staticmethod
    def enter(player, e):
        player.frame = 0
        if up_down(e) or down_up(e):  # 위쪽으로 RUN
            player.TB_dir, player.face_dir = 1, '위쪽'
        elif down_down(e) or up_up(e):  # 아래로 RUN
            player.TB_dir, player.face_dir = -1, '아래쪽'

    @staticmethod
    def exit(player, e):
        pass

    @staticmethod
    def do(player):
        # 이동하는 코드 작성
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3
        player.z += player.TB_dir * RUN_SPEED_PPS * game_framework.frame_time
        player.z = clamp(35, player.z, 145 - 35)
        player.x = clamp(player.z - 30, player.x, 800 + 30 - player.z)
        pass

    @staticmethod
    def draw(player):
        player.image.clip_draw(int(player.frame) * 70, player.move_dir * 80, 50, 78, player.x, player.z);
        pass


class MoveDiagonal:  # 대각선 이동 중
    @staticmethod
    def enter(player, e):
        player.frame = 0
        if right_down(e) or left_up(e):  # 오른쪽으로 RUN
            player.LR_dir, player.face_dir = 1, '오른쪽'
        elif left_down(e) or right_up(e):  # 왼쪽으로 RUN
            player.LR_dir, player.face_dir = -1, '왼쪽'
        elif up_down(e) or down_up(e):  # 위쪽으로 RUN
            player.TB_dir, player.face_dir = 1, '위쪽'
        elif down_down(e) or up_up(e):  # 아래로 RUN
            player.TB_dir, player.face_dir = -1, '아래쪽'
        pass

    @staticmethod
    def exit(player, e):
        pass

    @staticmethod
    def do(player):
        # 이동하는 코드 작성
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3
        player.x += player.LR_dir * RUN_SPEED_PPS * game_framework.frame_time
        player.x = clamp(player.z - 30, player.x, 800 + 30 - player.z)
        # player.x = clamp(35, player.x, 800 - 35)
        player.z += player.TB_dir * RUN_SPEED_PPS * game_framework.frame_time
        player.z = clamp(35, player.z, 145 - 35)

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
        player.image.clip_draw(int(player.frame) * 70, player.move_dir * 80, 50, 80, player.x, player.z);
        pass


class Jump:
    @staticmethod
    def enter(player, e):
        player.jump_time = get_time()  # pico2d import 필요
        player.current_time = player.jump_time
        player.height = player.z
        pass

    @staticmethod
    def exit(player, e):
        player.z = player.height
        pass

    @staticmethod
    def do(player):
        current_time = get_time() - player.jump_time

        if current_time > TIME_PER_JUMP:
            player.state_machine.handle_event(('TIME_OUT', 0))
        elif player.current_time < TIME_PER_JUMP / 2.0:
            player.z += JUMP_SPEED_PPS * game_framework.frame_time
        else:
            player.z -= JUMP_SPEED_PPS * game_framework.frame_time

        player.current_time = current_time
        pass

    @staticmethod
    def draw(player):
        player.image.clip_draw(int(player.frame) * 70, player.move_dir * 80, 50, 80, player.x, player.z);
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
            Jump: {time_out: Idle}
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
    shadow_image = None

    def __init__(self, dir):
        self.x, self.y = 0, 0
        self.height = 0
        self.frame = 6
        self.state_machine = StateMachine(self)
        self.LR_dir = 0  # 좌우 이동하는 방향 (로직)
        self.TB_dir = 0  # 상하 이동하는 방향 (로직)
        self.build_behavior_tree()
        self.bt = None
        if dir == '오른쪽':
            self.racket = Racket(90.0)
            game_world.add_object(self.racket, 1)
            game_world.add_collision_pair('racket:shuttle', self.racket, None)

            self.x, self.z = 300, 60
            self.face_dir = dir  # 바라보는 방향 (방향 파악)
            self.move_dir = 1  # 바라보는 방향 (이미지 위치)

        elif dir == '왼쪽':
            self.racket = Racket(0.0)
            game_world.add_object(self.racket, 1)
            game_world.add_collision_pair('racket:shuttle', self.racket, None)

            self.x, self.z = 800 - 300, 60
            self.face_dir = dir  # 바라보는 방향 (방향 파악)
            self.move_dir = 2  # 바라보는 방향 (이미지 위치)
            self.build_behavior_tree()

        if Player.image == None:
            Player.image = load_image('resource/character.png')  # 70 x 80 크기 스프라이트
        if Player.shadow_image == None:
            Player.shadow_image = load_image('resource/shuttle_shadow.png')  # 200 x 225 size

    def update(self):
        self.state_machine.update()
        self.racket.x = self.x
        self.racket.z = self.z
        if self.bt:
            self.bt.run()

    def handle_event(self, e):
        self.state_machine.handle_event(('INPUT', e))
        self.racket.state_machine.handle_event(('INPUT', e))

    def draw(self):
        self.state_machine.draw()
        draw_rectangle(*self.get_bb())
        pass

    def get_bb(self):
        return self.x - 35, self.z - 40, self.x + 35, self.z + 40

    def handle_collision(self, group, other):
        if group == 'player:net':
            if self.x < other.x:
                self.x = clamp(0, self.x, other.x - 20)
            else:
                self.x = clamp(other.x + 10, self.x, 800)
            pass

    def distance_less_than(self, x1, y1, x2, y2, r):
        distance2 = (x1 - x2) ** 2 + (y1 - y2) ** 2
        return distance2 < (PIXEL_PER_METER * r) ** 2

    def is_last_touching(self):  # 내가 마지막으로 쳤다면 FAIL
        if play_mode.shuttle.last_touch == self.racket:
            return BehaviorTree.FAIL
        return BehaviorTree.SUCCESS

    def move_slightly_to(self, tx, ty):
        self.dir = math.atan2(ty - self.y, tx - self.x)
        self.speed = RUN_SPEED_PPS
        self.x += self.speed * math.cos(self.dir) * game_framework.frame_time
        self.y += self.speed * math.sin(self.dir) * game_framework.frame_time

    pass

    def move_to_shuttle(self, r=20.0):
        self.move_slightly_to(play_mode.shuttle.x, play_mode.shuttle.y)
        if self.distance_less_than(play_mode.shuttle.x, play_mode.shuttle.y, self.x, self.y, r):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def swing_racket(self):
        if self.racket.state_machine is not Swing and self.racket.z - 30.0 < play_mode.shuttle.z < self.racket.z + 30.0:
            self.racket.state_machine.handle_event(('bt_swing', 0))
            return BehaviorTree.SUCCESS
        return BehaviorTree.FAIL

    def is_on_right_side(self):
        if play_mode.shuttle.x >= 400:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def move_to_center(self, r=0.3):
        if self.distance_less_than(600, 50, self.x, self.y, r):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def is_shuttle_face_right(self):
        if play_mode.shuttle.velocity[0] > 0:
            return BehaviorTree.SUCCESS
        return BehaviorTree.FAIL

    def is_left_side_from_self(self):
        if play_mode.shuttle.x < self.x:
            return BehaviorTree.SUCCESS
        return BehaviorTree.FAIL

    def is_low_than_racket(self):
        if (self.y + 35) ** 2 < self.racket.z ** 2:
            return BehaviorTree.SUCCESS
        return BehaviorTree.FAIL

    def build_behavior_tree(self):

        a1 = Action('라켓을 휘두른다', self.swing_racket)
        c1 = Condition('마지막으로 친 상대가 플레이어인가?', self.is_last_touching)  # 내가 마지막으로 쳤다면 FAIL
        a2 = Action('셔틀콕을 향해 이동', self.move_to_shuttle)
        c2 = Condition('셔틀콕이 내 코트쪽에 있는가?', self.is_on_right_side)
        c3 = Condition('셔틀콕이 향하는 방향이 우측인가?', self.is_shuttle_face_right)
        c5 = Condition('셔틀콕이 나보다 좌측에 있는가?', self.is_left_side_from_self)
        c6 = Condition('셔틀콕의 높이가 라켓의 높이보다 낮은가?', self.is_low_than_racket)
        a3 = Action('코트의 중앙으로 이동', self.move_to_center)


        SEQ_CHECK_SWING = Sequence('라켓을 휘둘러야 하는가?', a1)
        SEQ_MOVE_TO_SHUTTLE = Sequence('이동을 셔틀콕을 향해', a2)

        # 공격
        SEQ_ATTACK = Sequence('공격태세', SEQ_MOVE_TO_SHUTTLE, SEQ_CHECK_SWING)
        # 공격 판단
        SEQ_CHECK_MYTURN = Sequence('내가 공격할 차례인가?', c1, c2)
        SEQ_ATTACK_CHECK = Sequence('공격판단중', c1, c2, SEQ_ATTACK)

        # 수비
        SEQ_DEPEND = Sequence('수비태세', a3)

        root = SEL_ATTACK_or_DEFEND = Selector('공격 또는 수비', SEQ_ATTACK_CHECK, SEQ_DEPEND)
        self.bt = BehaviorTree(root)
