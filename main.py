import pyray as rl
from obstacles.car import Car
from obstacles.wall import Wall
from obstacles.light import TrafficLight
from obstacles.human import Human
import ctypes

def main():
    rl.init_window(800, 600, "Traffic Simulator Editor")
    rl.set_target_fps(60)

    obstacles = []
    obstacle_types = ["Car", "Wall", "Traffic Light", "Human"]
    
    # Create an integer pointer for the combo box index
    obstacle_type_index = ctypes.c_int(0)

    # Default parameters
    car_positions = [(100, 100), (200, 200)]
    human_start = (300, 300)
    human_end = (400, 400)
    speed = 5
    wait_time = 2
    traffic_light_start = (500, 300)
    traffic_light_end = (500, 350)

    while not rl.window_should_close():
        # Update
        for obstacle in obstacles:
            if isinstance(obstacle, Car):
                obstacle.update()
            elif isinstance(obstacle, TrafficLight):
                obstacle.update()
            elif isinstance(obstacle, Human):
                obstacle.update()

        # GUI Drawing
        rl.begin_drawing()
        rl.clear_background(rl.RAYWHITE)

        # Draw obstacles
        for obstacle in obstacles:
            obstacle.draw()

        # GUI elements
        obstacle_type_index = rl.gui_combo_box((10, 10, 150, 20), "Obstacle Type:", obstacle_types, obstacle_type_index.value)

        if rl.is_mouse_button_pressed(rl.MOUSE_LEFT_BUTTON):
            selected_type = obstacle_types[obstacle_type_index.value]
            if selected_type == "Car":
                obstacles.append(Car(car_positions, speed, wait_time))
            elif selected_type == "Wall":
                wall_positions = [(100, 100), (150, 150)]  # Example positions
                obstacles.append(Wall(wall_positions))
            elif selected_type == "Traffic Light":
                obstacles.append(TrafficLight(traffic_light_start, traffic_light_end))
            elif selected_type == "Human":
                obstacles.append(Human(human_start, human_end, speed, wait_time))

        rl.end_drawing()

    rl.close_window()

if __name__ == "__main__":
    main()
