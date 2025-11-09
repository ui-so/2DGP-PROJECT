from pico2d import *
import game_world
import game_framework
import player
from game_world import remove_object

PIXEL_PER_METER = (1.0 / 0.003)  # 1pixel = 3cm, 1m = 33.33 pixel

class Catch:
    image = None

    def __init__(self, x = 400, y = 300, dir = 1):
        self.x, self.y = x, y
        self.dir = dir
        self.size = 50
        self.time = get_time()

    def draw(self):
        draw_rectangle(*self.get_bb())

    def update(self):
        if get_time() - self.time > 0.2:
            game_world.remove_object(self)
        pass

    def get_bb(self):
        if self.dir == 1:
            return self.x, self.y - self.size//2, self.x + self.size, self.y + self.size//2
        else:
            return self.x - self.size*3, self.y - self.size//2, self.x- self.size*2, self.y + self.size//2

    def handle_collision(self, group, other):
        if group == 'slime:catch':
            print("Catch! Total Slime:", player.inventory)
            game_world.remove_object(self)