from pico2d import load_image, get_time
from sdl2 import SDL_KEYDOWN, SDLK_SPACE, SDLK_d, SDL_KEYUP, SDLK_a, SDLK_w, SDLK_s, SDL_MOUSEBUTTONDOWN

from state_machine import StateMachine

# 키 상태 플래그
right_pressed = False
left_pressed = False
up_pressed = False
down_pressed = False


# 이벤트 검사 함수들
def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE


def time_out(e):
    return e[0] == 'TIME_OUT'


def right_down(e):
    global right_pressed
    if e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_d:
        right_pressed = True
        return True
    return False


def left_down(e):
    global left_pressed
    if e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_a:
        left_pressed = True
        return True
    return False


def up_down(e):
    global up_pressed
    if e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_w:
        up_pressed = True
        return True
    return False


def down_down(e):
    global down_pressed
    if e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_s:
        down_pressed = True
        return True
    return False


def right_up(e):
    global right_pressed
    if e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_d:
        right_pressed = False
        return True
    return False


def left_up(e):
    global left_pressed
    if e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_a:
        left_pressed = False
        return True
    return False


def up_up(e):
    global up_pressed
    if e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_w:
        up_pressed = False
        return True
    return False


def down_up(e):
    global down_pressed
    if e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_s:
        down_pressed = False
        return True
    return False


def mouse_left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_MOUSEBUTTONDOWN and e[1].button == 1


# 모든 키가 해제되었는지 검사하는 이벤트 (IDLE 전이용)
def all_keys_up(e):
    # only react to KEYUP events
    global right_pressed, left_pressed, up_pressed, down_pressed
    if e[0] != 'INPUT' or e[1].type != SDL_KEYUP:
        return False

    key = e[1].key
    if key == SDLK_d:
        right_pressed = False
    elif key == SDLK_a:
        left_pressed = False
    elif key == SDLK_w:
        up_pressed = False
    elif key == SDLK_s:
        down_pressed = False

    return not (right_pressed or left_pressed or up_pressed or down_pressed)


class Run:
    def __init__(self, player):
        self.player = player

    def enter(self, e):
        # enter에서는 별도 초기화 필요 없음
        pass

    def exit(self, e):
        pass

    def do(self):
        global right_pressed, left_pressed, up_pressed, down_pressed

        # 수평 처리: 우선순위 없음 — 동시에 누르면 정지
        if right_pressed and not left_pressed:
            self.player.dir_x = 1
            self.player.face_dir = 1
        elif left_pressed and not right_pressed:
            self.player.dir_x = -1
            self.player.face_dir = -1
        else:
            self.player.dir_x = 0

        # 수직 처리
        if up_pressed and not down_pressed:
            self.player.dir_y = 1
        elif down_pressed and not up_pressed:
            self.player.dir_y = -1
        else:
            self.player.dir_y = 0

        # 위치 업데이트
        self.player.frame = (self.player.frame + 1) % 6
        self.player.x += self.player.dir_x * 0.5
        self.player.y += self.player.dir_y * 0.5

    def draw(self):
        if self.player.face_dir == 1:
            self.player.image.clip_draw(self.player.frame * 32, 0, 32, 32, self.player.x, self.player.y, 100, 100)
        else:
            self.player.image.clip_composite_draw(self.player.frame * 32, 0, 32, 32, 0, 'h', self.player.x, self.player.y, 100, 100)


class Idle:
    def __init__(self, player):
        self.player = player

    def enter(self, e):
        self.player.dir_x = 0
        self.player.dir_y = 0
        self.player.wait_start_time = get_time()

    def exit(self, e):
        pass

    def do(self):
        self.player.frame = (self.player.frame + 1) % 6
        if get_time() - self.player.wait_start_time > 2.0:
            self.player.state_machine.handle_state_event(('TIME_OUT', None))

    def draw(self):
        if self.player.face_dir == 1:
            self.player.image.clip_draw(self.player.frame * 32, 0, 32, 32, self.player.x, self.player.y, 100, 100)
        else:
            self.player.image.clip_composite_draw(self.player.frame * 32, 0, 32, 32, 0, 'h', self.player.x, self.player.y, 100, 100)


class Sleep:
    def __init__(self, player):
        self.player = player

    def enter(self, e):
        self.player.dir_x = 0
        self.player.dir_y = 0

    def exit(self, e):
        pass

    def do(self):
        self.player.frame = (self.player.frame + 1) % 6

    def draw(self):
        if self.player.face_dir == 1:
            self.player.image.clip_composite_draw(self.player.frame * 32, 0, 32, 32, -3.141592 / 2, ' ', self.player.x, self.player.y - 25, 100, 100)
        else:
            self.player.image.clip_composite_draw(self.player.frame * 32, 0, 32, 32, 3.141592 / 2, ' ', self.player.x, self.player.y - 25, 100, 100)


class Attack:
    def __init__(self, player):
        self.player = player

    def enter(self, e):
        self.player.wait_start_time = get_time()

    def exit(self, e):
        pass

    def do(self):
        if get_time() - self.player.wait_start_time > 1.0:
            self.player.state_machine.handle_state_event(('TIME_OUT', None))

    def draw(self):
        if self.player.face_dir == 1:
            self.player.image.clip_draw(self.player.frame * 32, 0, 32, 32, self.player.x, self.player.y, 100, 100)
        else:
            self.player.image.clip_composite_draw(self.player.frame * 32, 0, 32, 32, 0, 'h', self.player.x, self.player.y, 100, 100)

        self.player.image.clip_draw(0, 0, 32, 32, self.player.x + 32, self.player.y, 30, 30)


class Player:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.face_dir = 1
        self.dir_x = 0
        self.dir_y = 0
        self.image = load_image('Pink_Monster_Run_6.png')

        self.RUN = Run(self)
        self.IDLE = Idle(self)
        self.SLEEP = Sleep(self)
        self.ATTACK = Attack(self)

        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.SLEEP: {space_down: self.IDLE},
                # IDLE: 키다운만 RUN으로 전이
                self.IDLE: {time_out: self.SLEEP, right_down: self.RUN, left_down: self.RUN, up_down: self.RUN, down_down: self.RUN, mouse_left_down: self.ATTACK},
                # RUN: 상태 유지(모든 키 이벤트은 RUN에서 처리), 키업 후 모든 키 해제 시 all_keys_up으로 IDLE로 전이
                self.RUN: {right_down: self.RUN, left_down: self.RUN, up_down: self.RUN, down_down: self.RUN, mouse_left_down: self.ATTACK, all_keys_up: self.IDLE},
                self.ATTACK: {right_down: self.RUN, left_down: self.RUN, right_up: self.RUN, left_up: self.RUN, up_down: self.RUN, down_down: self.RUN, all_keys_up: self.IDLE, time_out: self.IDLE}
            }
        )

    def update(self):
        self.state_machine.update()

    def draw(self):
        self.state_machine.draw()

    def handle_event(self, event):
        self.state_machine.handle_state_event(('INPUT', event))
        pass
