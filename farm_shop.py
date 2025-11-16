from pico2d import *

import game_framework
import game_world
import play_mode
from pannel import Pannel
import player

pannel = None
select = 1
Now_slime = []

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
                        if not Now_slime:
                            Now_slime = [item_name, 1]
                            selected_slot[1] -= 1
                        elif Now_slime[0] == item_name:
                            Now_slime[1] += 1
                            selected_slot[1] -= 1

                        if selected_slot[1] == 0:
                            player.inventory[select - 1] = []

            elif x > 1024 // 4 + (4 * 120) - 80 and x < 1024 // 4 + (4 * 120) + 5 and y > 768 // 3 - 105 and y < 768 // 3 - 50:
                if Now_slime:
                    item_name = Now_slime[0]
                    item_count = Now_slime[1]
                    for i in range(4):
                        slot = player.inventory[i]
                        if not slot:
                            player.inventory[i] = [item_name, item_count]
                            Now_slime = []
                            break
                        elif slot[0] == item_name:
                            slot[1] += item_count
                            Now_slime = []
                            break


def pause():
    pass

def resume():
    pass