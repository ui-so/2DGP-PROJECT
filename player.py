import math
from operator import contains

from pico2d import load_image, get_time, draw_rectangle
from sdl2 import SDL_KEYDOWN, SDLK_SPACE, SDLK_d, SDL_KEYUP, SDLK_a, SDLK_w, SDLK_s, SDL_MOUSEBUTTONDOWN

from state_machine import StateMachine

import game_world
import game_framework
import play_mode

from attack import Attack
from catch import Catch


# Player Run Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 40.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# Player Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 6

# 키 상태 플래그
right_pressed = False
left_pressed = False
up_pressed = False
down_pressed = False

collision_flag = True
collision_time = 0.0

inventory = [[],[],[],[]]
inventory_max = 10
hp_max = 100
mp_max = 100
gold = 0

cx, cy, rx, ry = 1925, 890, 300, 230
rl, rb, rr, rt = 1325, 840, 1725, 1010

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

def mouse_right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_MOUSEBUTTONDOWN and e[1].button == 3


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


def hurt(e):
    return e[0] == 'hurt'

def Finish_Hurt(e):
    return e[0] == 'Finish_Hurt'

def death(e):
    return e[0] == 'death'

class Run:
    def __init__(self, player):
        self.player = player

    def enter(self, e):
        # enter에서는 별도 초기화 필요 없음
        pass

    def exit(self, e):
        if space_down(e):
            self.player.attack_()

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
        self.player.frame = (self.player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 6
        self.player.x += self.player.dir_x * RUN_SPEED_PPS * game_framework.frame_time
        self.player.y += self.player.dir_y * RUN_SPEED_PPS * game_framework.frame_time

        global collision_time, collision_flag
        if not collision_flag and get_time() - collision_time > 2.0:
            collision_flag = True

    def draw(self):
        if self.player.face_dir == 1:
            self.player.Run_image.clip_draw(int(self.player.frame) * 32, 0, 32, 32, self.player.x-play_mode.camera_x, self.player.y-play_mode.camera_y, 100, 100)
        else:
            self.player.Run_image.clip_composite_draw(int(self.player.frame) * 32, 0, 32, 32, 0, 'h', self.player.x-play_mode.camera_x, self.player.y-play_mode.camera_y, 100, 100)


class Idle:
    def __init__(self, player):
        self.player = player

    def enter(self, e):
        self.player.dir_x = 0
        self.player.dir_y = 0
        global right_pressed, left_pressed, up_pressed, down_pressed
        right_pressed = False
        left_pressed = False
        up_pressed = False
        down_pressed = False

    def exit(self, e):
        if space_down(e):
            self.player.attack_()

    def do(self):
        self.player.frame = (self.player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        global collision_time, collision_flag
        if not collision_flag and get_time() - collision_time > 2.0:
            collision_flag = True

    def draw(self):
        if self.player.face_dir == 1:
            self.player.Idle_image.clip_draw(int(self.player.frame) * 32, 0, 32, 32, self.player.x-play_mode.camera_x, self.player.y-play_mode.camera_y, 100, 100)
        else:
            self.player.Idle_image.clip_composite_draw(int(self.player.frame) * 32, 0, 32, 32, 0, 'h', self.player.x-play_mode.camera_x, self.player.y-play_mode.camera_y, 100, 100)


class Hurt:
    def __init__(self, player, num = 0):
        self.player = player

    def enter(self, e):
        self.player.dir_x = 0
        self.player.dir_y = 0
        self.player.frame = 0

    def exit(self, e):
        pass

    def do(self):
        self.player.frame = (self.player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time)
        if self.player.frame > 3:
            self.player.frame = 0
            self.player.state_machine.handle_state_event(('Finish_Hurt', None))
            global collision_flag, collision_time
            collision_time = get_time()
            collision_flag = False

    def draw(self):
        if self.player.face_dir == 1:
            self.player.Hurt_image.clip_draw(int(self.player.frame) * 32, 0, 32, 32, self.player.x-play_mode.camera_x, self.player.y-play_mode.camera_y, 100, 100)
        else:
            self.player.Hurt_image.clip_composite_draw(int(self.player.frame) * 32, 0, 32, 32, 0, 'h', self.player.x-play_mode.camera_x, self.player.y-play_mode.camera_y, 100, 100)



class Death:
    def __init__(self, player):
        self.player = player

    def enter(self, e):
        self.player.frame = 0

    def exit(self, e):
        global inventory
        for i in range(4):
            inventory[i] = []
        self.player.hp = 100

    def do(self):
        self.player.frame = (self.player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time * 0.5)
        if self.player.frame > 7:
            self.player.frame = 0
            self.player.state_machine.handle_state_event(('Finish_Hurt', None))

    def draw(self):
        if self.player.face_dir == 1:
            self.player.Death_image.clip_draw(int(self.player.frame) * 32, 0, 32, 32, self.player.x-play_mode.camera_x, self.player.y-play_mode.camera_y, 100, 100)
        else:
            self.player.Death_image.clip_composite_draw(int(self.player.frame) * 32, 0, 32, 32, 0, 'h', self.player.x-play_mode.camera_x, self.player.y-play_mode.camera_y, 100, 100)


class Player:
    def __init__(self):
        self.x, self.y = 1925, 870
        self.frame = 0
        self.face_dir = 1
        self.dir_x = 0
        self.dir_y = 0
        self.Run_image = load_image('Player_Run.png')
        self.Idle_image = load_image('Player_Idle.png')
        self.Hurt_image = load_image('Player_Hurt.png')
        self.Death_image = load_image('Player_Death.png')

        self.hp = 100
        self.mp = 100

        self.RUN = Run(self)
        self.IDLE = Idle(self)
        self.Hurt = Hurt(self)
        self.Death = Death(self)

        self.state_machine = StateMachine(
            self.IDLE,
            {
                # IDLE: 키다운만 RUN으로 전이
                self.IDLE: {right_down: self.RUN, left_down: self.RUN, up_down: self.RUN, down_down: self.RUN, hurt:self.Hurt, death:self.Death},
                # RUN: 상태 유지(모든 키 이벤트은 RUN에서 처리), 키업 후 모든 키 해제 시 all_keys_up으로 IDLE로 전이
                self.RUN: {right_down: self.RUN, left_down: self.RUN, up_down: self.RUN, down_down: self.RUN, all_keys_up: self.IDLE, hurt:self.Hurt, death:self.Death},
                self.Hurt: {Finish_Hurt:self.IDLE,death:self.Death},
                self.Death: {Finish_Hurt: self.IDLE},
            }
        )

    def update(self):
        self.state_machine.update()
        global cx, cy, rx, ry, rl, rb, rr, rt
        if play_mode.MAP == 'spawn_1':
            if self.x < 1525:
                play_mode.MAP = 'farm'
                cx, cy = 780, 935
                rx, ry = 515, 345
                rl, rb, rr, rt = 1225, 840, 1725, 1010
            elif self.x > 2000:
                play_mode.MAP = 'spawn_2'
                cx, cy = 1925, 890
                rx, ry = 300, 230
                rl, rb, rr, rt = 2100, 800, 2725, 990
            self.combined_map_limit(cx, cy, rx, ry, rl, rb, rr, rt)
        elif play_mode.MAP == 'spawn_2':
            if self.x < 2000:
                play_mode.MAP = 'spawn_1'
                cx, cy = 1925, 890
                rx, ry = 300, 230
                rl, rb, rr, rt = 1325, 840, 1725, 1010
            elif self.x > 2500:
                play_mode.MAP = 'prairie_1'
                cx, cy = 3670, 860
                rx, ry = 890, 520
                rl, rb, rr, rt = 2100, 800, 3025, 990
            self.combined_map_limit(cx, cy, rx, ry, rl, rb, rr, rt)

        elif play_mode.MAP == 'farm':
            if self.x > 1525:
                play_mode.MAP = 'spawn_1'
                cx, cy = 1925, 890
                rx, ry = 300, 230
                rl, rb, rr, rt = 1325, 840, 1725, 1010
            self.combined_map_limit(cx, cy, rx, ry, rl, rb, rr, rt)

        elif play_mode.MAP == 'prairie_1':
            if self.y > 1100:
                play_mode.MAP = 'prairie_2'
                cx, cy = 3670, 860
                rx, ry = 890, 520
                rl, rb, rr, rt = 3560, 1260, 3760, 2300
            self.combined_map_limit(cx, cy, rx, ry, rl, rb, rr, rt)
        elif play_mode.MAP == 'prairie_2':
            if self.y < 1100:
                play_mode.MAP = 'prairie_1'
                cx, cy = 3670, 860
                rx, ry = 890, 520
                rl, rb, rr, rt = 2100, 800, 3025, 990
            elif self.y > 2000:
                play_mode.MAP = 'lava_1'
                cx, cy = 3650, 2570
                rx, ry = 900, 500
                rl, rb, rr, rt = 3560, 1260, 3760, 2300
            self.combined_map_limit(cx, cy, rx, ry, rl, rb, rr, rt)

        elif play_mode.MAP == 'lava_1':
            if self.y < 1500:
                play_mode.MAP = 'prairie_2'
                cx, cy = 3670, 860
                rx, ry = 890, 520
                rl, rb, rr, rt = 3560, 1260, 3760, 2300
            elif self.x < 3000:
                play_mode.MAP = 'lava_2'
                cx, cy = 3650, 2570
                rx, ry = 900, 500
                rl, rb, rr, rt = 2100, 2450, 3025, 2550
            elif self.y > 2700:
                play_mode.MAP = 'lave_3'
                cx, cy = 3650, 2570
                rx, ry = 900, 500
                rl, rb, rr, rt = 3460, 2960, 3660, 3650
            self.combined_map_limit(cx, cy, rx, ry, rl, rb, rr, rt)
        elif play_mode.MAP == 'lava_2':
            if self.x > 3000:
                play_mode.MAP = 'lava_1'
                cx, cy = 3650, 2570
                rx, ry = 900, 500
                rl, rb, rr, rt = 3560, 1260, 3760, 2300
            elif self.x < 2300:
                play_mode.MAP = 'ice_1'
                cx, cy = 1200, 2500
                rx, ry = 900, 520
                rl, rb, rr, rt = 2000, 2450, 3025, 2550
            self.combined_map_limit(cx, cy, rx, ry, rl, rb, rr, rt)
        elif play_mode.MAP == 'lave_3':
            if self.y < 2500:
                play_mode.MAP = 'lava_1'
                cx, cy = 3650, 2570
                rx, ry = 900, 500
                rl, rb, rr, rt = 3560, 1260, 3760, 2300
            elif self.y > 3200:
                play_mode.MAP = 'cave_1'
                cx, cy = 3500, 4080
                rx, ry = 1000, 500
                rl, rb, rr, rt = 3460, 2960, 3660, 3650
            self.combined_map_limit(cx, cy, rx, ry, rl, rb, rr, rt)

        elif play_mode.MAP == 'ice_1':
            if self.x > 2300:
                play_mode.MAP = 'lava_2'
                cx, cy = 3650, 2570
                rx, ry = 900, 500
                rl, rb, rr, rt = 2100, 2450, 3025, 2550
            self.combined_map_limit(cx, cy, rx, ry, rl, rb, rr, rt)

        elif play_mode.MAP == 'cave_1':
            if self.y < 3500:
                play_mode.MAP = 'lave_3'
                cx, cy = 3650, 2570
                rx, ry = 900, 500
                rl, rb, rr, rt = 3460, 2960, 3660, 3650
            elif self.x < 2600:
                play_mode.MAP = 'cave_2'
                cx, cy = 3500, 4080
                rx, ry = 1000, 500
                rl, rb, rr, rt = 1800, 3950, 3025, 4150
            self.combined_map_limit(cx, cy, rx, ry, rl, rb, rr, rt)
        elif play_mode.MAP == 'cave_2':
            if self.x < 2300:
                play_mode.MAP = 'end_1'
                cx, cy = 1100, 4050
                rx, ry = 800, 420
                rl, rb, rr, rt = 1800, 3950, 3025, 4150
            elif self.y < 3800:
                play_mode.MAP = 'cave_1'
                cx, cy = 3500, 4080
                rx, ry = 1000, 500
                rl, rb, rr, rt = 3460, 2960, 3660, 3650
            self.combined_map_limit(cx, cy, rx, ry, rl, rb, rr, rt)

        elif play_mode.MAP == 'end_1':
            if self.x > 2300:
                play_mode.MAP = 'cave_1'
                cx, cy = 3500, 4080
                rx, ry = 1000, 500
                rl, rb, rr, rt = 1800, 3950, 3025, 4150
            self.combined_map_limit(cx, cy, rx, ry, rl, rb, rr, rt)

    def draw(self):
        self.state_machine.draw()
        draw_rectangle(*self.get_bb())

        # --- 화면 좌표 변환 ---
        cam_x = play_mode.camera_x
        cam_y = play_mode.camera_y

        # 1. 타원 그리기 (이전에 만든 함수 사용)
        self.draw_ellipse_debug(cx - cam_x, cy - cam_y, rx, ry)

        # 2. 사각형 그리기
        draw_rectangle(rl - cam_x, rb - cam_y, rr - cam_x, rt - cam_y)


    def handle_event(self, event):
        e = ('INPUT', event)
        # 마우스 왼쪽 클릭은 상태 전이와 무관하게 즉시 공격 생성
        if mouse_left_down(e):
            self.attack_()
        elif mouse_right_down(e):
            self.catch_()
        self.state_machine.handle_state_event(('INPUT', event))
        pass

    def catch_(self):
        catch = Catch(self.x - play_mode.camera_x +50, self.y-play_mode.camera_y, self.face_dir)
        game_world.add_object(catch, 1)
        game_world.add_collision_pair('slime:catch', None, catch)
        game_world.add_collision_pair('catch:plort', catch, None)
        pass

    def attack_(self):
        attack = Attack(self.x - play_mode.camera_x + self.face_dir * 40, self.y - play_mode.camera_y, self.face_dir)
        print("Attack!")
        game_world.add_object(attack, 1)
        game_world.add_collision_pair('slime:attack', None, attack)

    def ellipse_map_limit(self, ceneter_x, center_y, rx, ry):
        dx = self.x - ceneter_x
        dy = self.y - center_y
        distance = (dx**2) / (rx**2) + (dy**2) / (ry**2)

        if distance > 1.0:
            scale = 1 / math.sqrt(distance)
            self.x = ceneter_x + dx * scale
            self.y = center_y + dy * scale



    def combined_map_limit(self, cx, cy, rx, ry, rect_l, rect_b, rect_r, rect_t):
        # --- 1. 타원 내부 체크 ---
        dx = self.x - cx
        dy = self.y - cy
        # 타원 판별식: (x^2/a^2) + (y^2/b^2) <= 1 이면 내부
        ellipse_val = (dx ** 2) / (rx ** 2) + (dy ** 2) / (ry ** 2)

        if ellipse_val <= 1.0:
            return  # 타원 안에 있으므로 이동 허용 (종료)

        # --- 2. 사각형 내부 체크 ---
        # x가 left~right 사이이고, y가 bottom~top 사이인지 확인
        if rect_l <= self.x <= rect_r and rect_b <= self.y <= rect_t:
            return  # 사각형 안에 있으므로 이동 허용 (종료)

        # --- 3. 둘 다 벗어났을 때 (보정 로직) ---

        # (A) 타원 경계선 상의 가장 가까운 점(근사치) 구하기
        scale = 1 / math.sqrt(ellipse_val)
        ellipse_clamped_x = cx + dx * scale
        ellipse_clamped_y = cy + dy * scale

        # 플레이어와 타원 경계 사이의 거리 제곱
        dist_ellipse = (self.x - ellipse_clamped_x) ** 2 + (self.y - ellipse_clamped_y) ** 2

        # (B) 사각형 경계선 상의 가장 가까운 점 구하기 (Clamp)
        rect_clamped_x = max(rect_l, min(self.x, rect_r))
        rect_clamped_y = max(rect_b, min(self.y, rect_t))

        # 플레이어와 사각형 경계 사이의 거리 제곱
        dist_rect = (self.x - rect_clamped_x) ** 2 + (self.y - rect_clamped_y) ** 2

        # (C) 더 가까운 쪽으로 플레이어 위치 수정
        if dist_ellipse < dist_rect:
            self.x = ellipse_clamped_x
            self.y = ellipse_clamped_y
        else:
            self.x = rect_clamped_x
            self.y = rect_clamped_y

    def draw_ellipse_debug(self, cx, cy, rx, ry):
        for deg in range(0, 360, 10):
            rad = math.radians(deg)

            # 타원 좌표 공식
            # x = center_x + radius_x * cos(theta)
            # y = center_y + radius_y * sin(theta)
            x = cx + math.cos(rad) * rx
            y = cy + math.sin(rad) * ry

            draw_rectangle(x - 2, y - 2, x + 2, y + 2)


    def get_bb(self):
        sx = self.x - play_mode.camera_x
        sy = self.y - play_mode.camera_y
        return sx - 50, sy - 50, sx + 40, sy + 40

    def handle_collision(self, group, other):
        global collision_flag, collision_time
        if collision_flag == True:
            if group == 'player:slime':
                print("Player Hurt!")
                self.hp -= 10

                collision_flag = False
                collision_time = get_time()

                if self.hp <= 0:
                    self.state_machine.handle_state_event(('death', None))
                else:
                    self.state_machine.handle_state_event(('hurt', None))
        if group == 'player:slime_attack':
            self.hp -= 5
            if self.hp <= 0:
                self.state_machine.handle_state_event(('death', None))
            else:
                self.state_machine.handle_state_event(('hurt', None))
        pass
