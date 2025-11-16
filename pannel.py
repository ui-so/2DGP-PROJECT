from pico2d import load_image

class Pannel:
    def __init__(self):
        self.image = load_image('Farm_Shop.png')

    def draw(self):
        self.image.draw(1024//2, 768//2, 768, 576)

    def update(self):
        pass