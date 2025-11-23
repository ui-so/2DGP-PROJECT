import random
import game_framework
import game_world

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
    blue_image = None

    def load_images(self):
        if P_SLIME.green_image is None:
            P_SLIME.green_image = load_image('Green_Slime_Run.png')
        if P_SLIME.blue_image is None:
            P_SLIME.blue_image = load_image('Blue_Slime_Run.png')

    def __init__(self, num=1, limit_x1=0, limit_x2=1024, limit_y1=0, limit_y2=784):
        self.num = num
        self.load_images()
        if self.num == 1:
            self.image = P_SLIME.green_image
            self.item_id = 'P_slime_green'  # 인벤토리용
        elif self.num == 2:
            self.image = P_SLIME.blue_image
            self.item_id = 'P_slime_blue'  # 인벤토리용
        else:
            self.image = None  # 예외 처리
        self.frame = random.randint(0, int(FRAMES_PER_ACTION) - 1)
        self.dir_x = random.choice([-1, 1])
        self.dir_y = random.choice([-1, 1])
        self.size = 200
        self.draw_w = 100
        self.draw_h = 100

        self.limit_x1 = limit_x1
        self.limit_x2 = limit_x2
        self.limit_y1 = limit_y1
        self.limit_y2 = limit_y2

        self.x = random.randint(self.limit_x1 + self.size // 2, self.limit_x2 - self.size // 2)
        self.y = random.randint(self.limit_y1 + self.size // 2, self.limit_y2 - self.size // 2)

        self.change_timer = random.uniform(1.0, 3.0)
        self.plort_timer = get_time()

    def get_bb(self):
        return self.x - 30, self.y - 50, self.x + 30, self.y

    def update(self):
        self.change_timer -= game_framework.frame_time

        if get_time() - self.plort_timer > 10.0:
            self.plort_timer = get_time()
            plort = Plort(self.num, self.x, self.y)
            game_world.add_object(plort, 1)
            game_world.add_collision_pair('catch:plort', None, plort)

        if self.change_timer < 0:
            self.dir_x = random.choice([-1, 1])
            self.dir_y = random.choice([-1, 1])
            self.change_timer = random.uniform(1.0, 3.0)

        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        self.x += RUN_SPEED_PPS * self.dir_x * game_framework.frame_time
        self.y += RUN_SPEED_PPS * self.dir_y * game_framework.frame_time

        half_w = self.draw_w // 2
        half_h = self.draw_h // 2

        if self.x < self.limit_x1 + half_w or self.x > self.limit_x2 - half_w:
            self.x = clamp(self.limit_x1 + half_w, self.x, self.limit_x2 - half_w)
            self.dir_x *= -1

        if self.y < self.limit_y1 + half_h or self.y > self.limit_y2 - half_h:
            self.y = clamp(self.limit_y1 + half_h, self.y, self.limit_y2 - half_h)
            self.dir_y *= -1


    def draw(self):
        if self.image is None:
            return

        sx = int(self.frame) * 128
        if self.dir_x < 0:
            self.image.clip_composite_draw(sx, 0, 128, 128, 0, 'h', self.x, self.y, self.draw_w, self.draw_h)
        else:
            self.image.clip_draw(sx, 0, 128, 128, self.x, self.y, self.draw_w, self.draw_h)

        draw_rectangle(*self.get_bb())

    def handle_event(self, event):
        pass

    def handle_collision(self, group, other):
        if group == 'slime:catch':
            print("Slime catch!")
            game_world.remove_object(self)
        pass
