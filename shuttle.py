from math import radians, atan, degrees, cos, sin

from pico2d import *

import game_framework
from racket import Swing


def get_degree(m):
    radian = atan(m)
    return degrees(radian)


PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm


class Shuttle:
    image = None

    def __init__(self):
        self.last_touch = None
        self.x, self.y, self.z = 300, 30, 400
        self.velocity = [0.0, 0.0]
        self.accelate = [0.0, -9.8]

        self.cooldown = get_time()
        self.size = 20
        self.degree = 0.0


        if Shuttle.image == None:
            Shuttle.image = load_image('resource/shuttle.png')  # 200 x 225 size

    def update(self):
        self.x += self.velocity[0] * game_framework.frame_time
        self.z += self.velocity[1] * game_framework.frame_time

        self.velocity[0] += self.accelate[0] * PIXEL_PER_METER * game_framework.frame_time
        self.velocity[1] += self.accelate[1] * PIXEL_PER_METER * game_framework.frame_time
        if self.velocity[0] != 0:
            self.degree = get_degree(self.velocity[1]/self.velocity[0]) + 90.0

        self.x = clamp(0, self.x, 800)
        self.z = clamp(0, self.z, 600)

        if self.x == 0 or self.x == 800:
            self.velocity[0] *= -0.5
            self.accelate[0] *= -1

        if self.z == 0:
            self.velocity[0] = 0.0
            self.velocity[1] = 0.0
            pass

    def draw(self):
        Shuttle.image.clip_composite_draw(0, 0, 200, 225, radians(self.degree), ''
                                          , self.x, self.y + self.z, self.size, self.size)
        draw_rectangle(*self.get_bb())
        # self.image.draw(1200, 30)

    def get_bb(self):  # shuttle size
        return self.x - self.size, self.y + self.z - self.size, self.x + self.size, self.y + self.z + self.size

    def handle_collision(self, group, other):
        if group == 'racket:shuttle' and other.state_machine.cur_state == Swing and self.last_touch != other:
            if get_time() - self.cooldown > 0.5:
                self.velocity[0] = 400.0 * cos(radians(other.racket_rad + 90.0))
                self.velocity[1] = 400.0 * sin(radians(other.racket_rad + 90.0))
                self.degree = other.racket_rad + 90.0
                self.cooldown = get_time()
                self.last_touch = other
        if group == 'shuttle:net':
            self.velocity[0] *= -0.5
            self.accelate[0] *= -1
            self.velocity[1] = -400.0
        pass
