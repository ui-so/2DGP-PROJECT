from pico2d import *

import game_framework
import game_world
import play_mode
from shop_pannel import ShopPannel
import player
from P_slime import P_SLIME

shoppannel = None
select = 1
Now_slime = []

new_slime = None

Page = 0

shop_count = [0,0,0]
shop_gold = [100, 100, 1000]

def init():
    global shoppannel, Page

    shoppannel = ShopPannel(Page)
    game_world.add_object(shoppannel,3)
    pass

def finish():
    game_world.remove_object(shoppannel)

def update():
    pass

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()


def handle_events():
    global select, player
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                player.right_pressed = False
                player.left_pressed = False
                player.up_pressed = False
                player.down_pressed = False
                player.dir_x = 0
                player.dir_y = 0
                game_framework.pop_mode()
            elif event.key == SDLK_1:
                select = 1
            elif event.key == SDLK_2:
                select = 2
            elif event.key == SDLK_3:
                select = 3
            elif event.key == SDLK_4:
                select = 4
        elif event.type == SDL_MOUSEBUTTONDOWN:
            global Now_slime, Page, shoppannel
            x, y = event.x, 768 - event.y
            if Page == 0:
                if x > 1024 // 4 + (4 * 120) + 70 and x < 1024 // 4 + (4 * 120) + 130 and y > 768 // 3 - 60 and y < 768 // 3 - 10:
                    selected_slot = player.inventory[select - 1]
                    if selected_slot and len(selected_slot) == 2:
                        if selected_slot[1] > 0:
                            selected_slot[1] -= 1
                            if selected_slot[1] == 0:
                                player.inventory[select - 1] = []


                elif x > 1024 // 4 + (4 * 120) - 80 and x < 1024 // 4 + (4 * 120) + 5 and y > 768 // 3 - 60 and y < 768 // 3 - 10:
                    selected_slot = player.inventory[select - 1]
                    if selected_slot and len(selected_slot) == 2:
                        if selected_slot[1] > 0:
                            item_name = selected_slot[0]
                            if item_name == 'Green_plort':
                                player.gold += 10
                                player.inventory[select-1][1] -= 1
                                if player.inventory[select-1][1] <= 0:
                                    player.inventory[select-1] = []
                            if item_name == 'Blue_plort':
                                player.gold += 50
                                player.inventory[select-1][1] -= 1
                                if player.inventory[select-1][1] <= 0:
                                    player.inventory[select-1] = []
                            if item_name == 'Red_plort':
                                player.gold += 25
                                player.inventory[select-1][1] -= 1
                                if player.inventory[select-1][1] <= 0:
                                    player.inventory[select-1] = []
                            if item_name == 'Black_plort':
                                player.gold += 75
                                player.inventory[select-1][1] -= 1
                                if player.inventory[select-1][1] <= 0:
                                    player.inventory[select-1] = []
                elif x > 1024 // 2 + 300 and y < 768 // 2 - 220 and x < 1024 // 2 + 350 and y > 768 // 2 - 270:
                    print('눌림')
                    Page = 1
                    game_world.remove_object(shoppannel)
                    shoppannel = ShopPannel(Page)
                    game_world.add_object(shoppannel, 3)
            elif Page == 1:
                if x > 1024 // 2 - 350 and y < 768 // 2 - 220 and x < 1024 // 2 - 300 and y > 768 // 2 - 270:
                    Page = 0
                    game_world.remove_object(shoppannel)
                    shoppannel = ShopPannel(Page)
                    game_world.add_object(shoppannel, 3)
                elif x > 1024 // 2 - 315 and y < 768 // 2 - 50 and x < 1024 // 2 - 145 and y > 768 // 2 - 120:
                    if shop_count[0] < 10 and player.gold >= shop_gold[0]:
                        shop_count[0] += 1
                        player.gold -= shop_gold[0]
                        shop_gold[0] += 200
                        player.hp_max += 10
                elif x > 1024 // 2 - 80 and y < 768 // 2 - 50 and x < 1024 // 2 + 90 and y > 768 // 2 - 120:
                    if shop_count[1] < 10 and player.gold >= shop_gold[1]:
                        shop_count[1] += 1
                        player.gold -= shop_gold[1]
                        shop_gold[1] += 200
                        player.mp_max += 10
                elif x > 1024 // 2 + 155 and y < 768 // 2 - 50 and x < 1024 // 2 + 325 and y > 768 // 2 - 120:
                    if shop_count[2] < 5 and player.gold >= shop_gold[2]:
                        shop_count[2] += 1
                        player.gold -= shop_gold[2]
                        shop_gold[2] += 500
                        player.inventory_max += 5

def pause():
    pass

def resume():
    pass