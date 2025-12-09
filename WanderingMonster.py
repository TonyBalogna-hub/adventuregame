# wanderingMonster.py
import random

class WanderingMonster:
    def __init__(self, grid_width, grid_height, town_location, name=None):
        """
        Initializes a wandering monster on the map.

        Parameters:
            grid_width (int): Width of the grid.
            grid_height (int): Height of the grid.
            town_location (tuple): Coordinates of the town (x, y).
            name (str, optional): Specific monster name. If None, random.
        """
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.town_location = town_location
        self.name = name if name else self.random_name()
        self.color = self.assign_color()
        self.gold = random.randint(5, 20)
        self.x, self.y = self.random_position()

    def random_name(self):
        return random.choice(["Zombie", "Slime", "Goblin", "Orc", "Troll"])

    def assign_color(self):
        """Assign a color based on monster type."""
        colors = {
            "Zombie": (255, 0, 0),
            "Slime": (0, 255, 0),
            "Goblin": (255, 255, 0),
            "Orc": (128, 0, 128),
            "Troll": (0, 128, 128)
        }
        return colors.get(self.name, (255, 255, 255))

    def random_position(self):
        """Return a random position not on the town."""
        while True:
            x = random.randint(0, self.grid_width - 1)
            y = random.randint(0, self.grid_height - 1)
            if (x, y) != self.town_location:
                return x, y

    def move(self):
        """Attempt to move the monster one tile in a random direction, avoiding town."""
        directions = [(0,1), (0,-1), (1,0), (-1,0)]  # down, up, right, left
        random.shuffle(directions)
        for dx, dy in directions:
            new_x = self.x + dx
            new_y = self.y + dy
            if 0 <= new_x < self.grid_width and 0 <= new_y < self.grid_height:
                if (new_x, new_y) != self.town_location:
                    self.x, self.y = new_x, new_y
                    break

    def position(self):
        """Return the current position of the monster."""
        return self.x, self.y

    @staticmethod
    def spawn_monsters(count, grid_width, grid_height, town_location):
        """Create a list of WanderingMonster instances."""
        monsters = []
        for _ in range(count):
            monsters.append(WanderingMonster(grid_width, grid_height, town_location))
        return monsters
