from pico2d import load_image

class Ui:
    def __init__(self):
        self.image = load_image('UI.png')

    def update(self):
        pass

    def draw(self):
        self.image.draw(1024 // 2, 768 // 4, 512, 382)
