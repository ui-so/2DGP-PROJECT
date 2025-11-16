import game_framework
from pico2d import *
import play_mode as start_mode

open_canvas(1024, 768)
game_framework.run(start_mode)
close_canvas()