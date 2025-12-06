from pico2d import *
import game_world
import game_framework
from game_world import remove_object
import play_mode


class Key:
    green_image = None
    red_image = None
    blue_image = None
    black_image = None

    def load_images(self):
        if Key.green_image is None:
            Key.green_image = load_image('Green_Key.png')
        if Key.red_image is None:
            Key.red_image = load_image('Red_Key.png')
        if Key.blue_image is None:
            Key.blue_image = load_image('Blue_Key.png')
        if Key.black_image is None:
            Key.black_image = load_image('Black_Key.png')

    def __init__(self, num = 1, x = 400, y = 300):
        self.load_images()

        self.size = 35
        self.num = num
        self.x, self.y = x, y

        if self.num == 1:
            self.image = Key.green_image
        elif self.num == 2:
            self.image = Key.red_image
        elif self.num == 3:
            self.image = Key.blue_image
        elif self.num == 4:
            self.image = Key.black_image
        else:
            self.image = None  # 예외 처리

    def draw(self):
        sx = self.x - play_mode.camera_x
        sy = self.y - play_mode.camera_y
        self.image.draw(sx, sy, self.size, self.size)
        draw_rectangle(*self.get_bb())

    def update(self):
        pass

    def get_bb(self):
        return self.x - self.size//2 - play_mode.camera_x, self.y - self.size//2 - play_mode.camera_y, self.x + self.size//2 - play_mode.camera_x, self.y + self.size//2 - play_mode.camera_y

    def handle_collision(self, group, other):
        if group == 'player:key':
            game_world.remove_object(self)
            play_mode.KEY[self.num - 1] = 1