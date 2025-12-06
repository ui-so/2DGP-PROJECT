import game_framework
from pico2d import *

import play_mode


def init():
    global image
    # 이미지는 init에서 로드해야 합니다.
    image = load_image('start.png')


def finish():
    global image
    del image


def update():
    pass


def draw():
    clear_canvas()

    # 1. 화면(캔버스)의 너비와 높이를 가져옵니다.
    cw = get_canvas_width()
    ch = get_canvas_height()

    # 2. 이미지를 화면 중앙(cw // 2, ch // 2)에 그립니다.
    # 3. 뒤의 cw, ch는 이미지를 화면 크기에 딱 맞게 늘려서(resize) 그리라는 뜻입니다.
    image.draw(cw // 2, ch // 2, cw, ch)
    update_canvas()


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_s:
            game_framework.change_mode(play_mode)

def pause():
    pass


def resume():
    pass