import game_framework
from pico2d import *

from player import Player
from slime import SLIME
import game_world

player = None
slime = None

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
    global player, slime

    player = Player()
    game_world.add_object(player, 1)

    slimes = [SLIME() for _ in range(3)]
    game_world.add_objects(slimes, 1)

    game_world.add_collision_pair('player:slime', player, None)
    for slime in slimes:
        game_world.add_collision_pair('player:slime', None, slime)
        game_world.add_collision_pair('slime:attack', slime, None)



def update():
    game_world.update()
    game_world.handle_collisions()


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()


def finish():
    game_world.clear()
    pass


def pause():
    pass

def resume():
    pass