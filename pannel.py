from pico2d import load_image, load_font

import play_mode
import player
import farm_shop

class Pannel:
    def __init__(self):
        self.image = load_image('Farm_Shop.png')
        self.Green_slime_image = load_image('Green_Slime_RUN.png')
        self.Red_slime_image = load_image('Red_Slime_RUN.png')
        self.Blue_slime_image = load_image('Blue_Slime_RUN.png')
        self.Black_slime_image = load_image('Black_Slime_RUN.png')
        self.Green_Plort = load_image('Green_Plort.png')
        self.Red_Plort = load_image('Red_Plort.png')
        self.Blue_Plort = load_image('Blue_Plort.png')
        self.Black_Plort = load_image('Black_Plort.png')
        self.font = load_font('ENCR10B.TTF', 16)

    def draw(self):
        self.image.draw(1024//2, 768//2, 768, 576)
        self.font.draw(1024 // 4 + (4 * 120) - 60, 768 // 3,'PUT', (0, 0, 0))
        self.font.draw(1024 // 4 + (4 * 120) - 50, 768 // 3 - 75, 'TAKE OUT', (0, 0, 0))
        count = 0
        for i in range(4):
            if player.inventory[i]:

                item_name = player.inventory[i][0]
                count = player.inventory[i][1]

                if item_name == 'P_slime_green':
                    self.Green_slime_image.clip_draw(0, 0, 128, 128, 1024 // 4 + (i*120) - 30, 768 // 3+20, 150, 150)
                    self.font.draw(1024 // 4 + (i*120) - 15, 768 // 3-5, f'{count}', (0, 0, 0))
                elif item_name == 'P_slime_red':
                    self.Red_slime_image.clip_draw(0, 0, 128, 128, 1024 // 4 + (i*120) - 30, 768 // 3+20, 150, 150)
                    self.font.draw(1024 // 4 + (i*120) - 15, 768 // 3-5, f'{count}', (0, 0, 0))
                elif item_name == 'P_slime_blue':
                    self.Blue_slime_image.clip_draw(0, 0, 128, 128, 1024 // 4 + (i*120) - 30, 768 // 3+20, 150, 150)
                    self.font.draw(1024 // 4 + (i*120) - 15, 768 // 3-5, f'{count}', (0, 0, 0))
                elif item_name == 'P_slime_black':
                    self.Black_slime_image.clip_draw(0, 0, 128, 128, 1024 // 4 + (i*120) - 30, 768 // 3+20, 150, 150)
                    self.font.draw(1024 // 4 + (i*120) - 15, 768 // 3-5, f'{count}', (0, 0, 0))
                elif item_name == 'Green_plort':
                    self.Green_Plort.clip_draw(0, 0, 128, 128, 1024 // 4 + (i*120) - 40, 768 // 3 - 35, 75, 75)
                    self.font.draw(1024 // 4 + (i*120) - 15, 768 // 3-5, f'{count}', (0, 0, 0))
                elif item_name == 'Red_plort':
                    self.Red_Plort.clip_draw(0, 0, 128, 128, 1024 // 4 + (i*120) - 40, 768 // 3 - 35, 75, 75)
                    self.font.draw(1024 // 4 + (i*120) - 15, 768 // 3-5, f'{count}', (0, 0, 0))
                elif item_name == 'Blue_plort':
                    self.Blue_Plort.clip_draw(0, 0, 128, 128, 1024 // 4 + (i*120) - 40, 768 // 3 - 35, 75, 75)
                    self.font.draw(1024 // 4 + (i*120) - 15, 768 // 3-5, f'{count}', (0, 0, 0))
                elif item_name == 'Black_plort':
                    self.Black_Plort.clip_draw(0, 0, 128, 128, 1024 // 4 + (i*120) - 40, 768 // 3 - 35, 75, 75)
                    self.font.draw(1024 // 4 + (i*120) - 15, 768 // 3-5, f'{count}', (0, 0, 0))

        if farm_shop.farm_slime[farm_shop.farm_num-1]:
            if farm_shop.farm_slime[farm_shop.farm_num-1][0] == 'P_slime_green':
                self.Green_slime_image.clip_draw(0, 0, 128, 128, 1024 // 4 + 60, 768 // 2 + 200, 250, 250)
                self.font.draw(1024 // 4+35, 768 // 2 - 20, f'{farm_shop.farm_slime[farm_shop.farm_num-1][1]}', (0, 0, 0))

                self.Green_Plort.clip_draw(0, 0, 128, 128, 1024 // 4 + 260, 768 // 2 + 100, 150, 150)
                current_plort_data = play_mode.farm_plort[farm_shop.farm_num - 1]
                if current_plort_data:
                    count = current_plort_data[1]
                    self.font.draw(1024 // 4 + 250, 768 // 2 - 20, f'{count}', (0, 0, 0))
                else:
                    self.font.draw(1024 // 4 + 250, 768 // 2 - 20, '0', (0, 0, 0))

            elif farm_shop.farm_slime[farm_shop.farm_num-1][0] == 'P_slime_blue':
                self.Blue_slime_image.clip_draw(0, 0, 128, 128, 1024 // 4 + 60, 768 // 2 + 200, 250, 250)
                self.font.draw(1024 // 4+35, 768 // 2 - 20, f'{farm_shop.farm_slime[farm_shop.farm_num-1][1]}', (0, 0, 0))

                self.Blue_Plort.clip_draw(0, 0, 128, 128, 1024 // 4 + 260, 768 // 2 + 100, 150, 150)
                current_plort_data = play_mode.farm_plort[farm_shop.farm_num - 1]
                if current_plort_data:
                    count = current_plort_data[1]
                    self.font.draw(1024 // 4 + 250, 768 // 2 - 20, f'{count}', (0, 0, 0))
                else:
                    self.font.draw(1024 // 4 + 250, 768 // 2 - 20, '0', (0, 0, 0))

            elif farm_shop.farm_slime[farm_shop.farm_num-1][0] == 'P_slime_red':
                self.Red_slime_image.clip_draw(0, 0, 128, 128, 1024 // 4 + 60, 768 // 2 + 200, 250, 250)
                self.font.draw(1024 // 4+35, 768 // 2 - 20, f'{farm_shop.farm_slime[farm_shop.farm_num-1][1]}', (0, 0, 0))

                self.Red_Plort.clip_draw(0, 0, 128, 128, 1024 // 4 + 260, 768 // 2 + 100, 150, 150)
                current_plort_data = play_mode.farm_plort[farm_shop.farm_num - 1]
                if current_plort_data:
                    count = current_plort_data[1]
                    self.font.draw(1024 // 4 + 250, 768 // 2 - 20, f'{count}', (0, 0, 0))
                else:
                    self.font.draw(1024 // 4 + 250, 768 // 2 - 20, '0', (0, 0, 0))


            elif farm_shop.farm_slime[farm_shop.farm_num-1][0] == 'P_slime_black':
                self.Black_slime_image.clip_draw(0, 0, 128, 128, 1024 // 4 + 60, 768 // 2 + 200, 250, 250)
                self.font.draw(1024 // 4+35, 768 // 2 - 20, f'{farm_shop.farm_slime[farm_shop.farm_num-1][1]}', (0, 0, 0))
                self.Black_Plort.clip_draw(0, 0, 128, 128, 1024 // 4 + 260, 768 // 2 + 100, 150, 150)
                current_plort_data = play_mode.farm_plort[farm_shop.farm_num - 1]
                if current_plort_data:
                    count = current_plort_data[1]
                    self.font.draw(1024 // 4 + 250, 768 // 2 - 20, f'{count}', (0, 0, 0))
                else:
                    self.font.draw(1024 // 4 + 250, 768 // 2 - 20, '0', (0, 0, 0))


    def update(self):
        pass