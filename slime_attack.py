from pico2d import *
import game_world
import game_framework
import play_mode
from game_world import remove_object

PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 5.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)


class Slime_Attack:
    green_image = None
    red_image = None
    blue_image = None
    black_image = None

    def load_images(self):
        if Slime_Attack.green_image is None:
            Slime_Attack.green_image = load_image('Green_attack.png')
        if Slime_Attack.red_image is None:
            Slime_Attack.red_image = load_image('Red_attack.png')
        if Slime_Attack.blue_image is None:
            Slime_Attack.blue_image = load_image('Blue_attack.png')
        if Slime_Attack.black_image is None:
            Slime_Attack.black_image = load_image('Black_attack.png')

    def __init__(self, map = 'prairie', x = 400, y = 300, dir = 1, target_x = 400, target_y = 300):
        self.load_images()
        if map == 'prairie':
            self.image = Slime_Attack.green_image
        elif map == 'lava':
            self.image = Slime_Attack.red_image
        elif map == 'ice':
            self.image = Slime_Attack.blue_image
        elif map == 'cave':
            self.image = Slime_Attack.black_image
        else:
            self.image = None

        self.dir = dir
        self.size = 35
        self.x, self.y = x, y
        self.sx, self.sy = self.x, self.y
        self.tx, self.ty = target_x, target_y
        self.t = 0.0

    def draw(self):
        sx = self.x - play_mode.camera_x
        sy = self.y - play_mode.camera_y
        self.image.draw(sx, sy, self.size, self.size)
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
        return self.x - self.size//2-play_mode.camera_x, self.y - self.size//2-play_mode.camera_y, self.x + self.size//2-play_mode.camera_x, self.y + self.size//2-play_mode.camera_y

    def handle_collision(self, group, other):
        if group == 'slime:attack':
            pass
        elif group == 'player:slime_attack':
            game_world.remove_object(self)