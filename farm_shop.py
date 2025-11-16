from pico2d import *

import game_framework
import game_world
import play_mode
from pannel import Pannel
import player

pannel = None

def init():
    global pannel

    pannel = Pannel()
    game_world.add_object(pannel,3)
    pass

def finish():
    game_world.remove_object(pannel)

def update():
    pass

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                global player
                player.right_pressed = False
                player.left_pressed = False
                player.up_pressed = False
                player.down_pressed = False
                player.dir_x = 0
                player.dir_y = 0
                game_framework.pop_mode()
            elif event.key == SDLK_0:
                play_mode.boy.item = None
                game_framework.pop_mode()
            elif event.key == SDLK_1:
                play_mode.boy.item = 'Ball'
                game_framework.pop_mode()
            elif event.key == SDLK_2:
                play_mode.boy.item = 'BigBall'
                game_framework.pop_mode()


def pause():
    pass

def resume():
    pass