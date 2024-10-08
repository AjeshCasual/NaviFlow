import pyray as rl

class TrafficLight:
    def __init__(self, start_pos, end_pos, change_time=None):
        self.start_pos = start_pos  # Starting position of the line
        self.end_pos = end_pos        # Ending position of the line
        self.state = "red"           # Initial state
        self.timer = 0

        # Set default change times if not provided
        if change_time is None:
            self.change_time = {
                "red": 5,
                "yellow": 2,
                "green": 5
            }
        else:
            self.change_time = change_time

    def update(self):
        # Update the timer and change the light state if necessary
        self.timer += rl.get_frame_time()
        if self.timer >= self.change_time[self.state]:
            self.change_light()

    def change_light(self):
        # Cycle through the traffic light states
        if self.state == "red":
            self.state = "green"
        elif self.state == "green":
            self.state = "yellow"
        elif self.state == "yellow":
            self.state = "red"
        self.timer = 0  # Reset the timer

    def draw(self):
        # Determine the color based on the current state
        color_mapping = {
            "red": rl.RED,
            "yellow": rl.YELLOW,
            "green": rl.GREEN
        }
        
        # Draw the traffic light as a line segment
        color = color_mapping[self.state]
        rl.draw_line_ex(self.start_pos, self.end_pos,10, color)
