from pico2d import load_image, load_font

import player
import play_mode

class Ui:
    def __init__(self):
        global P_slime
        self.image = load_image('UI.png')
        self.HP = load_image('HP.png')
        self.MP = load_image('MP.png')
        self.Green_slime_image = load_image('Green_Slime_RUN.png')
        self.Blue_slime_image = load_image('Blue_Slime_RUN.png')
        self.Green_Plort = load_image('Green_Plort.png')
        self.Blue_Plort = load_image('Blue_Plort.png')

        self.font = load_font('ENCR10B.TTF', 16)

    def update(self):
        pass

    def draw(self):
        for i in range(4):
            if player.inventory[i]:

                item_name = player.inventory[i][0]
                count = player.inventory[i][1]

                if item_name == 'P_slime_green':
                    self.Green_slime_image.clip_draw(0, 0, 128, 128, 1024 // 2 + (i*70), 768 // 6 - 40, 100, 100)
                    self.font.draw(1024 // 2 + (i*70) + 5, 768 // 6 - 40 - 20, f'{count}', (0, 0, 0))
                elif item_name == 'P_slime_blue':
                    self.Blue_slime_image.clip_draw(0, 0, 128, 128, 1024 // 2 + (i*70), 768 // 6 - 40, 100, 100)
                    self.font.draw(1024 // 2 + (i*70) + 5, 768 // 6 - 40 - 20, f'{count}', (0, 0, 0))
                elif item_name == 'Green_plort':
                    self.Green_Plort.clip_draw(0, 0, 32, 32, 1024 // 2 + (i*70) -5, 768 // 6 - 80, 50, 50)
                    self.font.draw(1024 // 2 + (i*70) + 5, 768 // 6 - 40 - 20, f'{count}', (0, 0, 0))
                elif item_name == 'Blue_plort':
                    self.Blue_Plort.clip_draw(0, 0, 32, 32, 1024 // 2 + (i*70)-5, 768 // 6 - 80, 50, 50)
                    self.font.draw(1024 // 2 + (i*70) + 5, 768 // 6 - 40 - 20, f'{count}', (0, 0, 0))

        self.font.draw(1024 // 2 - 100, 768 // 6 - 40, f'{player.gold}', (0, 0, 0))
        self.image.draw(1024 // 2, 768 // 4, 512, 382)
        hp = play_mode.player.hp
        self.HP.clip_draw(0,0, hp*2, 10, 1024//2 - 150, 768//6-100)
        mp = play_mode.player.mp
        self.MP.clip_draw(0,0, mp*2, 10, 1024//2 - 150, 768//6-70)
