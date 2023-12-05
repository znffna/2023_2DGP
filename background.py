from pico2d import *


class BackGround:
    def __init__(self):
        self.image = load_image('resource/playstage.png')
        self.x, self.y = 400, 300
        self.height = 100
        self.bgm = load_music('resource/inplaying.mp3')
        self.bgm.set_volume(32)
        self.bgm.repeat_play()

    def update(self):
        pass

    def draw(self):
        self.image.draw(400, 300)
        # self.image.draw(1200, 30)

    def get_bb(self):  # Net
        return 380, 0, 410, 120

    def handle_collision(self, group, other):
        pass

