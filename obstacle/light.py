import time

class TrafficLight:
    def __init__(self, red_duration=10, yellow_duration=2, green_duration=10):
        self.red_duration = red_duration
        self.yellow_duration = yellow_duration
        self.green_duration = green_duration
        self.current_state = 'RED'
        self.state_duration = {
            'RED': self.red_duration,
            'YELLOW': self.yellow_duration,
            'GREEN': self.green_duration
        }
        self.last_switch_time = time.time()

    def switch_state(self):
        current_time = time.time()
        if current_time - self.last_switch_time >= self.state_duration[self.current_state]:
            if self.current_state == 'RED':
                self.current_state = 'GREEN'
            elif self.current_state == 'GREEN':
                self.current_state = 'YELLOW'
            elif self.current_state == 'YELLOW':
                self.current_state = 'RED'
            self.last_switch_time = current_time

    def get_state(self):
        self.switch_state()
        return self.current_state


traffic_light = TrafficLight()
while True:
    print(traffic_light.get_state())
    time.sleep(1)
