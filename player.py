
import pyray as rl
import math

class ControllableCar:
    def __init__(self, position, speed):
        self.position = position
        self.speed = speed
        self.angle = 0  # In degrees

    def update(self):
        # Handle input for movement
        if rl.is_key_down(rl.KEY_W):  # Move forward
            self.position[0] += self.speed * math.cos(math.radians(self.angle))
            self.position[1] += self.speed * math.sin(math.radians(self.angle))
        if rl.is_key_down(rl.KEY_S):  # Move backward
            self.position[0] -= self.speed * math.cos(math.radians(self.angle))
            self.position[1] -= self.speed * math.sin(math.radians(self.angle))
        if rl.is_key_down(rl.KEY_A):  # Turn left
            self.angle += 2  # Change this value for speed of turning
        if rl.is_key_down(rl.KEY_D):  # Turn right
            self.angle -= 2  # Change this value for speed of turning

    def draw(self):
        # Draw the car as a rectangle (or any shape you prefer)
        car_width = 20
        car_height = 10
        # Calculate the car's corner positions based on angle
        points = [
            (self.position[0] + car_width / 2 * math.cos(math.radians(self.angle)) - car_height / 2 * math.sin(math.radians(self.angle)),
             self.position[1] + car_width / 2 * math.sin(math.radians(self.angle)) + car_height / 2 * math.cos(math.radians(self.angle))),
            (self.position[0] - car_width / 2 * math.cos(math.radians(self.angle)) - car_height / 2 * math.sin(math.radians(self.angle)),
             self.position[1] - car_width / 2 * math.sin(math.radians(self.angle)) + car_height / 2 * math.cos(math.radians(self.angle))),
            (self.position[0] - car_width / 2 * math.cos(math.radians(self.angle)) + car_height / 2 * math.sin(math.radians(self.angle)),
             self.position[1] - car_width / 2 * math.sin(math.radians(self.angle)) - car_height / 2 * math.cos(math.radians(self.angle))),
            (self.position[0] + car_width / 2 * math.cos(math.radians(self.angle)) + car_height / 2 * math.sin(math.radians(self.angle)),
             self.position[1] + car_width / 2 * math.sin(math.radians(self.angle)) - car_height / 2 * math.cos(math.radians(self.angle))),
        ]
        # Draw the car
        rl.draw_polygon(points, rl.DARKBLUE)
