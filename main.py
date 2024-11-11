import pyray as rl
import neat
import random
from obstacles.car import Car
from obstacles.wall import Wall
from obstacles.light import TrafficLight
from obstacles.human import Human
import player

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

def eval_genomes(genomes, config):
    """
    Evaluates each genome in the population by running the simulation and calculating its fitness.
    """
    for genome_id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)

        # Initialize the controllable car with a small positive speed
        controllable_car = player.ControllableCar(position=[0, 250], speed=5)

        # Create the paths for the obstacles (cars, walls, etc.)
        car_paths = [
            [(310, 600), (310, 320), (0, 320)],
            [(650, 0), (650, 230)],
            [(730, 600), (730, 330), (573, 330), (440, 430), (440, 600)],
            [(0, 250), (310, 250), (375, 200), (440, 250), (800, 250)],
        ]
        cars = [Car(path, speed=random.randint(1, 5), wait_time=1) for path in car_paths]
        traffic_lights = [TrafficLight((630, 230), (700, 230))]
        humans = [Human((250, 80), (480, 80), speed=1, wait_time=2)]
        walls = [Wall(positions) for positions in [
            [(0, 230), (280, 230)],
            [(280, 230), (280, 0)],
            [(0, 350), (280, 350)],
            [(280, 350), (280, 600)],
            [(460, 600), (460, 450)],
            [(460, 390), (460, 350)],
            [(460, 350), (520, 350)],
            [(460, 390), (520, 350)],
            [(460, 450), (590, 350)],
            [(590, 350), (710, 350)],
            [(710, 350), (710, 600)],
            [(460, 0), (460, 230)],
            [(460, 230), (630, 230)],
            [(630, 230), (630, 0)],
            [(700, 0), (700, 230)],
            [(700, 230), (800, 230)],
            [(350, 280), (375, 255)],
            [(350, 280), (375, 310)],
            [(375, 310), (400, 280)],
            [(400, 280), (375, 255)],
            [(0,0),(0,600)],
            [(0,600),(800,600)],
            [(800,600),(800,0)],
            [(800,0),(0,0)]
        ]]

        max_fitness = -float('inf')
        penalty = 0  # Initialize penalty here

        # Run the simulation for 300 frames
        for _ in range(60):
            for car in cars:
                car.update()
            for human in humans:
                human.update()
            for traffic_light in traffic_lights:
                traffic_light.update()

            # Gather sensor data and pass it to the neural network
            sensor_data = get_sensor_data(controllable_car, cars, walls, traffic_lights, humans)
            output = net.activate(sensor_data)

            steer, throttle, brake, reverse = output

            # Apply the throttle and steering to the car
            controllable_car.steer(steer)
            controllable_car.throttle(throttle)

            # Update the car's position
            controllable_car.update()

            # Check for collisions and apply penalties
            for obstacle in cars + walls + humans:
                if controllable_car.check_collision(obstacle):
                    penalty += 1  # Penalty for collision (you can adjust this value)

            # Calculate fitness as the distance the car has traveled minus the penalty
            fitness = controllable_car.position[0] - penalty
            if fitness > max_fitness:
                max_fitness = fitness

        genome.fitness = max_fitness


def get_sensor_data(controllable_car, cars, walls, traffic_lights, humans):
    """
    Gathers the sensor data for the controllable car.
    """
    x, y = controllable_car.position
    speed = controllable_car.speed
    angle = controllable_car.angle

    # Sensor data includes the car's position, speed, angle, and distance to the nearest obstacle
    sensor_data = [
        x,  # Car's x position
        y,  # Car's y position
        speed,  # Speed of the car
        angle,  # Angle/direction of the car
        get_nearest_obstacle_distance(controllable_car, cars, walls, traffic_lights, humans)  # Nearest obstacle distance
    ]

    return sensor_data


def get_nearest_obstacle_distance(controllable_car, cars, walls, traffic_lights, humans):
    """
    Returns the distance to the nearest obstacle (car, wall, traffic light, or human).
    """
    min_distance = float('inf')
    for obstacle in cars + walls + traffic_lights + humans:
        distance = controllable_car.get_distance_to(obstacle)
        min_distance = min(min_distance, distance)
    
    return min_distance


def run_neat(config):
    """
    Runs the NEAT algorithm with the given configuration.
    """
    population = neat.Population(config)
    population.add_reporter(neat.StdOutReporter(True))
    population.add_reporter(neat.Checkpointer(5))

    winner = population.run(eval_genomes, 1)
    return winner


def main():
    rl.init_window(WINDOW_WIDTH, WINDOW_HEIGHT, "Traffic Simulator with NEAT")
    rl.set_target_fps(60)

    # Load the NEAT configuration
    config_path = "config-feedforward.cfg"
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    winner = run_neat(config)
    print("Winner genome:", winner)

    net = neat.nn.FeedForwardNetwork.create(winner, config)
    controllable_car = player.ControllableCar(position=[30, 250], speed=0.1)  # Non-zero initial speed

    # Create the obstacles
    walls = [Wall(positions) for positions in [
        [(0, 230), (280, 230)],
        [(280, 230), (280, 0)],
        [(0, 350), (280, 350)],
        [(280, 350), (280, 600)],
        [(460, 600), (460, 450)],
        [(460, 390), (460, 350)],
        [(460, 350), (520, 350)],
        [(460, 390), (520, 350)],
        [(460, 450), (590, 350)],
        [(590, 350), (710, 350)],
        [(710, 350), (710, 600)],
        [(460, 0), (460, 230)],
        [(460, 230), (630, 230)],
        [(630, 230), (630, 0)],
        [(700, 0), (700, 230)],
        [(700, 230), (800, 230)],
        [(350, 280), (375, 255)],
        [(350, 280), (375, 310)],
        [(375, 310), (400, 280)],
        [(400, 280), (375, 255)],
    ]]

    cars = [Car(path, speed=random.randint(1, 5), wait_time=1) for path in [
        [(310, 600), (310, 320), (0, 320)],
        [(650, 0), (650, 230)],
        [(730, 600), (730, 330), (573, 330), (440, 430), (440, 600)],
        [(0, 250), (310, 250), (375, 200), (440, 250), (800, 250)],
    ]]

    traffic_lights = [TrafficLight((630, 230), (700, 230))]
    humans = [Human((250, 80), (480, 80), speed=1, wait_time=2)]

    penalty = 0  # Initialize penalty here for main game loop

    # Main game loop
    while not rl.window_should_close():
        for car in cars:
            car.update()
        for human in humans:
            human.update()
        for traffic_light in traffic_lights:
            traffic_light.update()

        # Get the sensor data and use the neural network to control the car
        sensor_data = get_sensor_data(controllable_car, cars, walls, traffic_lights, humans)
        output = net.activate(sensor_data)

        steer, throttle, brake, reverse = output
        controllable_car.steer(steer)
        controllable_car.throttle(throttle)

        # Check for collisions and apply penalties
        for obstacle in cars + walls + humans:
            if controllable_car.check_collision(obstacle):
                penalty += 1  # Penalty for collision (you can adjust this value)

        # Update the car’s position
        controllable_car.update()

        # Draw everything
        rl.begin_drawing()
        rl.clear_background(rl.LIGHTGRAY)

        for car in cars:
            car.draw()
        for wall in walls:
            wall.draw()
        for human in humans:
            human.draw()
        for traffic_light in traffic_lights:
            traffic_light.draw()
        controllable_car.draw()

        rl.end_drawing()

    rl.close()


if __name__ == "__main__":
    main()
