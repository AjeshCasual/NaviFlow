import pyray as rl
import math

class Human:
    def __init__(self, start_position, end_position, speed, wait_time):
        self.start_position = start_position
        self.end_position = end_position
        self.speed = speed
        self.wait_time = wait_time
        self.distance = math.sqrt((end_position[0] - start_position[0]) ** 2 + (end_position[1] - start_position[1]) ** 2)
        self.frames = max(1, int(self.distance / self.speed))
        self.current_position = start_position
        self.frame = 0
        self.wait_frame = 0
        self.is_waiting = False

    def update(self):
        if self.is_waiting:
            if self.wait_frame < self.wait_time * rl.get_fps():
                self.wait_frame += 1
            else:
                self.is_waiting = False
                self.frame = 0
                self.current_position = self.start_position

        else:
            if self.frame < self.frames:
                alpha = self.frame / self.frames
                x = (1 - alpha) * self.start_position[0] + alpha * self.end_position[0]
                y = (1 - alpha) * self.start_position[1] + alpha * self.end_position[1]
                self.current_position = (x, y)
                self.frame += 1
            else:
                self.is_waiting = True
                self.wait_frame = 0

    def draw(self):
        rl.draw_circle(int(self.current_position[0]), int(self.current_position[1]), 20, rl.DARKBLUE)
        rl.draw_line_ex(self.start_position,self.end_position,4,rl.DARKBLUE)

