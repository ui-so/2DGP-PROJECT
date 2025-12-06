from pico2d import load_image, load_font
import player
import farm_shop
import shop


class ShopPannel:
    def __init__(self, page = 0):
        self.image = load_image('Farm_Shop.png')
        self.shop_image_1 = load_image('shop_pannel.png')
        self.shop_image_2 = load_image('Shop_ui.png')
        self.Green_slime_image = load_image('Green_Slime_RUN.png')
        self.Blue_slime_image = load_image('Blue_Slime_RUN.png')
        self.Red_slime_image = load_image('Red_Slime_RUN.png')
        self.Black_slime_image = load_image('Black_Slime_RUN.png')
        self.Green_Plort = load_image('Green_Plort.png')
        self.Blue_Plort = load_image('Blue_Plort.png')
        self.Red_Plort = load_image('Red_Plort.png')
        self.Black_Plort = load_image('Black_Plort.png')
        self.font = load_font('ENCR10B.TTF', 16)

        self.Page = page

    def draw(self):
            if self.Page == 0:
                self.shop_image_1.draw(1024//2, 768//2, 768, 576)
                self.font.draw(1024 // 4 + (4 * 120) - 60, 768 // 3-35,'Sell', (0, 0, 0))
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
                        elif item_name == 'P_slime_red':
                            self.Red_slime_image.clip_draw(0, 0, 128, 128, 1024 // 4 + (i*120) - 30, 768 // 3+20, 150, 150)
                            self.font.draw(1024 // 4 + (i*120) - 15, 768 // 3-5, f'{count}', (0, 0, 0))
                        elif item_name == 'P_slime_black':
                            self.Black_slime_image.clip_draw(0, 0, 128, 128, 1024 // 4 + (i*120) - 30, 768 // 3+20, 150, 150)
                            self.font.draw(1024 // 4 + (i*120) - 15, 768 // 3-5, f'{count}', (0, 0, 0))
                        elif item_name == 'Green_plort':
                            self.Green_Plort.clip_draw(0, 0, 128, 128, 1024 // 4 + (i*120) - 40, 768 // 3 - 35, 75, 75)
                            self.font.draw(1024 // 4 + (i*120) - 15, 768 // 3-5, f'{count}', (0, 0, 0))
                        elif item_name == 'Blue_plort':
                            self.Blue_Plort.clip_draw(0, 0, 128, 128, 1024 // 4 + (i*120) - 40, 768 // 3 - 35, 75, 75)
                            self.font.draw(1024 // 4 + (i*120) - 15, 768 // 3-5, f'{count}', (0, 0, 0))
                        elif item_name == 'Red_plort':
                            self.Red_Plort.clip_draw(0, 0, 128, 128, 1024 // 4 + (i*120) - 40, 768 // 3 - 35, 75, 75)
                            self.font.draw(1024 // 4 + (i*120) - 15, 768 // 3-5, f'{count}', (0, 0, 0))
                        elif item_name == 'Black_plort':
                            self.Black_Plort.clip_draw(0, 0, 128, 128, 1024 // 4 + (i*120) - 40, 768 // 3 - 35, 75, 75)
                            self.font.draw(1024 // 4 + (i*120) - 15, 768 // 3-5, f'{count}', (0, 0, 0))
                self.Green_Plort.clip_draw(0, 0, 128, 128, 1024 // 4- 20, 768 // 2 + 100, 150, 150)
                self.font.draw(1024 // 4-35, 768 // 2 - 20, f'+10', (0, 0, 0))
                self.Red_Plort.clip_draw(0, 0, 128, 128, 1024 // 4 + 160, 768 // 2 + 100, 150, 150)
                self.font.draw(1024 // 4+145, 768 // 2 - 20, f'+25', (0, 0, 0))
                self.Blue_Plort.clip_draw(0, 0, 128, 128, 1024 // 4 + 350, 768 // 2 + 100, 150, 150)
                self.font.draw(1024 // 4+330, 768 // 2 - 20, f'+40', (0, 0, 0))
                self.Black_Plort.clip_draw(0, 0, 128, 128, 1024 // 4 + 530, 768 // 2 + 100, 150, 150)
                self.font.draw(1024 // 4+515, 768 // 2 - 20, f'+60', (0, 0, 0))

            elif self.Page == 1:
                self.shop_image_2.draw(1024 // 2, 768 // 2, 768, 576)
                if shop.shop_count[0] < 10:
                    self.font.draw(1024 // 4 + 10, 768 // 2 - 90, f'-{shop.shop_gold[0]}', (0, 0, 0))
                else:
                    self.font.draw(1024 // 4 + 10, 768 // 2 - 90, 'MAX', (0, 0, 0))
                if shop.shop_count[1] < 10:
                    self.font.draw(1024 // 4 + 250, 768 // 2 - 90, f'-{shop.shop_gold[1]}', (0, 0, 0))
                else:
                    self.font.draw(1024 // 4 + 250, 768 // 2 - 90, 'MAX', (0, 0, 0))
                if shop.shop_count[2] < 5:
                    self.font.draw(1024 // 4 + 480, 768 // 2 - 90, f'-{shop.shop_gold[2]}', (0, 0, 0))
                else:
                    self.font.draw(1024 // 4 + 480, 768 // 2 - 90, 'MAX', (0, 0, 0))
    def update(self):
        pass