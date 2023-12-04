from math import radians, atan, degrees, cos, sin

from pico2d import *

import game_framework
import play_mode
from racket import Swing


def get_degree(m):
    radian = atan(m)
    return degrees(radian)


PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm


class Shuttle:
    image = None
    shadow_image = None
    hit_sound = None
    def __init__(self):
        self.last_touch = None
        self.x, self.y, self.z = 200, 30, 400
        self.velocity = [0.0, 0.0]
        self.accelate = [0.0, -9.8]
        self.move_in_air = True
        self.cooldown = get_time()
        self.size = 20
        self.degree = 0.0
        self.restart_timer = get_time()
        self.start_spot = 'Player'

        if Shuttle.image == None:
            Shuttle.image = load_image('resource/shuttle.png')  # 200 x 225 size
        if Shuttle.shadow_image == None:
            Shuttle.shadow_image = load_image('resource/shuttle_shadow.png')  # 200 x 225 size
        if Shuttle.hit_sound == None:
            Shuttle.hit_sound = load_wav('resource/hit.wav')
            Shuttle.hit_sound.set_volume(32)

    def update(self):
        # 판이 끝났을때 판을 초기화 하고 다시 시작되는 코드
        if not self.move_in_air:
            if get_time() - self.restart_timer > 1.5:
                self.x = 200 if self.start_spot == 'Player' else 600
                self.y = 30
                self.z = 300
                self.last_touch = None
                self.move_in_air = True
                self.velocity[0] = 0.0
                self.velocity[1] = 0.0

        # 이동 업데이트
        self.x += self.velocity[0] * game_framework.frame_time
        self.z += self.velocity[1] * game_framework.frame_time

        self.velocity[0] += self.accelate[0] * (self.velocity[0] / 100) * PIXEL_PER_METER * game_framework.frame_time
        self.velocity[1] += self.accelate[1] * PIXEL_PER_METER * game_framework.frame_time
        if self.velocity[0] != 0:
            self.degree = get_degree(self.velocity[1] / self.velocity[0]) + 90.0

        self.x = clamp(0, self.x, 800)
        self.z = clamp(0, self.z, 600)
        if self.z == 0 and self.move_in_air:
            self.move_in_air = False
            self.restart_timer = get_time()
            if self.x > 400:
                play_mode.player.point += 1
                self.start_spot = 'Player'
            else:
                play_mode.ai_player.point += 1
                self.start_spot = 'AI'

        if self.x == 0 or self.x == 800:
            self.velocity[0] *= -0.5
            self.accelate[0] *= -1

        if self.z == 0:
            self.velocity[0] = 0.0
            self.velocity[1] = 0.0
            pass

    def draw(self):
        Shuttle.shadow_image.clip_composite_draw(0, 0, 200, 200, 0, ''
                                                 , self.x, self.y - 5, self.size, self.size)
        Shuttle.image.clip_composite_draw(0, 0, 200, 225, radians(self.degree), ''
                                          , self.x, self.y + self.z, self.size, self.size)
        draw_rectangle(*self.get_bb())

        # self.image.draw(1200, 30)

    def get_bb(self):  # shuttle size
        return self.x - self.size // 2, self.y + self.z - self.size // 2, self.x + self.size // 2, self.y + self.z + self.size // 2

    def get_shadow(self):
        return self.x - self.size, self.y - self.size, self.x + self.size, self.y + self.size

    def handle_collision(self, group, other):
        if group == 'racket:shuttle' and other.state_machine.cur_state == Swing:
            if get_time() - self.cooldown > 0.5:
                other_rad = other.default_rad
                # if other_rad == 0.0:
                #     other_rad = 270.0
                self.velocity[0] = 600.0 * cos(radians(other.racket_rad + 90.0))
                self.velocity[1] = 400.0 * sin(radians(other.racket_rad + 90.0))
                self.degree = other.racket_rad + 90.0
                # if other.swing_dir == -1:
                #     self.velocity[0] = 600.0 * cos(radians(other.racket_rad + 90.0))
                #     self.velocity[1] = 400.0 * sin(radians(other.racket_rad + 90.0))
                #     self.degree = other.racket_rad + 90.0
                # else:
                #     self.velocity[0] = 600.0 * cos(radians(other.racket_rad + 270.0))
                #     self.velocity[1] = 400.0 * sin(radians(other.racket_rad + 270.0))
                #     self.degree = other.racket_rad + 270.0
                self.cooldown = get_time()
                self.last_touch = other
                Shuttle.hit_sound.play()
        if group == 'shuttle:net':
            self.velocity[0] *= -0.5
            self.accelate[0] *= -1
            self.velocity[1] = -400.0
        pass
