from pico2d import load_image, load_font
import player
import farm_shop

class Pannel:
    def __init__(self):
        self.image = load_image('Farm_Shop.png')
        self.slime_image = load_image('P_Slime_RUN.png')
        self.font = load_font('ENCR10B.TTF', 16)

    def draw(self):
        self.image.draw(1024//2, 768//2, 768, 576)
        self.font.draw(1024 // 4 + (4 * 120) - 60, 768 // 3,'PUT', (0, 0, 0))
        self.font.draw(1024 // 4 + (4 * 120) - 50, 768 // 3 - 75, 'TAKE OUT', (0, 0, 0))
        for i in range(4):
            if player.inventory[i]:

                item_name = player.inventory[i][0]
                count = player.inventory[i][1]

                if item_name == 'P_slime':
                    self.slime_image.clip_draw(0, 0, 128, 128, 1024 // 4 + (i*100) - 30, 768 // 3+20, 150, 150)
                    self.font.draw(1024 // 4 + (i*100) - 15, 768 // 3-5, f'{count}', (0, 0, 0))

        if farm_shop.Now_slime:
            if farm_shop.Now_slime[0] == 'P_slime':
                self.slime_image.clip_draw(0, 0, 128, 128, 1024 // 4 + 20, 768 // 2 + 250, 250, 250)
                self.font.draw(1024 // 4, 768 // 2 + 50, f'{farm_shop.Now_slime[1]}', (0, 0, 0))

    def update(self):
        pass