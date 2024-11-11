import pyray as rl
import math
import random
from obstacles.car import Car  # Import Car class
from obstacles.wall import Wall  # Import Wall class
from obstacles.light import TrafficLight  # Import TrafficLight class
from obstacles.human import Human  # Import Human class

class ControllableCar:
    def __init__(self, position, speed=1, angle=random.randint(0,3)):
        self.position = position  # (x, y)
        self.speed = speed  # Start with a speed > 0 so the car is not still
        self.angle = angle  # Direction in radians (0 is pointing right)
        self.max_steer_angle = math.pi / 4  # Max steering angle (45 degrees)
        self.max_speed = 10  # Max speed of the car

    def steer(self, steer_input):
        """
        Adjusts the steering angle of the car based on input.
        steer_input: float in the range [-1, 1], where 1 is maximum right and -1 is maximum left.
        """
        self.angle += steer_input * self.max_steer_angle

    def throttle(self, throttle_input):
        """
        Adjusts the speed of the car based on throttle input.
        throttle_input: float in the range [-1, 1], where 1 is full throttle (forward)
                        and -1 is full reverse.
        """
        if throttle_input > 0:
            # Accelerating forward
            self.speed = min(self.max_speed, self.speed + throttle_input * 2)  # Accelerate forward
        elif throttle_input < 0:
            # Reversing
            self.speed = max(-self.max_speed, self.speed + throttle_input * 2)  # Reverse

    def update(self):
        """
        Updates the car's position based on the current speed and angle.
        """
        dx = self.speed * math.cos(self.angle)
        dy = self.speed * math.sin(self.angle)
        self.position = (self.position[0] + dx, self.position[1] + dy)

    def draw(self):
        """
        Draws the car on the screen at its current position.
        """
        rl.draw_circle(int(self.position[0]), int(self.position[1]), 15, rl.GREEN)

    def get_distance_to(self, obstacle):
        """
        Computes the distance between the car and an obstacle.
        Handles different types of obstacles (Car, Wall, TrafficLight, Human).
        """
        x1, y1 = self.position
        if isinstance(obstacle, Car):  # If the obstacle is a car, use its current position
            x2, y2 = obstacle.current_position
        elif isinstance(obstacle, Wall):  # If the obstacle is a Wall, use the closest point from the wall's positions
            min_distance = float('inf')
            for (x2, y2) in obstacle.positions:
                distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
                min_distance = min(min_distance, distance)
            return min_distance
        elif isinstance(obstacle, TrafficLight):  # If the obstacle is a traffic light, use its position
            x2, y2 = obstacle.start_pos
        elif isinstance(obstacle, Human):  # If the obstacle is a human, use its position
            x2, y2 = obstacle.start_position
        else:
            raise ValueError("Unknown obstacle type")

        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    def check_collision(self, obstacle):
        """
        Checks if the car collides with an obstacle (Car, Wall, or Human).
        Returns True if the obstacle is within a collision distance, False otherwise.
        """
        collision_distance = 15  # Adjust based on the sizes of the obstacles
        distance = self.get_distance_to(obstacle)
        return distance < collision_distance
