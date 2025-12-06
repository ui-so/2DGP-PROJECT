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
        self.Red_slime_image = load_image('Red_Slime_RUN.png')
        self.Blue_slime_image = load_image('Blue_Slime_RUN.png')
        self.Black_slime_image = load_image('Black_Slime_RUN.png')
        self.Green_Plort = load_image('Green_Plort.png')
        self.Red_Plort = load_image('Red_Plort.png')
        self.Blue_Plort = load_image('Blue_Plort.png')
        self.Black_Plort = load_image('Black_Plort.png')
        self.Green_Key = load_image('Green_Key.png')
        self.Red_Key = load_image('Red_Key.png')
        self.Blue_Key = load_image('Blue_Key.png')
        self.Black_Key = load_image('Black_Key.png')

        self.font = load_font('ENCR10B.TTF', 16)

    def update(self):
        pass

    def draw(self):
        self.image.draw(1024 // 2, 768 // 4, 512, 382)
        for i in range(4):
            if player.inventory[i]:

                item_name = player.inventory[i][0]
                count = player.inventory[i][1]

                if item_name == 'P_slime_green':
                    self.Green_slime_image.clip_draw(0, 0, 128, 128, 1024 // 2 + (i*70), 768 // 6 - 40, 100, 100)
                    self.font.draw(1024 // 2 + (i*70) + 5, 768 // 6 - 40 - 20, f'{count}', (0, 0, 0))
                elif item_name == 'P_slime_red':
                    self.Red_slime_image.clip_draw(0, 0, 128, 128, 1024 // 2 + (i*70), 768 // 6 - 40, 100, 100)
                    self.font.draw(1024 // 2 + (i*70) + 5, 768 // 6 - 40 - 20, f'{count}', (0, 0, 0))
                elif item_name == 'P_slime_blue':
                    self.Blue_slime_image.clip_draw(0, 0, 128, 128, 1024 // 2 + (i*70), 768 // 6 - 40, 100, 100)
                    self.font.draw(1024 // 2 + (i*70) + 5, 768 // 6 - 40 - 20, f'{count}', (0, 0, 0))
                elif item_name == 'P_slime_black':
                    self.Black_slime_image.clip_draw(0, 0, 128, 128, 1024 // 2 + (i*70), 768 // 6 - 40, 100, 100)
                    self.font.draw(1024 // 2 + (i*70) + 5, 768 // 6 - 40 - 20, f'{count}', (0, 0, 0))
                elif item_name == 'Green_plort':
                    self.Green_Plort.clip_draw(0, 0, 32, 32, 1024 // 2 + (i*70) -5, 768 // 6 - 80, 50, 50)
                    self.font.draw(1024 // 2 + (i*70) + 5, 768 // 6 - 40 - 20, f'{count}', (0, 0, 0))
                elif item_name == 'Red_plort':
                    self.Red_Plort.clip_draw(0, 0, 32, 32, 1024 // 2 + (i*70)-5, 768 // 6 - 80, 50, 50)
                    self.font.draw(1024 // 2 + (i*70) + 5, 768 // 6 - 40 - 20, f'{count}', (0, 0, 0))
                elif item_name == 'Blue_plort':
                    self.Blue_Plort.clip_draw(0, 0, 32, 32, 1024 // 2 + (i*70)-5, 768 // 6 - 80, 50, 50)
                    self.font.draw(1024 // 2 + (i*70) + 5, 768 // 6 - 40 - 20, f'{count}', (0, 0, 0))
                elif item_name == 'Black_plort':
                    self.Black_Plort.clip_draw(0, 0, 32, 32, 1024 // 2 + (i*70)-5, 768 // 6 - 80, 50, 50)
                    self.font.draw(1024 // 2 + (i*70) + 5, 768 // 6 - 40 - 20, f'{count}', (0, 0, 0))


        for i in range(4):
            if play_mode.KEY[i]:
                if i == 0:
                    self.Green_Key.clip_draw(0, 0, 32, 32, 1024 // 2 - 275 + (i*40), 768 // 6 - 40, 40, 40)
                elif i == 1:
                    self.Red_Key.clip_draw(0, 0, 32, 32, 1024 // 2 - 275 + (i*40), 768 // 6- 40, 40, 40)
                elif i == 2:
                    self.Blue_Key.clip_draw(0, 0, 32, 32, 1024 // 2 - 275 + (i*40), 768 // 6- 40, 40, 40)
                elif i == 3:
                    self.Black_Key.clip_draw(0, 0, 32, 32, 1024 // 2 - 275 + (i*40), 768 // 6 - 40, 40, 40)
        self.font.draw(1024 // 2 - 120, 768 // 6 - 58, f'{player.gold}', (0, 0, 0))

        FIXED_BAR_WIDTH = 200

        ratio = play_mode.player.hp / player.hp_max
        current_bar_width = FIXED_BAR_WIDTH * ratio
        right_anchor = (1024 // 2 - 151) + (FIXED_BAR_WIDTH / 2)
        draw_x = right_anchor - (current_bar_width / 2)
        self.HP.clip_draw(0,0, int(200 * ratio), 10, draw_x, 768//6-100,current_bar_width, 10)
        ratio = play_mode.player.mp / player.mp_max
        current_bar_width = FIXED_BAR_WIDTH * ratio
        right_anchor = (1024 // 2 - 151) + (FIXED_BAR_WIDTH / 2)
        draw_x = right_anchor - (current_bar_width / 2)
        self.MP.clip_draw(0,0, int(200 * ratio), 10, draw_x, 768//6-80,current_bar_width, 10)
