import game_framework
from pico2d import *

from ui import Ui
from back_1 import Back1
from back_2 import Back2
from player import Player
from slime import SLIME
from P_slime import P_SLIME
import game_world
import farm_shop

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
        elif event.type == SDL_KEYDOWN and event.key == SDLK_e:
            if MAP == 1:
                global player
                if player.x > 350 and player.x < 400 and player.y > 374 and player.y < 484:
                    game_framework.push_mode(farm_shop)

            pass
        else:
            player.handle_event(event)


def init():
    global player, slimes, P_slimes, back_1, back_2, ui

    back_1 = Back1()
    game_world.add_object(back_1, 0)
    back_2 = Back2()
    game_world.add_object(back_2, 2)

    player = Player()
    game_world.add_object(player, 1)

    slimes = [SLIME() for _ in range(5)]
    game_world.add_objects(slimes, 1)

    green_slimes = [P_SLIME(1) for _ in range(3)]
    blue_slimes = [P_SLIME(2) for _ in range(3)]
    P_slimes = green_slimes + blue_slimes
    game_world.add_objects(P_slimes, 1)

    game_world.add_collision_pair('player:slime_attack', player, None)

    for slime in P_slimes:
        game_world.add_collision_pair('slime:catch', slime, None)

    game_world.add_collision_pair('player:slime', player, None)
    for slime in slimes:
        game_world.add_collision_pair('player:slime', None, slime)
        game_world.add_collision_pair('slime:attack', slime, None)

    ui = Ui()
    game_world.add_object(ui, 3)


def update():
    global player, back_1,back_2, slimes, P_slimes, MAP
    game_world.update()
    if MAP == 0:
        if player.x < 100 and player.y < 434 and player.y > 334:
            back_1.x = 0
            back_1.y = 0
            back_2.x = 0
            back_2.y = 0
            player.x = 512
            player.y = 384
            for o in slimes:
                try:
                    game_world.remove_object(o)
                except ValueError:
                    pass
            slimes.clear()

            for o in P_slimes:
                try:
                    game_world.remove_object(o)
                except ValueError:
                    pass
            P_slimes.clear()

            if farm_shop.Now_slime:
                if farm_shop.Now_slime[0] == 'P_slime_green':
                    farm_shop.new_slime = [P_SLIME(1, 8, 400, 435, 640) for _ in range(farm_shop.Now_slime[1])]
                    game_world.add_objects(farm_shop.new_slime, 1)
                elif farm_shop.Now_slime[0] == 'P_slime_blue':
                    farm_shop.new_slime = [P_SLIME(2, 8, 400, 435, 640) for _ in range(farm_shop.Now_slime[1])]
                    game_world.add_objects(farm_shop.new_slime, 1)
            MAP = 1

    elif MAP == 1:
        if player.x > 924 and player.x < 1024 and player.y < 434 and player.y > 334:
            back_1.x = 256
            back_1.y = 0
            back_2.x = 256
            back_2.y = 0
            player.x = 512
            player.y = 384
            try:
                for o in farm_shop.new_slime:
                    try:
                        game_world.remove_object(o)
                    except ValueError:
                        pass
                farm_shop.new_slime.clear()
            except (NameError, TypeError):
                farm_shop.new_slime = []
            farm_shop.new_slime.clear()

            slimes = [SLIME() for _ in range(5)]
            game_world.add_objects(slimes, 1)
            green_slimes = [P_SLIME(1) for _ in range(3)]
            blue_slimes = [P_SLIME(2) for _ in range(3)]
            P_slimes = green_slimes + blue_slimes
            game_world.add_objects(P_slimes, 1)

            for slime in P_slimes:
                game_world.add_collision_pair('slime:catch', slime, None)

            game_world.add_collision_pair('player:slime', player, None)
            for slime in slimes:
                game_world.add_collision_pair('player:slime', None, slime)
                game_world.add_collision_pair('slime:attack', slime, None)


            MAP = 0

    game_world.handle_collisions()


def draw():
    clear_canvas()
    game_world.render()
    if MAP == 0:
        draw_rectangle(0, 334, 100, 434)
    elif MAP == 1:
        draw_rectangle(924, 334, 1024, 434)
        draw_rectangle(350, 374, 400, 484)

        draw_rectangle(8, 435, 400, 640)
    update_canvas()


def finish():
    game_world.clear()
    pass


def pause():
    pass

def resume():
    pass