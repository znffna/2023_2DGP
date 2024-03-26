from pico2d import *
import random
# Game object class here


class Grass:
    def __init__(self):
        self.image = load_image('grass.png')

    def draw(self):
        self.image.draw(400, 30)

    def update(self): pass


class Boy:
    def __init__(self):
        self.x, self.y = random.randint(100, 700), 90
        self.frame = random.randint(0, 7)
        self.image = load_image('run_animation.png')

    def update(self):
        self.frame = (self.frame + 1) % 8
        self.x += 5

    def draw(self):
        self.image.clip_draw(self.frame * 100, 0, 100, 100, self.x, self.y)


class Ball:
    def __init__(self):
        self.x, self.y, self.size = random.randint(100, 700), 599, random.randint(0, 1)
        self.image = load_image('ball21x21.png') if self.size == 0 else load_image('ball41x41.png')
        self.speed = random.randint(3, 15)

    def draw(self):
        self.image.draw(self.x, self.y, (self.size+1)*20, (self.size+1)*20)

    def update(self):
        self.y = self.y - self.speed if self.y > 60 + (self.size+1) * 10 else 60 + (self.size+1)*10


def handle_events():
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False



def reset_world():
    global running
    global grass
    global team
    global world
    global sball
    global bball


    running = True
    world = []

    grass = Grass()
    world.append(grass)

    team = [Boy() for i in range(11)]
    world += team

    ball = [Ball() for i in range(20)]
    world += ball


def update_world():
    grass.update()
    for o in world:
        o.update()
    pass


def render_world():
    clear_canvas()
    for o in world:
        o.draw()
    update_canvas()
    pass


open_canvas()
# initialization code
reset_world()

# game main loop code
while running:
    handle_events()
    update_world()
    render_world()
    delay(0.05)


# finalization code
close_canvas()
