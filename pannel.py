from pico2d import load_image, load_font
import player

class Pannel:
    def __init__(self):
        self.image = load_image('Farm_Shop.png')
        self.slime_image = load_image('P_Slime_RUN.png')
        self.font = load_font('ENCR10B.TTF', 16)

    def draw(self):
        self.image.draw(1024//2, 768//2, 768, 576)
        for i in range(4):
            if player.inventory[i]:

                item_name = player.inventory[i][0]
                count = player.inventory[i][1]

                if item_name == 'P_slime':
                    self.slime_image.clip_draw(0, 0, 128, 128, 1024 // 4 + (i*100) - 30, 768 // 3+20, 150, 150)
                    self.font.draw(1024 // 4 + (i*100) - 15, 768 // 3-5, f'{count}', (0, 0, 0))

    def update(self):
        pass