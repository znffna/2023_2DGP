from math import radians

from pico2d import *


class Shuttle:
    image = None

    def __init__(self):
        self.x, self.y = 400, 500
        self.size = 10
        self.degree = 0.0
        if Shuttle.image == None:
            Shuttle.image = load_image('resource/shuttle.png')  # 200 x 225 size

    def update(self):
        pass

    def draw(self):
        Shuttle.image.clip_composite_draw(0, 0, 200, 225, radians(self.degree), ''
                                          , self.x, self.y, self.size, self.size)
        draw_rectangle(*self.get_bb())
        # self.image.draw(1200, 30)

    def get_bb(self):  # shuttle size
        return self.x - self.size, self.y - self.size, self.x + self.size, self.y + self.size

    def handle_collision(self, group, other):
        pass
