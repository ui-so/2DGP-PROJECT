import random

import math

import catch
import game_framework
import game_world
import play_mode

from pico2d import *

from plort import Plort

# Slime Run Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 5.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# Slime Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 7.0


class P_SLIME:
    green_image = None
    red_image = None
    blue_image = None
    black_image = None

    def load_images(self):
        if P_SLIME.green_image is None:
            P_SLIME.green_image = load_image('Green_Slime_Run.png')
        if P_SLIME.red_image is None:
            P_SLIME.red_image = load_image('Red_Slime_Run.png')
        if P_SLIME.blue_image is None:
            P_SLIME.blue_image = load_image('Blue_Slime_Run.png')
        if P_SLIME.black_image is None:
            P_SLIME.black_image = load_image('Black_Slime_Run.png')

    def __init__(self, num=1, map='prairie', x=3670, y=860):
        self.num = num
        self.load_images()
        if self.num == 1:
            self.image = P_SLIME.green_image
            self.item_id = 'P_slime_green'  # 인벤토리용
        elif self.num == 2:
            self.image = P_SLIME.red_image
            self.item_id = 'P_slime_red'  # 인벤토리용
        elif self.num == 3:
            self.image = P_SLIME.blue_image
            self.item_id = 'P_slime_blue'  # 인벤토리용
        elif self.num == 4:
            self.image = P_SLIME.black_image
            self.item_id = 'P_slime_black'
        else:
            self.image = None  # 예외 처리

        self.frame = random.randint(0, int(FRAMES_PER_ACTION) - 1)
        self.dir_x = random.choice([-1, 1])
        self.dir_y = random.choice([-1, 1])
        self.size = 600
        self.draw_w = 100
        self.draw_h = 100
        self.map = map

        self.x = random.randint(x - self.size // 2, x + self.size // 2)
        self.y = random.randint(y - self.size // 2, y + self.size // 2)

        self.change_timer = random.uniform(1.0, 3.0)
        self.plort_timer = get_time()

    def get_bb(self):
        return self.x - play_mode.camera_x - 30, self.y - play_mode.camera_y - 50, self.x - play_mode.camera_x + 30, self.y - play_mode.camera_y - 10

    def update(self):
        import farm_shop
        self.change_timer -= game_framework.frame_time

        if self.map == 'farm_1' or self.map == 'farm_2' or self.map == 'farm_3' or self.map == 'farm_4' or self.map == play_mode.ISLAND:
            if get_time() - self.plort_timer > 10.0:
                self.plort_timer = get_time()
                plort = Plort(self.num, self.x, self.y-10)
                game_world.add_object(plort, 1)
                game_world.add_collision_pair('catch:plort', None, plort)

        if self.change_timer < 0:
            self.dir_x = random.choice([-1, 1])
            self.dir_y = random.choice([-1, 1])
            self.change_timer = random.uniform(1.0, 3.0)

        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        self.x += RUN_SPEED_PPS * self.dir_x * game_framework.frame_time
        self.y += RUN_SPEED_PPS * self.dir_y * game_framework.frame_time

        if self.map == 'farm_1':
            self.constrain_rect(385,960,680,1150)
        elif self.map == 'farm_2':
            self.constrain_rect(835,960,1130,1150)
        elif self.map == 'farm_3':
            self.constrain_rect(341,680,636,870)
        elif self.map == 'farm_4':
            self.constrain_rect(791,680,1086,870)

        if self.map == 'prairie':
            self.constrain_to_ellipse(3670, 860, 870, 500)
        elif self.map == 'lava':
            self.constrain_to_ellipse(3650, 2570, 880, 480)
        elif self.map == 'ice':
            self.constrain_to_ellipse(1200, 2500, 880, 500)
        elif self.map == 'cave':
            self.constrain_to_ellipse(3500, 4080, 980, 480)


    def draw(self):
        if self.image is None:
            return

        sx = self.x - play_mode.camera_x
        sy = self.y - play_mode.camera_y

        frame_idx = int(self.frame) * 128
        if self.dir_x < 0:
            self.image.clip_composite_draw(frame_idx, 0, 128, 128, 0, 'h', sx, sy, self.draw_w, self.draw_h)
        else:
            self.image.clip_draw(frame_idx, 0, 128, 128, sx, sy, self.draw_w, self.draw_h)


    def constrain_to_ellipse(self, cx, cy, rx, ry):
        dx = self.x - cx
        dy = self.y - cy

        if rx == 0 or ry == 0: return

        normalized_dist = (dx ** 2) / (rx ** 2) + (dy ** 2) / (ry ** 2)

        if normalized_dist > 1.0:
            scale = 1 / math.sqrt(normalized_dist)

            self.x = cx + dx * scale
            self.y = cy + dy * scale

    def constrain_rect(self, left, bottom, right, top):
        half_w = 30

        if self.x < left + half_w:
            self.x = left + half_w
            self.dir_x *= -1
        elif self.x > right - half_w:
            self.x = right - half_w
            self.dir_x *= -1

        if self.y < bottom + 50:
            self.y = bottom + 50
            self.dir_y *= -1
        elif self.y > top:
            self.y = top
            self.dir_y *= -1

    def handle_event(self, event):
        pass

    def handle_collision(self, group, other):
        if group == 'slime:catch':
            print("Slime catch!")
            if catch.catch == 1:
                game_world.remove_object(self)
                for i in range(10):
                    if play_mode.P_slime_respawn[self.num-1][i] == -1:
                        play_mode.P_slime_respawn[self.num-1][i] = get_time()
                        break
                catch.catch = 0