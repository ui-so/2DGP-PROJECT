import game_framework
from pico2d import *

from ui import Ui
from background import Back
from player import Player
from slime import SLIME
from P_slime import P_SLIME
import game_world
import farm_shop
import shop

BG_W = 1350
BG_H = 1350

MAP_WIDTH = BG_W * 4.0
MAP_HEIGHT = BG_H * 4.0

camera_x = 0
camera_y = 0

back = None
player = None
slimes = None
P_slimes = None

MAP = 'spawn_1'
ISLAND = 'spawn'

BRIDGE = []

def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_e:
            global player
            if MAP == 1:
                if player.x > 350 and player.x < 400 and player.y > 374 and player.y < 484:
                    game_framework.push_mode(farm_shop)
            if MAP == 'spawn_1' or MAP == 'spawn_2':
                shop_x, shop_y = 1910, 950
                if (shop_x - 50 < player.x < shop_x + 50) and (shop_y - 50 < player.y < shop_y + 50):
                    game_framework.push_mode(shop)
        else:
            player.handle_event(event)


def init():
    global player, slimes, P_slimes, back_1, back_2, ui

    back = Back()
    game_world.add_object(back, 0)


    slimes = [SLIME('prairie',3670, 860) for _ in range(2)]
    game_world.add_objects(slimes, 1)

    green_slimes = [P_SLIME(1) for _ in range(2)]
    blue_slimes = [P_SLIME(2) for _ in range(2)]
    P_slimes = green_slimes + blue_slimes
    game_world.add_objects(P_slimes, 1)

    player = Player()
    game_world.add_object(player, 1)

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
    global camera_x, camera_y, player, back_1,back_2, slimes, P_slimes, MAP
    camera_x = player.x - 1024 // 2
    camera_y = player.y - 768 // 2

    camera_x = max(0, min(camera_x, MAP_WIDTH - 1024))
    camera_y = max(0, min(camera_y, MAP_HEIGHT - 768))

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
    if MAP == 'spawn_1' or MAP == 'spawn_2':
        sx, sy = 1910 - camera_x, 950 - camera_y
        draw_rectangle(sx - 50, sy - 50, sx + 50, sy + 50)

        sx, sy = 1910 - camera_x, 1050 - camera_y
        draw_rectangle(sx - 80, sy - 80, sx + 80, sy + 80)
    update_canvas()


def finish():
    game_world.clear()
    pass


def pause():
    pass

def resume():
    pass