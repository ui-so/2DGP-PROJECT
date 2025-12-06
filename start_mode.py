import game_framework
from pico2d import *

import play_mode


def init():
    global image, bgm, click
    image = load_image('start.png')

    bgm = load_music('start_bgm.mp3')
    bgm.set_volume(32)
    bgm.repeat_play()

    click = load_wav('Button_sound.mp3')
    click.set_volume(32)


def finish():
    global image, bgm, click
    del image
    del bgm
    del click


def update():
    pass


def draw():
    clear_canvas()

    cw = get_canvas_width()
    ch = get_canvas_height()

    image.draw(cw // 2, ch // 2, cw, ch)
    update_canvas()


def handle_events():
    global click
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            click.play()
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            click.play()
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_s:
            click.play()
            game_framework.change_mode(play_mode)

def pause():
    pass

def resume():
    pass