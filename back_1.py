from pico2d import load_image

class Back:
    def __init__(self):
        self.image = load_image('Back_1.png')
        self.x = 256
        self.y = 0

    def update(self):
        pass

    def draw(self):
        self.image.clip_draw(self.x, self.y, 256, 192, 512, 384, 1024, 768)
