import game_framework
from pico2d import *

import play_mode


def init():
    global image, bgm
    image = load_image('end.png')

    bgm = load_music('end_bgm.mp3')
    bgm.set_volume(32)
    bgm.repeat_play()


def finish():
    global image, bgm
    del image
    del bgm

def update():
    pass


def draw():
    clear_canvas()

    cw = get_canvas_width()
    ch = get_canvas_height()

    image.draw(cw // 2, ch // 2, cw, ch)
    update_canvas()


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            game_framework.quit()

def pause():
    pass


def resume():
    pass