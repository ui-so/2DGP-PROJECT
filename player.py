from pico2d import load_image, get_time
from sdl2 import SDL_KEYDOWN, SDLK_SPACE, SDLK_RIGHT, SDL_KEYUP, SDLK_LEFT, SDLK_a

from state_machine import StateMachine


# 이벤트를 체크하는 함수들을 구현
def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE


def time_out(e):
    return e[0] == 'TIME_OUT'


def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT


def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT


def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT


def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT


def auto_run(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_a


class Run:
    def __init__(self, player):
        self.player = player

    def enter(self, e):
        if right_down(e) or left_up(e):
            self.player.dir = self.player.face_dir = 1
        elif left_down(e) or right_up(e):
            self.player.dir = self.player.face_dir = -1

    def exit(self, e):
        pass

    def do(self):
        self.player.frame = (self.player.frame + 1) % 6
        self.player.x += self.player.dir * 5

    def draw(self):
        if self.player.face_dir == 1:  # right
            self.player.image.clip_draw(self.player.frame * 32, 0, 32, 32, self.player.x, self.player.y, 100, 100)
        else:  # face_dir == -1: # left
            self.player.image.clip_composite_draw(self.player.frame * 32, 0, 32, 32, 0, 'h', self.player.x, self.player.y, 100, 100)


class Idle:
    def __init__(self, player):
        self.player = player

    def enter(self, e):
        self.player.dir = 0
        self.player.wait_start_time = get_time()

    def exit(self, e):
        pass

    def do(self):
        self.player.frame = (self.player.frame + 1) % 6
        if get_time() - self.player.wait_start_time > 2.0:
            # IDLE 2초 경과, state machine에게 TIME_OUT 이벤트 전달
            self.player.state_machine.handle_state_event(('TIME_OUT', None))

    def draw(self):
        if self.player.face_dir == 1:  # right
            self.player.image.clip_draw(self.player.frame * 32, 0, 32, 32, self.player.x, self.player.y, 100, 100)
        else:  # face_dir == -1: # left
            self.player.image.clip_composite_draw(self.player.frame * 32, 0, 32, 32, 0, 'h', self.player.x, self.player.y, 100, 100)


class Sleep:
    def __init__(self, player):
        self.player = player

    def enter(self, e):
        self.player.dir = 0

    def exit(self, e):
        pass

    def do(self):
        self.player.frame = (self.player.frame + 1) % 6

    def draw(self):
        if self.player.face_dir == 1:  # right
            self.player.image.clip_composite_draw(self.player.frame * 32, 0, 32, 32, -3.141592 / 2, ' ', self.player.x,
                                               self.player.y - 25, 100, 100)
        else:  # face_dir == -1: # left
            self.player.image.clip_composite_draw(self.player.frame * 32, 0, 32, 32, 3.141592 / 2, ' ', self.player.x,
                                               self.player.y - 25, 100, 100)


class Player:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.face_dir = 1
        self.dir = 0
        self.image = load_image('Pink_Monster_Run_6.png')

        self.RUN = Run(self)
        self.IDLE = Idle(self)
        self.SLEEP = Sleep(self)  # 새로운 SLEEP 상태 생성

        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.SLEEP: {space_down: self.IDLE},
                self.IDLE: {time_out: self.SLEEP, right_down: self.RUN, left_down: self.RUN,
                            right_up: self.RUN, left_up: self.RUN
                            },
                self.RUN: {right_up: self.IDLE, left_up: self.IDLE,
                           right_down: self.IDLE, left_down: self.IDLE}
            }
        )

    def update(self):
        self.state_machine.update()

    def draw(self):
        self.state_machine.draw()

    def handle_event(self, event):
        # 들어온 외부 키입력 등을 상태 머신에게 전달하기 위해서 튜플화 시킨 후, 전달
        self.state_machine.handle_state_event(('INPUT', event))
        pass
