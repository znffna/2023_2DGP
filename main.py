from pico2d import *
import game_framework

import game_mode as start_mode
from player import Player



# 게임 시작

open_canvas()
game_framework.run(start_mode)
close_canvas()
