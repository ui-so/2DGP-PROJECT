from pico2d import load_image, load_font
import player
import farm_shop

class ShopPannel:
    def __init__(self, page = 0):
        self.image = load_image('Farm_Shop.png')
        self.shop_image = load_image('Shop_ui.png')
        self.Green_slime_image = load_image('Green_Slime_RUN.png')
        self.Blue_slime_image = load_image('Blue_Slime_RUN.png')
        self.Green_Plort = load_image('Green_Plort.png')
        self.Blue_Plort = load_image('Blue_Plort.png')
        self.font = load_font('ENCR10B.TTF', 16)

        self.Page = page

    def draw(self):
        if self.Page == 0:
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
                    elif item_name == 'P_slime_blue':
                        self.Blue_slime_image.clip_draw(0, 0, 128, 128, 1024 // 4 + (i*120) - 30, 768 // 3+20, 150, 150)
                        self.font.draw(1024 // 4 + (i*120) - 15, 768 // 3-5, f'{count}', (0, 0, 0))
                    elif item_name == 'Green_plort':
                        self.Green_Plort.clip_draw(0, 0, 128, 128, 1024 // 4 + (i*120) - 40, 768 // 3 - 35, 75, 75)
                        self.font.draw(1024 // 4 + (i*120) - 15, 768 // 3-5, f'{count}', (0, 0, 0))
                    elif item_name == 'Blue_plort':
                        self.Blue_Plort.clip_draw(0, 0, 128, 128, 1024 // 4 + (i*120) - 40, 768 // 3 - 35, 75, 75)
                        self.font.draw(1024 // 4 + (i*120) - 15, 768 // 3-5, f'{count}', (0, 0, 0))

            if farm_shop.Now_slime:
                if farm_shop.Now_slime[0] == 'P_slime_green':
                    self.Green_slime_image.clip_draw(0, 0, 128, 128, 1024 // 4 + 20, 768 // 2 + 250, 250, 250)
                    self.font.draw(1024 // 4, 768 // 2 + 50, f'{farm_shop.Now_slime[1]}', (0, 0, 0))
                elif farm_shop.Now_slime[0] == 'P_slime_blue':
                    self.Blue_slime_image.clip_draw(0, 0, 128, 128, 1024 // 4 + 20, 768 // 2 + 250, 250, 250)
                    self.font.draw(1024 // 4, 768 // 2 + 50, f'{farm_shop.Now_slime[1]}', (0, 0, 0))

        elif self.Page == 1:
            self.shop_image.draw(1024 // 2, 768 // 2, 768, 576)

    def update(self):
        pass