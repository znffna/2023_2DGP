from math import radians, atan, degrees

from pico2d import *

import game_framework

def get_degree(m):
    radian = atan(m)
    return degrees(radian)


class Shuttle:
    image = None

    def __init__(self):
        self.x, self.y = 300, 30
        self.x_distance = 0
        self.height = 400
        self.velocity = 0.0
        self.accelate = 0.0

        self.size = 10
        self.degree = 0.0

        if Shuttle.image == None:
            Shuttle.image = load_image('resource/shuttle.png')  # 200 x 225 size

    def update(self):
        if self.height > 0:
            self.height += self.velocity * game_framework.frame_time
            self.velocity += self.accelate
            self.velocity = clamp(-1000.0, self.velocity, 1000.0)
            self.accelate -= 9.8 * game_framework.frame_time
        else:
            self.accelate = 0
            self.velocity = 0
            self.height = 0
        pass

    def draw(self):
        Shuttle.image.clip_composite_draw(0, 0, 200, 225, radians(self.degree), ''
                                          , self.x, self.y + self.height, self.size, self.size)
        draw_rectangle(*self.get_bb())
        # self.image.draw(1200, 30)

    def get_bb(self):  # shuttle size
        return self.x - self.size, self.y + self.height - self.size, self.x + self.size, self.y + self.height + self.size

    def handle_collision(self, group, other):
        pass
