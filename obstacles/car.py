import pyray as rl
import math


class Car:
    def __init__(self, positions, speed, wait_time):
        self.positions = positions
        self.speed = speed
        self.wait_time = wait_time
        self.frames_per_segment = []
        self.current_segment = 0
        self.frame = 0
        self.current_position = positions[0]
        self.calculate_frames_per_segment()
        self.is_waiting = False
        self.wait_frame = 0

    def calculate_frames_per_segment(self):
        for i in range(len(self.positions) - 1):
            p1 = self.positions[i]
            p2 = self.positions[i + 1]
            distance = math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)
            frames = max(1, int(distance / self.speed))
            self.frames_per_segment.append(frames)

    def update(self):
        if self.is_waiting:
            if self.wait_frame < self.wait_time * rl.get_fps():
                self.wait_frame += 1
            else:
                # Reset to the first segment after waiting
                self.is_waiting = False
                self.current_segment = 0
                self.frame = 0
                self.current_position = self.positions[0]  # Reset position to start

        else:
            if self.current_segment < len(self.frames_per_segment):
                if self.frame < self.frames_per_segment[self.current_segment]:
                    p1 = self.positions[self.current_segment]
                    p2 = self.positions[self.current_segment + 1]
                    alpha = self.frame / self.frames_per_segment[self.current_segment]
                    x = (1 - alpha) * p1[0] + alpha * p2[0]
                    y = (1 - alpha) * p1[1] + alpha * p2[1]
                    self.current_position = (x, y)
                    self.frame += 1
                else:
                    self.current_segment += 1
                    self.frame = 0

            # If we finished all segments, start waiting
            if self.current_segment >= len(self.frames_per_segment):
                self.is_waiting = True
                self.wait_frame = 0

    def draw(self):
        # Draw the car at the current position
        rl.draw_circle(int(self.current_position[0]), int(self.current_position[1]), 15, rl.DARKBLUE)

        # Draw the path taken by the car
        if len(self.positions) > 1:
            rl.draw_line_strip(self.positions, len(self.positions), rl.DARKBLUE)


