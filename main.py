from pico2d import *


class Player:
    image = None

    def __init__(self):
        print('Player 생성')
        self.x, self.y = 400, 60
        self.frame = 0
        if Player.image == None:
            Player.image = load_image('resource/character.png')  # 70 x 80 크기 스프라이트
        pass

    def update(self):
        print('Player.update')
        self.frame = (self.frame + 1) % 3
        pass

    def handle_event(self):
        pass

    def draw(self):
        print('Player.draw')
        # Player.image.draw(self.x, self.y)
        Player.image.clip_draw(self.frame * 70, 400, 50, 70, self.x, self.y);
        pass

    pass


def create_world():
    global running
    global player
    running = True

    player = Player()
    pass


def handle_events():
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
    pass


def update_world():
    player.update()
    pass


def render_world():
    clear_canvas()
    player.draw()

    update_canvas()
    pass


open_canvas()
create_world()

while running:
    handle_events()
    update_world()
    render_world()
    delay(0.05)

close_canvas()
