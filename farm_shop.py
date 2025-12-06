from pico2d import *

import game_framework
import game_world
import play_mode
from pannel import Pannel
import player
from P_slime import P_SLIME
from plort import Plort

pannel = None
select = 1
farm_slime = [[],[],[],[]]

farm_num = 0

new_slime = []

def init():
    global pannel, count

    pannel = Pannel()
    game_world.add_object(pannel,3)

    # 1. 범위 설정
    if farm_num == 1:
        left, right, bottom, top = 385, 960, 960, 1150
    elif farm_num == 2:
        left, right, bottom, top = 835, 1130, 960, 1150
    elif farm_num == 3:
        left, right, bottom, top = 341, 636, 680, 870
    elif farm_num == 4:
        left, right, bottom, top = 791, 1086, 680, 870
    else:
        left, right, bottom, top = 0, 0, 0, 0

    # 2. 현재 농장 데이터 확인 (안전장치)
    if not farm_slime[farm_num - 1]:
        return

    # 3. 목표 플로트 결정
    slime_type = farm_slime[farm_num - 1][0]
    target_plort_id = ""

    if slime_type == 'P_slime_green':
        target_plort_id = 'Green_plort'
    elif slime_type == 'P_slime_blue':
        target_plort_id = 'Blue_plort'
    elif slime_type == 'P_slime_red':
        target_plort_id = 'Red_plort'
    elif slime_type == 'P_slime_black':
        target_plort_id = 'Black_plort'

    # 4. 게임 월드 순회 및 수집
    plorts_to_remove = []

    # [핵심 수정] game_world.objects -> game_world.world 로 변경
    for layer in game_world.world:
        for o in layer:
            if isinstance(o, Plort):
                if o.item_id == target_plort_id:
                    if left <= o.x <= right and bottom <= o.y <= top:
                        plorts_to_remove.append(o)

    # 5. 데이터 저장 및 삭제 처리
    count = len(plorts_to_remove)

    if count > 0:
        target_slot = play_mode.farm_plort[farm_num - 1]

        if not target_slot:
            play_mode.farm_plort[farm_num - 1] = [target_plort_id, count]
        else:
            play_mode.farm_plort[farm_num - 1][1] += count

        # 월드에서 삭제
        for o in plorts_to_remove:
            game_world.remove_object(o)

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
            elif farm_slime[i][0] == 'P_slime_red':
                new_slime += [P_SLIME(2,f'farm_{i+1}',S_X,S_Y) for _ in range(farm_slime[i][1])]
            elif farm_slime[i][0] == 'P_slime_blue':
                new_slime += [P_SLIME(3,f'farm_{i+1}',S_X,S_Y) for _ in range(farm_slime[i][1])]
            elif farm_slime[i][0] == 'P_slime_black':
                new_slime += [P_SLIME(4,f'farm_{i+1}',S_X,S_Y) for _ in range(farm_slime[i][1])]

    if new_slime:
        game_world.add_objects(new_slime, 1)
    game_world.remove_object(pannel)

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
                            if player.inventory[i][1] < player.inventory_max:
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

            elif x > 1024 // 4 + (4 * 120) - 105 and x < 1024 // 4 + (4 * 120)-20 and y > 768 // 3 + 130 and y < 768 // 3 + 190:
                if play_mode.farm_plort[farm_num-1]:
                    item_name = play_mode.farm_plort[farm_num-1][0]
                    count = 0
                    for i in range(4):
                        slot = player.inventory[i]
                        if slot and slot[0] == item_name:
                            if player.inventory[i][1] < player.inventory_max:
                                player.inventory[i][1] += 1
                                play_mode.farm_plort[farm_num-1][1] -= 1
                                if play_mode.farm_plort[farm_num-1][1] == 0:
                                    play_mode.farm_plort[farm_num-1] = []
                            break
                        else:
                            count += 1
                    if count == 4:
                        for i in range(4):
                            slot = player.inventory[i]
                            if not slot:
                                player.inventory[i] = [item_name, 1]
                                play_mode.farm_plort[farm_num-1][1] -= 1
                                if play_mode.farm_plort[farm_num-1][1] == 0:
                                    play_mode.farm_plort[farm_num-1] = []
                                break

def pause():
    pass

def resume():
    pass