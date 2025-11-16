from pico2d import load_image

import player

class Ui:
    def __init__(self):
        self.image = load_image('UI.png')
        self.slime_image = load_image('P_Slime_RUN.png')

    def update(self):
        pass

    def draw(self):
        for i in range(4):
            if player.inventory[i]:

                item_name = player.inventory[i][0]
                count = player.inventory[i][1]

                if item_name == 'P_slime':
                    self.slime_image.clip_draw(0, 0, 128, 128, 1024 // 2 + (i*100), 768 // 6 - 40, 100, 100)

        self.image.draw(1024 // 2, 768 // 4, 512, 382)
