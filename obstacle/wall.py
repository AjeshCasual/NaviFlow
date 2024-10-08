import pyray as rl


class Wall:
    def __init__(self, positions):
        self.positions = positions
    def draw(self):
        if len(self.positions) > 1:
            rl.draw_line_strip(self.positions, len(self.positions), rl.BLACK)