class Wall:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def is_point_inside(self, x, y):
        return self.x1 <= x <= self.x2 and self.y1 <= y <= self.y2

wall = Wall(10, 10, 20, 20)
print(wall.is_point_inside(15, 15))  # True
print(wall.is_point_inside(25, 25))  # False
