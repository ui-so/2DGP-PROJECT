import game_framework
from pico2d import *

from back_1 import Back1
from back_2 import Back2
from player import Player
from slime import SLIME
from P_slime import P_SLIME
import game_world

back_1 = None
back_2 = None
player = None
slimes = None
P_slimes = None

MAP = 0

def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            player.handle_event(event)


def init():
    global player, slimes, P_slimes, back_1, back_2

    back_1 = Back1()
    game_world.add_object(back_1, 0)
    back_2 = Back2()
    game_world.add_object(back_2, 2)

    player = Player()
    game_world.add_object(player, 1)

    slimes = [SLIME() for _ in range(3)]
    game_world.add_objects(slimes, 1)

    P_slimes = [P_SLIME() for _ in range(3)]
    game_world.add_objects(P_slimes, 1)

    for slime in P_slimes:
        game_world.add_collision_pair('slime:catch', slime, None)

    game_world.add_collision_pair('player:slime', player, None)
    for slime in slimes:
        game_world.add_collision_pair('player:slime', None, slime)
        game_world.add_collision_pair('slime:attack', slime, None)



def update():
    global player, back_1,back_2, slimes, P_slimes, MAP
    game_world.update()
    if MAP == 0:
        if player.x < 50 and player.y < 434 and player.y > 334:
            back_1.x = 0
            back_1.y = 0
            back_2.x = 0
            back_2.y = 0
            player.x = 512
            player.y = 384
            for(o) in slimes:
                game_world.remove_object(o)
            for(o) in P_slimes:
                game_world.remove_object(o)
            MAP = 1
    game_world.handle_collisions()


def draw():
    clear_canvas()
    game_world.render()
    if MAP == 0:
        draw_rectangle(0, 334, 50, 434)
    update_canvas()


def finish():
    game_world.clear()
    pass


def pause():
    pass

def resume():
    pass