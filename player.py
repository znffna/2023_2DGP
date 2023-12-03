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

PIXEL_PER_HEIGHT_METER = (3.0 / 0.3)  # 3 pixel 30 cm
RUN_HEIGHT_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_HEIGHT_METER)

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
        player.image.clip_draw(int(player.frame) * 70, player.move_dir * 80, 50, 80, player.x, player.y);
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
        player.z += player.TB_dir * RUN_HEIGHT_SPEED_PPS * game_framework.frame_time
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
        player.y += player.TB_dir * RUN_HEIGHT_SPEED_PPS * game_framework.frame_time
        player.y = clamp(35, player.z, 145 - 35)

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
        player.move_dir = 5 if player.dir == '오른쪽' else 6
        pass

    @staticmethod
    def exit(player, e):
        player.height = 0.0
        player.move_dir -= 4
        pass

    @staticmethod
    def do(player):
        current_time = get_time() - player.jump_time
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3
        if current_time > TIME_PER_JUMP:
            player.state_machine.handle_event(('TIME_OUT', 0))
        elif player.current_time < TIME_PER_JUMP / 2.0:
            player.height += JUMP_SPEED_PPS * game_framework.frame_time
        else:
            player.height -= JUMP_SPEED_PPS * game_framework.frame_time

        player.current_time = current_time
        pass

    @staticmethod
    def draw(player):
        player.image.clip_draw(int(player.frame) * 70, player.move_dir * 80, 50, 80, player.x,
                               player.y + player.height);
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
        self.speed = 1.0  # 스탯
        self.state_machine = StateMachine(self)
        self.LR_dir = 0  # 좌우 이동하는 방향 (로직)
        self.TB_dir = 0  # 상하 이동하는 방향 (로직)
        self.build_behavior_tree()
        self.bt = None
        self.point = 0  # 플레이어 점수

        if dir == '오른쪽':
            self.racket = Racket(90.0)
            game_world.add_object(self.racket, 1)
            game_world.add_collision_pair('racket:shuttle', self.racket, None)

            self.x, self.y = 300, 60
            self.face_dir = dir  # 바라보는 방향 (방향 파악)
            self.move_dir = 1  # 바라보는 방향 (이미지 위치)

        elif dir == '왼쪽':
            self.racket = Racket(0.0)
            game_world.add_object(self.racket, 1)
            game_world.add_collision_pair('racket:shuttle', self.racket, None)

            self.x, self.y = 800 - 300, 60
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
        self.racket.y = self.y
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
        return self.x - 35, self.y - 40, self.x + 35, self.y + 40

    def point_position(self):
        return (200, 500) if dir == '오른쪽' else (600, 500)

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
        self.dir = math.atan2(ty - self.y, tx + 30 - self.x)
        dir = math.cos(self.dir)
        dir /= math.fabs(dir)
        self.x += dir * self.speed * RUN_SPEED_PPS * game_framework.frame_time  # * math.cos(self.dir)
        self.y += self.speed * RUN_HEIGHT_SPEED_PPS * math.sin(self.dir) * game_framework.frame_time
    pass

    def move_slightly_from(self, tx, ty):
        self.dir = math.atan2(ty - self.y, self.x - tx)
        dir = math.cos(self.dir)
        dir /= math.fabs(dir)
        self.x += dir * self.speed * RUN_SPEED_PPS * game_framework.frame_time  # * math.cos(self.dir)
        self.y += self.speed * RUN_HEIGHT_SPEED_PPS * math.sin(self.dir) * game_framework.frame_time
        self.x = clamp(self.y - 30, self.x, 800 + 30 - self.y)
        self.y = clamp(35, self.y, 145 - 35)

    def move_to_shuttle(self, r=50.0):
        print("move_to_shuttle")
        self.move_slightly_to(play_mode.shuttle.x, play_mode.shuttle.y + 35)
        if self.distance_less_than(play_mode.shuttle.x, play_mode.shuttle.y, self.x, self.y, r):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def move_from_shuttle(self, r=50.0):
        print("move_from_shuttle")
        self.move_slightly_from(play_mode.shuttle.x + play_mode.shuttle.velocity[0],
                                play_mode.shuttle.y + play_mode.shuttle.velocity[1])
        if self.distance_less_than(play_mode.shuttle.x, play_mode.shuttle.y, self.x, self.y, r):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def swing_racket(self):
        if self.racket.state_machine is not Swing and self.racket.y - 30.0 < play_mode.shuttle.z < self.racket.y + 30.0:
            self.racket.state_machine.handle_event(('bt_swing', 0))
            return BehaviorTree.SUCCESS
        return BehaviorTree.SUCCESS

    def is_on_right_side(self):
        if play_mode.shuttle.x >= 400:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def move_to_center(self, r=0.3):
        if self.distance_less_than(600, 50, self.x, self.y, r):
            return BehaviorTree.SUCCESS
        else:
            self.move_slightly_to(600, 50)
            return BehaviorTree.RUNNING

    def is_shuttle_speed_high(self):
        if play_mode.shuttle.velocity[1] > 0.0:
            return BehaviorTree.SUCCESS
        return BehaviorTree.FAIL

    def is_shuttle_face_right(self):
        if play_mode.shuttle.velocity[0] > 0.0:
            return BehaviorTree.SUCCESS
        return BehaviorTree.FAIL

    def is_left_side_from_self(self):
        if play_mode.shuttle.x < self.x:
            return BehaviorTree.SUCCESS
        return BehaviorTree.FAIL

    def is_racket_distance(self):
        # TODO 거리계산
        if (play_mode.shuttle.x - self.x) ** 2 + (play_mode.shuttle.y - self.y) ** 2 + (
                play_mode.shuttle.z - self.height) ** 2 < 150 ** 2:
            return BehaviorTree.SUCCESS
        return BehaviorTree.FAIL

    def move_to_shuttle_dest(self, r = 0.5): # 셔틀콕의 현재 기울기의 도착점으로 이동하는거
        if play_mode.shuttle.velocity[1] < 0.0 and abs(play_mode.shuttle.velocity[0]) > RUN_SPEED_PPS:
            dir = math.atan2(play_mode.shuttle.velocity[0], play_mode.shuttle.velocity[1])
            c = play_mode.shuttle.y + play_mode.shuttle.z + dir * play_mode.shuttle.x
            x = -c / dir
            self.move_slightly_from(x, play_mode.shuttle.y)
        else:
            self.move_slightly_from(play_mode.shuttle.x, play_mode.shuttle.y)

        if self.distance_less_than(play_mode.shuttle.x, play_mode.shuttle.y, self.x, self.y, r):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.SUCCESS

    def build_behavior_tree(self):

        a1 = Action('라켓을 휘두른다', self.swing_racket)
        c1 = Condition('마지막으로 친 상대가 플레이어인가?', self.is_last_touching)  # 내가 마지막으로 쳤다면 FAIL
        a2 = Action('셔틀콕을 향해 이동', self.move_to_shuttle)
        c2 = Condition('셔틀콕이 내 코트쪽에 있는가?', self.is_on_right_side)
        c3 = Condition('셔틀콕이 향하는 방향이 우측인가?', self.is_shuttle_face_right)
        c5 = Condition('셔틀콕이 나보다 좌측에 있는가?', self.is_left_side_from_self)
        # c6 = Condition('셔틀콕의 높이가 라켓의 높이보다 낮은가?', self.is_low_than_racket)
        a3 = Action('코트의 중앙으로 이동', self.move_to_center)
        c7 = Condition('셔틀콕이 캐릭터의 라켓범위 안에 있는가?', self.is_racket_distance)
        a4 = Action('셔틀콕 반대로 이동', self.move_from_shuttle)
        c8 = Condition('셔틀콕이 향하는 속도가 선수보다 빠른가?', self.is_shuttle_speed_high)
        a5 = Action('셔틀콕의 도착지점으로 이동', self.move_to_shuttle_dest)
        # 스윙 판단 : 현재 라켓의 사거리 안에 있을시 라켓스윙 수행.
        SEQ_CHECK_SWING = Sequence('라켓을 휘둘러야 하는가?', c7, a1)

        # 공격 이동: 셔틀콕의 속도에 따라 이동방향 결정
        SEQ_MOVE_TO_SHUTTLE = Sequence('셔틀콕 방향 이동', c8, a2)
        SEL_MOVE_TO_OR_FROM = Selector('셔틀콕을 치기위해 이동', SEQ_MOVE_TO_SHUTTLE, a5)

        # 공격 액션 - 이동하고 범위안에 셔틀콕 존재시 스윙도 수행
        SEQ_SWING_AND_MOVE = Sequence('스윙 및 이동', SEQ_CHECK_SWING, SEL_MOVE_TO_OR_FROM)
        SEQ_JUST_MOVE = Sequence('오직 이동', SEL_MOVE_TO_OR_FROM)
        SEL_ATTACK_ACTION = Selector('공격태세', SEQ_SWING_AND_MOVE, SEQ_JUST_MOVE)

        # 공격 판단 - 공이 우측으로 향하거나 코트위에 있으면 SUCCESS 리턴
        SEL_ATTACK_CHECK = Selector('현재 공격을 해야하는가?', c3, c2)

        # 공격 - 공격할 차례가 아니면 CHECK에서 FAIL 리턴
        SEQ_ATTACK = Sequence('공격', SEL_ATTACK_CHECK, SEL_ATTACK_ACTION)

        # 수비
        SEQ_DEPEND = Sequence('수비', a3)

        root = SEL_ATTACK_or_DEFEND = Selector('공격 또는 수비', SEQ_ATTACK, SEQ_DEPEND)
        self.bt = BehaviorTree(root)
