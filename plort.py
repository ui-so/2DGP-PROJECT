from pico2d import *
import game_world
import game_framework
from game_world import remove_object


class Plort:
    green_image = None
    blue_image = None

    def load_images(self):
        if Plort.green_image is None:
            Plort.green_image = load_image('Green_Plort.png')
        if Plort.blue_image is None:
            Plort.blue_image = load_image('Blue_Plort.png')

    def __init__(self, num = 1, x = 400, y = 300):
        self.load_images()

        self.size = 35
        self.num = num
        self.x, self.y = x, y

        if self.num == 1:
            self.image = Plort.green_image
            self.item_id = 'Green_plort'  # 인벤토리용
        elif self.num == 2:
            self.image = Plort.blue_image
            self.item_id = 'Blue_plort'  # 인벤토리용
        else:
            self.image = None  # 예외 처리

    def draw(self):
        self.image.draw(self.x, self.y, self.size, self.size)
        draw_rectangle(*self.get_bb())

    def update(self):
        pass

    def get_bb(self):
        return self.x - self.size//2, self.y - self.size//2, self.x + self.size//2, self.y + self.size//2

    def handle_collision(self, group, other):
        if group == 'catch:plort':
            game_world.remove_object(self)