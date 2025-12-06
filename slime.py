import random
import game_framework
import game_world
import play_mode
from slime_attack import Slime_Attack
import player
from key import Key

from pico2d import *
import math

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

class SLIME:
    green_image = None
    red_image = None
    blue_image = None
    black_image = None

    def load_images(self):
        if SLIME.green_image is None:
            SLIME.green_image = load_image('Green_Monster_Run.png')
        if SLIME.red_image is None:
            SLIME.red_image = load_image('Red_Monster_Run.png')
        if SLIME.blue_image is None:
            SLIME.blue_image = load_image('Blue_Monster_Run.png')
        if SLIME.black_image is None:
            SLIME.black_image = load_image('Black_Monster_Run.png')

    def __init__(self, map='prairie', x=3670, y=860):
        self.load_images()
        if map == 'prairie':
            self.image = SLIME.green_image
        elif map == 'lava':
            self.image = SLIME.red_image
        elif map == 'ice':
            self.image = SLIME.blue_image
        elif map == 'cave':
            self.image = SLIME.black_image
        else:
            self.image = None

        self.frame = random.randint(0, int(FRAMES_PER_ACTION) - 1)
        self.dir_x = random.choice([-1, 1])
        self.dir_y = random.choice([-1, 1])
        self.size = 1000
        self.draw_w = 150
        self.draw_h = 150
        self.x = random.randint(x - self.size // 2, x + self.size // 2)
        self.y = random.randint(y - self.size // 2, y + self.size // 2)
        self.map = map

        self.change_timer = random.uniform(1.0, 3.0)

        self.attack_time = 0.0

    def get_bb(self):
        return self.x - play_mode.camera_x - 20, self.y- play_mode.camera_y - 80, self.x - play_mode.camera_x + 40, self.y - play_mode.camera_y-20

    def update(self):
        if self.map == play_mode.ISLAND:
            self.change_timer -= game_framework.frame_time

            if self.change_timer < 0:
                self.dir_x = random.choice([-1, 1])
                self.dir_y = random.choice([-1, 1])
                self.change_timer = random.uniform(1.0, 3.0)

            self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
            self.x += RUN_SPEED_PPS * self.dir_x * game_framework.frame_time
            self.y += RUN_SPEED_PPS * self.dir_y * game_framework.frame_time

            if self.map == 'prairie':
                self.constrain_to_ellipse(3670, 860, 870, 500)
            elif self.map == 'lava':
                self.constrain_to_ellipse(3650, 2570, 880, 480)
            elif self.map == 'ice':
                self.constrain_to_ellipse(1200, 2500, 880, 500)
            elif self.map == 'cave':
                self.constrain_to_ellipse(3500, 4080, 980, 480)

            if self.x + 110 >= play_mode.player.x - 50 and self.x - 100 <= play_mode.player.x + 40 and self.y + 50 >= play_mode.player.y - 50 and self.y - 140 <= play_mode.player.y + 40:
                self.attack()

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
        draw_rectangle(*self.get_bb())
        draw_rectangle(sx - 100, sy - 140, sx + 110, sy+50)

    def attack(self):
        if get_time() - self.attack_time > 3.0:
            self.attack_time = get_time()
            attack = Slime_Attack(self.map, self.x, self.y-25, self.dir_x, play_mode.player.x, play_mode.player.y)
            game_world.add_object(attack, 1)
            game_world.add_collision_pair('player:slime_attack', None, attack)

    def constrain_to_ellipse(self, cx, cy, rx, ry):
        dx = self.x - cx
        dy = self.y - cy

        if rx == 0 or ry == 0: return

        normalized_dist = (dx ** 2) / (rx ** 2) + (dy ** 2) / (ry ** 2)

        if normalized_dist > 1.0:
            scale = 1 / math.sqrt(normalized_dist)

            self.x = cx + dx * scale
            self.y = cy + dy * scale

    def handle_event(self, event):
        pass

    def handle_collision(self, group, other):
        if group == 'slime:attack':
            print("Slime Hit!")
            game_world.remove_object(self)
            if self.map == 'prairie':
                player.gold += 10
                key_num = 1
            elif self.map == 'lava':
                player.gold += 25
                key_num = 2
            elif self.map == 'ice':
                player.gold += 50
                key_num = 3
            elif self.map == 'cave':
                player.gold += 100
                key_num = 4

            if random.randint(1, 100) <= 20:
                key = Key(key_num, self.x, self.y)
                game_world.add_object(key, 1)
                game_world.add_collision_pair('player:key', None, key)


        pass
