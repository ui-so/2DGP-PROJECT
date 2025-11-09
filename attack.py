from pico2d import *
import game_world
import game_framework
from game_world import remove_object

PIXEL_PER_METER = (1.0 / 0.003)  # 1pixel = 3cm, 1m = 33.33 pixel

class Attack:
    image = None

    def __init__(self, x = 400, y = 300, dir = 1):
        if Attack.image == None:
            Attack.image = load_image('Player_Attack.png')
        self.x, self.y = x, y
        self.dir = dir
        self.size = 50

    def draw(self):
        self.image.draw(self.x, self.y, self.size, self.size)
        draw_rectangle(*self.get_bb())

    def update(self):
        # 위치 업데이트
        self.x += self.dir * game_framework.frame_time * PIXEL_PER_METER
        self.size += 50 * game_framework.frame_time
        # 삭제 조건 만족 시 즉시 제거하고 update 종료
        if self.size > 60:
            remove_object(self)  # from game_world import remove_object
            return

    def get_bb(self):
        return self.x - self.size//2, self.y - self.size//2, self.x + self.size//2, self.y + self.size//2

