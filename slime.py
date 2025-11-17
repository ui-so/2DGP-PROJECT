import random
import game_framework
import game_world
import play_mode
from slime_attack import Slime_Attack

from pico2d import *

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

    def __init__(self):
        self.load_images()
        self.frame = random.randint(0, int(FRAMES_PER_ACTION) - 1)
        self.dir_x = random.choice([-1, 1])
        self.dir_y = random.choice([-1, 1])
        self.size = 200
        self.draw_w = 100
        self.draw_h = 100
        self.x = random.randint(self.size // 2, 800 - self.size // 2)
        self.y = random.randint(self.size // 2, 600 - self.size // 2)

        self.change_timer = random.uniform(1.0, 3.0)

        self.attack_time = get_time()

    def get_bb(self):
        return self.x - 30, self.y - 50, self.x + 30, self.y

    def update(self):
        self.change_timer -= game_framework.frame_time

        if self.change_timer < 0:
            self.dir_x = random.choice([-1, 1])
            self.dir_y = random.choice([-1, 1])
            self.change_timer = random.uniform(1.0, 3.0)

        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        self.x += RUN_SPEED_PPS * self.dir_x * game_framework.frame_time
        self.y += RUN_SPEED_PPS * self.dir_y * game_framework.frame_time

        half_w = self.draw_w // 2
        half_h = self.draw_h // 2

        if self.x < half_w or self.x > 800 - half_w:
            self.x = clamp(half_w, self.x, 800 - half_w)
            self.dir_x *= -1

        if self.y < half_h or self.y > 600 - half_h:
            self.y = clamp(half_h, self.y, 600 - half_h)
            self.dir_y *= -1

        if self.x + 100 >= play_mode.player.x - 50 and self.x - 100 <= play_mode.player.x + 40 and self.y + 70 >= play_mode.player.y - 50 and self.y - 120 <= play_mode.player.y + 40:
            self.attack()

    def draw(self):
        if SLIME.image is None:
            return
        sx = int(self.frame) * 128
        if self.dir_x < 0:
            SLIME.image.clip_composite_draw(sx, 0, 128, 128, 0, 'h', self.x, self.y, self.draw_w, self.draw_h)
        else:
            SLIME.image.clip_draw(sx, 0, 128, 128, self.x, self.y, self.draw_w, self.draw_h)
        draw_rectangle(*self.get_bb())
        draw_rectangle(self.x - 100, self.y - 120, self.x + 100, self.y+70)

    def attack(self):
        if get_time() - self.attack_time > 3.0:
            self.attack_time = get_time()
            attack = Slime_Attack(self.x, self.y-25, self.dir_x, play_mode.player.x, play_mode.player.y)
            game_world.add_object(attack, 1)
            game_world.add_collision_pair('player:slime_attack', None, attack)

    def handle_event(self, event):
        pass

    def handle_collision(self, group, other):
        if group == 'slime:attack':
            print("Slime Hit!")
            game_world.remove_object(self)
        pass
