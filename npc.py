class NPC:
    def __init__(self, name, position, dialogue, item=None):
        self.name = name
        self.position = position  # tuple (x, y)
        self.dialogue = dialogue  # string to show when interacting
        self.item = item          # optional item dict

    def interact(self, player):
        print(f"\n{self.name} says: '{self.dialogue}'")
        if self.item:
            print(f"{self.name} gives you a {self.item['name']}!")
            player['inventory'].append(self.item)
            self.item = None  # remove item after giving
