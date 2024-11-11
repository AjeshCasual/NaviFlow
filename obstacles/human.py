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
        self.moving_to_end = True  # Track direction of movement

    def update(self):
        if self.is_waiting:
            if self.wait_frame < self.wait_time * rl.get_fps():
                self.wait_frame += 1
            else:
                self.is_waiting = False
                self.frame = 0  # Reset frame counter
                # Toggle the direction for the next move
                self.moving_to_end = not self.moving_to_end

        else:
            if self.frame < self.frames:
                if self.moving_to_end:
                    alpha = self.frame / self.frames
                    x = (1 - alpha) * self.start_position[0] + alpha * self.end_position[0]
                    y = (1 - alpha) * self.start_position[1] + alpha * self.end_position[1]
                else:
                    alpha = self.frame / self.frames
                    x = (1 - alpha) * self.end_position[0] + alpha * self.start_position[0]
                    y = (1 - alpha) * self.end_position[1] + alpha * self.start_position[1]
                
                self.current_position = (x, y)
                self.frame += 1
            else:
                self.is_waiting = True  # Start waiting after reaching the end
                self.wait_frame = 0  # Reset wait frame

    def draw(self):
        rl.draw_circle(int(self.current_position[0]), int(self.current_position[1]), 15, rl.YELLOW)

        rl.draw_line_ex(self.start_position,self.end_position,1,rl.YELLOW)

