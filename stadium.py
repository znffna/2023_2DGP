from pico2d import *


class Stadium:
    def __init__(self):
        self.image = load_image('resource/playstage.png')
        self.x, self.y = 400, 300

    def update(self):
        pass

    def draw(self):
        self.image.draw(400, 300)
        draw_rectangle(*self.get_bb())
        # self.image.draw(1200, 30)

    def get_bb(self):  # Net
        return 380, 0, 410, 150

    def handle_collision(self, group, other):
        pass
