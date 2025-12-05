import random
import game_framework
import game_world
import play_mode
from slime_attack import Slime_Attack
import player

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
    image = None

    def load_images(self):
        if SLIME.image is None:
            SLIME.image = load_image('Red_Slime_Run.png')

    def __init__(self, map='prairie', x=3670, y=860):
        self.load_images()
        self.frame = random.randint(0, int(FRAMES_PER_ACTION) - 1)
        self.dir_x = random.choice([-1, 1])
        self.dir_y = random.choice([-1, 1])
        self.size = 200
        self.draw_w = 100
        self.draw_h = 100
        self.x = random.randint(x - self.size // 2, x + self.size // 2)
        self.y = random.randint(y - self.size // 2, y + self.size // 2)
        self.map = map

        self.change_timer = random.uniform(1.0, 3.0)

        self.attack_time = 0.0

    def get_bb(self):
        return self.x - play_mode.camera_x - 30, self.y- play_mode.camera_y - 50, self.x - play_mode.camera_x + 30, self.y - play_mode.camera_y - 10

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
                self.constrain_to_ellipse(3670, 860, 890, 520)

            if self.x + 100 >= play_mode.player.x - 50 and self.x - 100 <= play_mode.player.x + 40 and self.y + 70 >= play_mode.player.y - 50 and self.y - 120 <= play_mode.player.y + 40:
                self.attack()

    def draw(self):
        if SLIME.image is None:
            return

        sx = self.x - play_mode.camera_x
        sy = self.y - play_mode.camera_y

        frame_idx = int(self.frame) * 128
        if self.dir_x < 0:
            SLIME.image.clip_composite_draw(frame_idx, 0, 128, 128, 0, 'h', sx, sy, self.draw_w, self.draw_h)
        else:
            SLIME.image.clip_draw(frame_idx, 0, 128, 128, sx, sy, self.draw_w, self.draw_h)
        draw_rectangle(*self.get_bb())
        draw_rectangle(sx - 100, sy - 120, sx + 100, sy+70)

    def attack(self):
        if get_time() - self.attack_time > 3.0:
            self.attack_time = get_time()
            attack = Slime_Attack(self.x, self.y-25, self.dir_x, play_mode.player.x, play_mode.player.y)
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
            player.gold += 10
        pass
