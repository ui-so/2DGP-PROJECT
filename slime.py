from pico2d import load_image, get_time

from state_machine import StateMachine

class MOVE:
    def __init__(self, player):
        self.player = player

    def enter(self, e):
        pass

    def exit(self, e):
        pass

    def do(self):
        self.player.frame = (self.player.frame + 1) % 6
        self.player.x += self.player.dir_x * 5
        self.player.y += self.player.dir_y * 5

    def draw(self):
        if self.player.face_dir == 1:  # right
            self.player.image.clip_draw(self.player.frame * 32, 0, 32, 32, self.player.x, self.player.y, 100, 100)
        else:  # face_dir == -1: # left
            self.player.image.clip_composite_draw(self.player.frame * 32, 0, 32, 32, 0, 'h', self.player.x, self.player.y, 100, 100)


class Attack:
    def __init__(self, player):
        self.player = player

    def enter(self, e):
        self.player.wait_start_time = get_time()

    def exit(self, e):
        pass

    def do(self):
        if get_time() - self.player.wait_start_time > 1.0:
            # IDLE 2초 경과, state machine에게 TIME_OUT 이벤트 전달
            self.player.state_machine.handle_state_event(('TIME_OUT', None))

    def draw(self):
        if self.player.face_dir == 1:  # right
            self.player.image.clip_draw(self.player.frame * 32, 0, 32, 32, self.player.x, self.player.y, 100, 100)
        else:  # face_dir == -1: # left
            self.player.image.clip_composite_draw(self.player.frame * 32, 0, 32, 32, 0, 'h', self.player.x, self.player.y, 100, 100)

        self.player.image.clip_draw(0, 0, 32, 32, self.player.x+32, self.player.y, 30, 30)


class SLIME:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.face_dir = 1
        self.dir_x = 0
        self.dir_y = 0
        self.image = load_image('Pink_Monster_Run_6.png')

        self.MOVE = MOVE(self)
        self.ATTACK = Attack(self)



    def update(self):
        self.state_machine.update()

    def draw(self):
        self.state_machine.draw()

    def handle_event(self, event):
        # 들어온 외부 키입력 등을 상태 머신에게 전달하기 위해서 튜플화 시킨 후, 전달
        self.state_machine.handle_state_event(('INPUT', event))
        pass
