from pico2d import *

import P_slime
import game_world
import game_framework
import player
import play_mode

PIXEL_PER_METER = (1.0 / 0.003)  # 1pixel = 3cm, 1m = 33.33 pixel

catch = 0

class Catch:
    image = None

    def __init__(self, x = 400, y = 300, dir = 1):
        self.x, self.y = x, y
        self.dir = dir
        self.size = 50
        self.time = get_time()

    def draw(self):
        draw_rectangle(*self.get_bb())

    def update(self):
        if get_time() - self.time > 0.2:
            game_world.remove_object(self)
        pass

    def get_bb(self):
        if self.dir == 1:
            return self.x, self.y - self.size//2, self.x + self.size, self.y + self.size//2
        else:
            return self.x - self.size*3, self.y - self.size//2, self.x- self.size*2, self.y + self.size//2

    def handle_collision(self, group, other):
        global catch
        if group == 'slime:catch':
            if play_mode.ISLAND != 'farm' and catch != 1:
                S = other.item_id
                count = 0
                for i in range(4):
                    slot = player.inventory[i]
                    if slot and slot[0] == S:
                        if player.inventory[i][1] < player.inventory_max and catch != 1:
                            player.inventory[i][1] += 1
                            catch = 1
                            game_world.remove_object(other)
                            break
                    else:
                        count += 1
                if count == 4:
                    for i in range(4):
                        if not player.inventory[i] and catch != 1:
                            player.inventory[i] = [S, 1]
                            catch = 1
                            game_world.remove_object(other)
                            break

        elif group == 'catch:plort':
            S = other.item_id
            count = 0
            for i in range(4):
                if player.inventory[i] == S and player.inventory[i][1] < player.inventory_max:
                    player.inventory[i][1] += 1
                    break
                else:
                    count += 1
            if count == 4:
                for i in range(4):
                    if not player.inventory[i]:
                        player.inventory[i] = [S, 1]
                        break
                    elif player.inventory[i][0] == S:
                        player.inventory[i][1] += 1
                        break