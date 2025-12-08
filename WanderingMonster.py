import random

class WanderingMonster:
    def __init__(self, grid_width, grid_height, town_location, name=None):
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.town_location = town_location  # (x, y)
        self.name = name if name else self.random_name()
        self.color = self.assign_color()
        self.gold = random.randint(5, 20)
        self.x, self.y = self.random_position()

    def random_name(self):
        return random.choice(["Zombie", "Slime", "Goblin", "Orc"])

    def assign_color(self):
        colors = {
            "Zombie": (255, 0, 0),
            "Slime": (0, 255, 0),
            "Goblin": (255, 255, 0),
            "Orc": (128, 0, 128)
        }
        return colors.get(self.name, (255, 255, 255))

    def random_position(self):
        while True:
            x = random.randint(0, self.grid_width - 1)
            y = random.randint(0, self.grid_height - 1)
            if (x, y) != self.town_location:
                return x, y

    def move(self):
        directions = [(0,1),(0,-1),(1,0),(-1,0)]
        random.shuffle(directions)
        for dx, dy in directions:
            new_x = self.x + dx
            new_y = self.y + dy
            if 0 <= new_x < self.grid_width and 0 <= new_y < self.grid_height:
                if (new_x, new_y) != self.town_location:
                    self.x, self.y = new_x, new_y
                    break

    def position(self):
        return self.x, self.y
