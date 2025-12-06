import end_mode
import game_framework
from pico2d import *

from bridge import Bridge
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
P_slime_respawn = [[],[],[],[]]
farm_plort = [[],[],[],[]]

KEY = [0,0,0,0]

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
                shop_x, shop_y = 2000, 950
                next_x, next_y = 2250, 850
                home_x , home_y = 1830, 950
                if (shop_x - 50 < player.x < shop_x + 50) and (shop_y - 50 < player.y < shop_y + 50):
                    game_framework.push_mode(shop)
                elif BRIDGE[0] == 0 and (next_x - 80 < player.x < next_x + 80) and (next_y - 80 < player.y < next_y + 80):
                    if PLAYER.gold >= 100:
                        PLAYER.gold -= 100
                        BRIDGE[0] = 1
                        bridge = Bridge(1)
                        game_world.add_object(bridge,0)
                elif (home_x - 50 < player.x < home_x + 50) and (home_y - 50 < player.y < home_y + 50):
                    player.hp = PLAYER.hp_max
                    player.mp = PLAYER.mp_max

            elif MAP == 'prairie_1' or MAP == 'prairie_2':
                next_x, next_y = 3650, 1300
                if BRIDGE[1] == 0 and (next_x - 100 < player.x < next_x + 100) and (next_y - 100 < player.y < next_y + 100):
                    if PLAYER.gold >= 500:
                        PLAYER.gold -= 500
                        BRIDGE[1] = 1
                        bridge = Bridge(2)
                        game_world.add_object(bridge,0)

            elif MAP == 'lava_1' or MAP == 'lava_2' or MAP == 'lava_3':
                next_x1, next_y1 = 2750, 2500
                next_x2, next_y2 = 3560, 3000
                if BRIDGE[2] == 0 and (next_x1 - 100 < player.x < next_x1 + 100) and (next_y1 - 100 < player.y < next_y1 + 100):
                    if PLAYER.gold >= 700:
                        PLAYER.gold -= 700
                        BRIDGE[2] = 1
                        bridge = Bridge(3)
                        game_world.add_object(bridge,0)
                elif BRIDGE[3] == 0 and (next_x2 - 100 < player.x < next_x2 + 100) and (next_y2 - 100 < player.y < next_y2 + 100):
                    if PLAYER.gold >= 1000:
                        PLAYER.gold -= 700
                        BRIDGE[3] = 1
                        bridge = Bridge(4)
                        game_world.add_object(bridge,0)

            elif MAP == 'cave_1' or MAP == 'cave_2':
                next_x, next_y = 2550, 4000
                if BRIDGE[4] == 0 and (next_x - 100 < player.x < next_x + 100) and (next_y - 100 < player.y < next_y + 100):
                    if PLAYER.gold >= 1500:
                        PLAYER.gold -= 1500
                        BRIDGE[4] = 1
                        bridge = Bridge(5)
                        game_world.add_object(bridge,0)

            elif MAP == 'end_1':
                home_x , home_y = 1050, 4000
                if (home_x - 50 < player.x < home_x + 50) and (home_y - 50 < player.y < home_y + 50):
                    if KEY[0] == 1 and KEY[1] == 1 and KEY[2] == 1 and KEY[3] == 1:
                        game_framework.push_mode(end_mode)
        else:
            player.handle_event(event)


def init():
    global player, slimes, P_slimes, ui, font, bgm

    font = load_font('ENCR10B.TTF', 16)

    bgm = load_music('play_bgm.mp3')
    bgm.set_volume(32)
    bgm.repeat_play()

    for i in range(5):
        BRIDGE.append(0)

    back_1 = Back(1)
    game_world.add_object(back_1, 0)
    back_2 = Back(2)
    game_world.add_object(back_2, 2)
    back_3 = Back(3)
    game_world.add_object(back_3, 3)


    G_slimes = [SLIME('prairie',3670, 860) for _ in range(10)]
    R_slimes = [SLIME('lava', 3650, 2570) for _ in range(10)]
    B_slimes = [SLIME('ice', 1200, 2570) for _ in range(10)]
    Bl_slimes = [SLIME('cave', 3500, 4080) for _ in range(10)]
    slimes = G_slimes + R_slimes + B_slimes + Bl_slimes
    game_world.add_objects(slimes, 1)

    green_slimes = [P_SLIME(1, 'prairie',3670, 860) for _ in range(10)]
    red_slimes = [P_SLIME(2, 'lava', 3650, 2570) for _ in range(10)]
    blue_slimes = [P_SLIME(3, 'ice', 1200, 2570) for _ in range(10)]
    black_slimes = [P_SLIME(4, 'cave', 3500, 4080) for _ in range(10)]
    P_slimes = green_slimes + red_slimes + blue_slimes + black_slimes
    game_world.add_objects(P_slimes, 1)

    for i in range(4):
        for _ in range(10):
            slime_respawn[i].append(-1)
            P_slime_respawn[i].append(-1)


    player = Player()
    game_world.add_object(player, 2)

    game_world.add_collision_pair('player:slime_attack', player, None)
    game_world.add_collision_pair('player:key', player, None)

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

    for i in range(4):
        for j in range(10):
            if P_slime_respawn[i][j] != -1:
                if get_time() - P_slime_respawn[i][j] > 10.0:
                    new_slime = P_SLIME(i+1, ISLAND, 2000, 2000)
                    game_world.add_object(new_slime, 1)
                    game_world.add_collision_pair('slime:catch', new_slime, None)
                    P_slimes.append(new_slime)
                    P_slime_respawn[i][j] = -1
            if slime_respawn[i][j] != -1:
                if get_time() - slime_respawn[i][j] > 10.0:
                    new_slime = SLIME(ISLAND, 2000, 2000)
                    game_world.add_object(new_slime, 1)
                    game_world.add_collision_pair('slime:attack', new_slime, None)
                    game_world.add_collision_pair('player:slime', None, new_slime)
                    slimes.append(new_slime)
                    slime_respawn[i][j] = -1


    game_world.handle_collisions()


def draw():
    clear_canvas()
    game_world.render()

    for i in range(5):
        if BRIDGE[i] == 0:
            if i == 0:
                sx, sy = 2250 - camera_x + 10, 850 - camera_y
                need_gold = 100
                font.draw(sx, sy, f'{PLAYER.gold} / {need_gold} ', (255, 255, 255))
            elif i == 1:
                sx, sy = 3600 - camera_x + 10, 1400 - camera_y
                need_gold = 500
                font.draw(sx, sy, f'{PLAYER.gold} / {need_gold} ', (255, 255, 255))
            elif i == 2:
                sx, sy = 2700 - camera_x + 10, 2550 - camera_y
                need_gold = 700
                font.draw(sx, sy, f'{PLAYER.gold} / {need_gold} ', (255, 255, 255))
            elif i == 3:
                sx, sy = 3490 - camera_x + 10, 3050 - camera_y
                need_gold = 1000
                font.draw(sx, sy, f'{PLAYER.gold} / {need_gold} ', (255, 255, 255))
            elif i == 4:
                sx, sy = 2425 - camera_x + 10, 4025 - camera_y
                need_gold = 1500
                font.draw(sx, sy, f'{PLAYER.gold} / {need_gold} ', (255, 255, 255))


    if MAP == 'spawn_1' or MAP == 'spawn_2':
        sx, sy = 1830 - camera_x, 950 - camera_y
        draw_rectangle(sx - 50, sy - 50, sx + 50, sy + 50)

        sx, sy = 2000 - camera_x, 950 - camera_y
        draw_rectangle(sx - 50, sy - 50, sx + 50, sy + 50)

        sx, sy = 2250 - camera_x, 850 - camera_y
        draw_rectangle(sx - 80, sy - 80, sx + 80, sy + 80)

    elif MAP == 'prairie_1' or MAP == 'prairie_2':
        sx, sy = 3650 - camera_x, 1300 - camera_y
        draw_rectangle(sx - 100, sy - 100, sx + 100, sy + 100)

    elif MAP == 'lava_1' or MAP == 'lava_2' or MAP == 'lava_3':
        sx, sy = 2750 - camera_x, 2500 - camera_y
        draw_rectangle(sx - 100, sy - 100, sx + 100, sy + 100)
        sx, sy = 3560 - camera_x, 3000 - camera_y
        draw_rectangle(sx - 100, sy - 100, sx + 100, sy + 100)

    elif MAP == 'cave_1' or MAP == 'cave_2':
        sx, sy = 2550 - camera_x, 4000 - camera_y
        draw_rectangle(sx - 100, sy - 100, sx + 100, sy + 100)

    elif MAP == 'farm':
        sx, sy = 680 - camera_x, 1000 - camera_y
        draw_rectangle(sx - 80, sy - 110, sx + 30, sy)
        sx, sy = 835 - camera_x, 1000 - camera_y
        draw_rectangle(sx - 30, sy - 110, sx + 80, sy)
        sx, sy = 636 - camera_x, 720 - camera_y
        draw_rectangle(sx - 80, sy - 110, sx + 30, sy)
        sx, sy = 791 - camera_x, 720 - camera_y
        draw_rectangle(sx - 30, sy - 110, sx + 80, sy)

    elif MAP == 'end_1':
        sx, sy = 1050 - camera_x, 4000 - camera_y
        draw_rectangle(sx - 50, sy - 50, sx + 50, sy + 50)

    update_canvas()


def finish():
    game_world.clear()
    global bgm
    del bgm
    pass


def pause():
    pass

def resume():
    pass