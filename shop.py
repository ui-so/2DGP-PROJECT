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
    if Page == 0:
        for i in range(1, 5):
            if i == select:
                draw_rectangle(1024 // 4 + ((i-1)*120) - 75, 768 // 3-75, 1024 // 4 + ((i-1)*120), 768 // 3)

        draw_rectangle(1024 // 4 + (4 * 120) - 80, 768 // 3 - 30, 1024 // 4 + (4 * 120)+5, 768 // 3+30)
        draw_rectangle(1024 // 4 + (4 * 120) - 80, 768 // 3 - 105, 1024 // 4 + (4 * 120) + 5, 768 // 3 - 50)

    elif Page == 1:
        draw_rectangle(1024 // 2 - 315, 768 // 2 - 50 , 1024 // 2 - 145 , 768 // 2 - 120)
        draw_rectangle(1024 // 2 - 80, 768 // 2 - 50 , 1024 // 2 + 90 , 768 // 2 - 120)
        draw_rectangle(1024 // 2 + 155, 768 // 2 - 50 , 1024 // 2 + 325 , 768 // 2 - 120)

    draw_rectangle(1024 // 2 + 300, 768 // 2 - 220, 1024 // 2 + 350 , 768 // 2 - 270)
    draw_rectangle(1024 // 2 - 300, 768 // 2 - 220, 1024 // 2 - 350, 768 // 2 - 270)

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
                if x > 1024 // 4 + (4 * 120) - 80 and x < 1024 // 4 + (4 * 120) + 5 and y > 768 // 3 - 30 and y < 768 // 3 + 30:
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
                                player.gold += 20
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
                    player.hp_max += 10
                elif x > 1024 // 2 - 80 and y < 768 // 2 - 50 and x < 1024 // 2 + 90 and y > 768 // 2 - 120:
                    player.mp_max += 10
                elif x > 1024 // 2 + 155 and y < 768 // 2 - 50 and x < 1024 // 2 + 325 and y > 768 // 2 - 120:
                    player.inventory_max += 5

def pause():
    pass

def resume():
    pass