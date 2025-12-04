from pico2d import *

import game_framework
import game_world
import play_mode
from pannel import Pannel
import player
from P_slime import P_SLIME

pannel = None
select = 1
farm_slime = [[],[],[],[]]

farm_num = 0

new_slime = []

def init():
    global pannel

    pannel = Pannel()
    game_world.add_object(pannel,3)
    pass

def finish():
    global pannel, farm_slime, new_slime

    if new_slime:
        for o in new_slime:
            game_world.remove_object(o)

    new_slime = []
    for i in range(4):
        if farm_slime[i]:
            if i == 0:
                S_X, S_Y = 400, 1000
            elif i == 1:
                S_X, S_Y = 912, 1000
            elif i == 2:
                S_X, S_Y = 410, 730
            elif i == 3:
                S_X, S_Y = 830, 730

            if farm_slime[i][0] == 'P_slime_green':
                new_slime += [P_SLIME(1,f'farm_{i+1}',S_X,S_Y) for _ in range(farm_slime[i][1])]
            elif farm_slime[i][0] == 'P_slime_blue':
                new_slime += [P_SLIME(2,f'farm_{i+1}',S_X,S_Y) for _ in range(farm_slime[i][1])]

    if new_slime:
        game_world.add_objects(new_slime, 1)
    game_world.remove_object(pannel)

def update():
    pass

def draw():
    clear_canvas()
    game_world.render()
    for i in range(1, 5):
        if i == select:
            draw_rectangle(1024 // 4 + ((i-1)*120) - 75, 768 // 3-75, 1024 // 4 + ((i-1)*120), 768 // 3)

    draw_rectangle(1024 // 4 + (4 * 120) - 80, 768 // 3 - 30, 1024 // 4 + (4 * 120)+5, 768 // 3+30)
    draw_rectangle(1024 // 4 + (4 * 120) - 80, 768 // 3 - 105, 1024 // 4 + (4 * 120) + 5, 768 // 3 - 50)
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
            global Now_slime
            x, y = event.x, 768 - event.y
            if x > 1024 // 4 + (4 * 120) - 80 and x < 1024 // 4 + (4 * 120) + 5 and y > 768 // 3 - 30 and y < 768 // 3 + 30:
                selected_slot = player.inventory[select - 1]
                if selected_slot and len(selected_slot) == 2:
                    if selected_slot[1] > 0:
                        item_name = selected_slot[0]
                        if not farm_slime[farm_num-1]:
                            farm_slime[farm_num-1] = [item_name, 1]
                            selected_slot[1] -= 1
                        elif farm_slime[farm_num-1][0] == item_name:
                            farm_slime[farm_num-1][1] += 1
                            selected_slot[1] -= 1

                        if selected_slot[1] == 0:
                            player.inventory[select - 1] = []

            elif x > 1024 // 4 + (4 * 120) - 80 and x < 1024 // 4 + (4 * 120) + 5 and y > 768 // 3 - 105 and y < 768 // 3 - 50:
                if farm_slime[farm_num-1]:
                    item_name = farm_slime[farm_num-1][0]
                    count = 0
                    for i in range(4):
                        slot = player.inventory[i]
                        if slot and slot[0] == item_name:
                            player.inventory[i][1] += 1
                            farm_slime[farm_num-1][1] -= 1
                            if farm_slime[farm_num-1][1] == 0:
                                farm_slime[farm_num-1] = []
                            break
                        else:
                            count += 1
                    if count == 4:
                        for i in range(4):
                            slot = player.inventory[i]
                            if not slot:
                                player.inventory[i] = [item_name, 1]
                                farm_slime[farm_num-1][1] -= 1
                                if farm_slime[farm_num-1][1] == 0:
                                    farm_slime[farm_num-1] = []
                                break


def pause():
    pass

def resume():
    pass