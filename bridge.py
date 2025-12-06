from pico2d import load_image
import play_mode

class Bridge:
    def __init__(self, num = 1):
        if num == 1:
            self.image = load_image('Bridge_1.png')
        elif num == 2:
            self.image = load_image('Bridge_2.png')
        elif num == 3:
            self.image = load_image('Bridge_3.png')
        elif num == 4:
            self.image = load_image('Bridge_4.png')
        elif num == 5:
            self.image = load_image('Bridge_5.png')
        self.scale = 4.0  # 2배 확대

    def update(self):
        pass

    def draw(self):
        map_width = self.image.w * self.scale
        map_height = self.image.h * self.scale

        world_cx = map_width / 2
        world_cy = map_height / 2

        screen_x = world_cx - play_mode.camera_x
        screen_y = world_cy - play_mode.camera_y

        self.image.draw(screen_x, screen_y, map_width, map_height)
