import pyray as rl
import math
from obstacles.car import Car
from obstacles.wall import Wall
from obstacles.light import TrafficLight
from obstacles.human import Human
import random
import player
# Initialize the Raylib window dimensions
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600




def main():
    # Initialize the Raylib window
    rl.init_window(WINDOW_WIDTH, WINDOW_HEIGHT, "Traffic Simulator")
    rl.set_target_fps(60)
    controllable_car = player.ControllableCar(position=[0, 250], speed=5)
    # Wall positions as specified
    wall_pos = [
        [(0,230),(280,230)],
        [(280,230),(280,0)],
        [(0,350),(280,350)],
        [(280,350),(280,600)],
        [(460,600),(460,450)],
        [(460,390),(460,350)],
        [(460,350),(520,350)],
        [(460,390),(520,350)],
        [(460,450),(590,350)],
        [(590,350),(710,350)],
        [(710,350),(710,600)],
        [(460,0),(460,230)],
        [(460,230),(630,230)],
        [(630,230),(630,0)],
        [(700,0),(700,230)],
        [(700,230),(800,230)],
        [(350,280),(375,255)],
        [(350,280),(375,310)],
        [(375,310),(400,280)],
        [(400,280),(375,255)]

    ]
    car_paths = [
    [(310, 600), (310, 320) , (0,320)],
    [(650,0),(650,230)],
    [(730,600),(730,330),(573,330),(440,430),(440,600)],
    [(0,250),(310,250),(375,200),(440,250),(800,250)]

]

    # Create walls from the positions
    walls = [Wall(positions) for positions in wall_pos]

    # Create some example objects
    cars = [Car(path, speed=random.randint(1,5), wait_time=1) for path in car_paths]
    traffic_lights = [
        TrafficLight((630,230), (700, 230)),
    ]
    humans = [
        Human((250,80),(480,80), speed=1, wait_time=2),
    ]

    # Main game loop
    while not rl.window_should_close():
        # Update
        for car in cars:
            car.update()
        for human in humans:
            human.update()
        for traffic_light in traffic_lights:
            traffic_light.update()

        # Draw
        rl.begin_drawing()
        rl.clear_background(rl.BLACK)

        # Draw walls
        for wall in walls:
            wall.draw()
        
        # Draw traffic lights
        for traffic_light in traffic_lights:
            traffic_light.draw()

        # Draw cars
        for car in cars:
            car.draw()

        # Draw humans
        for human in humans:
            human.draw()

        rl.end_drawing()

    # Close window and deallocate resources
    rl.close_window()

if __name__ == "__main__":
    main()
