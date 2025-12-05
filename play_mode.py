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
import player as PLAYER

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

slime_respawn = [[],[],[],[]]

def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_e:
            global player
            if MAP == 'farm':
                if player.x > 680-80 and player.x < 680+30 and player.y > 1000-110 and player.y < 1000:
                    game_framework.push_mode(farm_shop)
                    farm_shop.farm_num = 1
                elif player.x > 835-30 and player.x < 835+80 and player.y > 1000-110 and player.y < 1000:
                    game_framework.push_mode(farm_shop)
                    farm_shop.farm_num = 2
                elif player.x > 636-80 and player.x < 636+30 and player .y > 720-110 and player.y < 720:
                    game_framework.push_mode(farm_shop)
                    farm_shop.farm_num = 3
                elif player.x > 791-30 and player.x < 791+80 and player.y > 720-110 and player.y < 720:
                    game_framework.push_mode(farm_shop)
                    farm_shop.farm_num = 4

            if MAP == 'spawn_1' or MAP == 'spawn_2':
                shop_x, shop_y = 1910, 950
                next_x, next_y = 2250, 850
                if (shop_x - 50 < player.x < shop_x + 50) and (shop_y - 50 < player.y < shop_y + 50):
                    game_framework.push_mode(shop)
                elif (next_x - 80 < player.x < next_x + 80) and (next_y - 80 < player.y < next_y + 80):
                    if PLAYER.gold >= 100:
                        PLAYER.gold -= 100
                        BRIDGE[0] = 1
        else:
            player.handle_event(event)


def init():
    global player, slimes, P_slimes, back_1, back_2, ui
    for i in range(5):
        BRIDGE.append(0)

    back = Back()
    game_world.add_object(back, 0)


    slimes = [SLIME('prairie',3670, 860) for _ in range(2)]
    game_world.add_objects(slimes, 1)

    green_slimes = [P_SLIME(1, 'prairie',3670, 860) for _ in range(10)]
    red_slimes = [P_SLIME(2, 'lava', 3650, 2570) for _ in range(10)]
    blue_slimes = [P_SLIME(3, 'ice', 1200, 2570) for _ in range(10)]
    black_slimes = [P_SLIME(4, 'cave', 3500, 4080) for _ in range(10)]
    P_slimes = green_slimes + red_slimes + blue_slimes + black_slimes
    game_world.add_objects(P_slimes, 1)
    for i in range(10):
        slime_respawn[0].append(-1)

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

    for i in range(10):
        if slime_respawn[0][i] != -1:
            if get_time() - slime_respawn[0][i] > 10.0:
                new_slime = P_SLIME(1)
                game_world.add_object(new_slime, 1)
                game_world.add_collision_pair('slime:catch', new_slime, None)
                P_slimes.append(new_slime)
                slime_respawn[0][i] = -1


    game_world.handle_collisions()


def draw():
    clear_canvas()
    game_world.render()
    if MAP == 'spawn_1' or MAP == 'spawn_2':
        sx, sy = 1910 - camera_x, 950 - camera_y
        draw_rectangle(sx - 50, sy - 50, sx + 50, sy + 50)

        sx, sy = 1910 - camera_x, 1050 - camera_y
        draw_rectangle(sx - 80, sy - 80, sx + 80, sy + 80)

        sx, sy = 2250 - camera_x, 850 - camera_y
        draw_rectangle(sx - 80, sy - 80, sx + 80, sy + 80)

    elif MAP == 'farm':
        sx, sy = 680 - camera_x, 1000 - camera_y
        draw_rectangle(sx - 80, sy - 110, sx + 30, sy)
        sx, sy = 835 - camera_x, 1000 - camera_y
        draw_rectangle(sx - 30, sy - 110, sx + 80, sy)
        sx, sy = 636 - camera_x, 720 - camera_y
        draw_rectangle(sx - 80, sy - 110, sx + 30, sy)
        sx, sy = 791 - camera_x, 720 - camera_y
        draw_rectangle(sx - 30, sy - 110, sx + 80, sy)

    update_canvas()


def finish():
    game_world.clear()
    pass


def pause():
    pass

def resume():
    pass