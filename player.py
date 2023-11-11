from pico2d import *


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


def time_out(e):
    return e[0] == 'TIME_OUT'


# 상태에 대한 클래스

class Idle:  # 가만히 있음
    @staticmethod
    def enter(player, e):
        if player.face_dir == -1:
            player.move_dir = 2
        elif player.face_dir == 1:
            player.move_dir = 1
        elif player.face_dir == 2:
            player.move_dir = 0
        elif player.face_dir == -2:
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
        player.frame = (player.frame - 6 + 1) % 6 + 6
        pass

    @staticmethod
    def draw(player):
        player.image.clip_draw(player.frame * 70, player.move_dir * 80, 50, 70, player.x, player.y);
        pass


class MoveHorizon:  # 좌우 이동 중
    @staticmethod
    def enter(player, e):
        player.frame = 0
        if right_down(e) or left_up(e):  # 오른쪽으로 RUN
            player.LR_dir, player.move_dir, player.face_dir = 1, 5, 1
        elif left_down(e) or right_up(e):  # 왼쪽으로 RUN
            player.LR_dir, player.move_dir, player.face_dir = -1, 6, -1
        elif up_down(e) or down_up(e) or down_down(e) or up_up(e):
            if player.LR_dir == 1:
                player.move_dir, player.face_dir = 5, 1
            else:
                player.move_dir, player.face_dir = 6, -1

        pass

    @staticmethod
    def exit(player, e):
        pass

    @staticmethod
    def do(player):
        # 이동하는 코드 작성
        player.frame = (player.frame + 1) % 3
        player.x += player.LR_dir * 5
        player.x = clamp(35, player.x, 800 - 35)
        pass

    @staticmethod
    def draw(player):
        player.image.clip_draw(player.frame * 70, player.move_dir * 80, 50, 70, player.x, player.y);
        pass


class MoveVertical:  # 상하 이동 중
    @staticmethod
    def enter(player, e):
        player.frame = 0
        if up_down(e) or down_up(e):  # 위쪽으로 RUN
            player.TB_dir, player.move_dir, player.face_dir = 1, 4, 2
        elif down_down(e) or up_up(e):  # 아래로 RUN
            player.TB_dir, player.move_dir, player.face_dir = -1, 7, -2
        elif right_down(e) or left_up(e) or left_down(e) or right_up(e):
            if player.TB_dir == 1:
                player.move_dir, player.face_dir = 4, 2
            else:
                player.move_dir, player.face_dir = 7, -2


    @staticmethod
    def exit(player, e):
        pass

    @staticmethod
    def do(player):
        # 이동하는 코드 작성
        player.frame = (player.frame + 1) % 3
        player.y += player.TB_dir * 5
        player.y = clamp(35, player.y, 200 - 35)
        pass

    @staticmethod
    def draw(player):
        player.image.clip_draw(player.frame * 70, player.move_dir * 80, 50, 70, player.x, player.y);
        pass


class MoveDiagonal:  # 대각선 이동 중
    @staticmethod
    def enter(player, e):
        player.frame = 0
        if right_down(e) or left_up(e):  # 오른쪽으로 RUN
            player.LR_dir, player.move_dir, player.face_dir = 1, 5, 1
        elif left_down(e) or right_up(e):  # 왼쪽으로 RUN
            player.LR_dir, player.move_dir, player.face_dir = -1, 6, -1
        elif up_down(e) or down_up(e):  # 위쪽으로 RUN
            player.TB_dir, player.move_dir, player.face_dir = 1, 4, 2
        elif down_down(e) or up_up(e):  # 아래로 RUN
            player.TB_dir, player.move_dir, player.face_dir = -1, 7, -2
        pass

    @staticmethod
    def exit(player, e):
        pass

    @staticmethod
    def do(player):
        # 이동하는 코드 작성
        player.frame = (player.frame + 1) % 3
        player.x += player.LR_dir * 5
        player.x = clamp(35, player.x, 800 - 35)
        player.y += player.TB_dir * 5
        player.y = clamp(35, player.y, 200 - 35)
        pass

    @staticmethod
    def draw(player):
        player.image.clip_draw(player.frame * 70, player.move_dir * 80, 50, 70, player.x, player.y);
        pass


class StateMachine:
    def __init__(self, player):
        self.player = player
        self.cur_state = Idle
        self.transitions = {
            Idle: {right_down: MoveHorizon, left_down: MoveHorizon, right_up: MoveHorizon, left_up: MoveHorizon,
                   up_down: MoveVertical, down_up: MoveVertical, down_down: MoveVertical, up_up: MoveVertical},
            MoveHorizon: {right_down: Idle, left_down: Idle, right_up: Idle, left_up: Idle
                          ,up_down: MoveDiagonal, down_up: MoveDiagonal, down_down: MoveDiagonal, up_up: MoveDiagonal},
            MoveVertical: {right_down: MoveDiagonal, left_down: MoveDiagonal, right_up: MoveDiagonal, left_up: MoveDiagonal
                          ,up_down: Idle, down_up: Idle, down_down: Idle, up_up: Idle},
            MoveDiagonal: {right_down: MoveVertical, left_down: MoveVertical, right_up: MoveVertical, left_up: MoveVertical
                          ,up_down: MoveHorizon, down_up: MoveHorizon, down_down: MoveHorizon, up_up: MoveHorizon},
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

    def __init__(self):
        self.x, self.y = 400, 60
        self.frame = 0
        self.state_machine = StateMachine(self)
        self.LR_dir = 0  # 좌우 이동하는 방향 (로직)
        self.TB_dir = 0  # 상하 이동하는 방향 (로직)
        self.face_dir = 1  # 바라보는 방향 (방향 파악)
        self.move_dir = 0  # 바라보는 방향 (이미지 위치)

        if Player.image == None:
            Player.image = load_image('resource/character.png')  # 70 x 80 크기 스프라이트

    def update(self):
        self.state_machine.update()

    def handle_event(self, e):
        self.state_machine.handle_event(('INPUT', e))

    def draw(self):
        self.state_machine.draw()
        pass
