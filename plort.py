from pico2d import *
import game_world
import game_framework
from game_world import remove_object
import play_mode


class Plort:
    green_image = None
    red_image = None
    blue_image = None
    black_image = None

    def load_images(self):
        if Plort.green_image is None:
            Plort.green_image = load_image('Green_Plort.png')
        if Plort.red_image is None:
            Plort.red_image = load_image('Red_Plort.png')
        if Plort.blue_image is None:
            Plort.blue_image = load_image('Blue_Plort.png')
        if Plort.black_image is None:
            Plort.black_image = load_image('Black_Plort.png')

    def __init__(self, num = 1, x = 400, y = 300):
        self.load_images()

        self.size = 25
        self.num = num
        self.x, self.y = x, y

        if self.num == 1:
            self.image = Plort.green_image
            self.item_id = 'Green_plort'  # 인벤토리용
        elif self.num == 2:
            self.image = Plort.red_image
            self.item_id = 'Red_plort'
        elif self.num == 3:
            self.image = Plort.blue_image
            self.item_id = 'Blue_plort'  # 인벤토리용
        elif self.num == 4:
            self.image = Plort.black_image
            self.item_id = 'Black_plort'
        else:
            self.image = None  # 예외 처리

    def draw(self):
        sx = self.x - play_mode.camera_x
        sy = self.y - play_mode.camera_y
        self.image.draw(sx, sy, self.size, self.size)

    def update(self):
        pass

    def get_bb(self):
        return self.x - self.size//2 - play_mode.camera_x, self.y - self.size//2 - play_mode.camera_y, self.x + self.size//2 - play_mode.camera_x, self.y + self.size//2 - play_mode.camera_y

    def handle_collision(self, group, other):
        if group == 'catch:plort':
            game_world.remove_object(self)