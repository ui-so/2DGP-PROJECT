from pico2d import *
import game_world
import game_framework
from game_world import remove_object

PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 5.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

PIXEL_PER_METER = (1.0 / 0.003)  # 1pixel = 3cm, 1m = 33.33 pixel

class Slime_Attack:
    image = None

    def __init__(self, x = 400, y = 300, dir = 1, target_x = 400, target_y = 300):
        if Slime_Attack.image == None:
            Slime_Attack.image = load_image('Slime_attack.png')
        self.dir = dir
        self.size = 50
        self.x, self.y = x, y
        self.sx, self.sy = self.x, self.y
        self.tx, self.ty = target_x, target_y
        self.t = 0.0

    def draw(self):
        self.image.draw(self.x, self.y, self.size, self.size)
        draw_rectangle(*self.get_bb())

    def update(self):
        self.t += game_framework.frame_time / 1.0
        if self.t < 1.0:
            self.x = self.sx * (1.0 - self.t) + (self.tx * self.t)
            self.y = self.sy * (1.0 - self.t) + (self.ty * self.t)
        else:
            self.x, self.y = self.tx, self.ty
            game_world.remove_object(self)

    def get_bb(self):
        return self.x - self.size//2, self.y - self.size//2, self.x + self.size//2, self.y + self.size//2

    def handle_collision(self, group, other):
        if group == 'slime:attack':
            pass