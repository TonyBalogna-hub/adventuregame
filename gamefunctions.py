"""
Main game file for the Adventure Game.

This version includes saving and loading your game using JSON,
plus wandering monsters, a map, inventory, shop, and combat.
"""

import random
import json
import os
import pygame
from wanderingMonster import WanderingMonster

class NPC:
    def __init__(self, name, position, dialogue, item=None):
        self.name = name
        self.position = position  # (x, y) tuple
        self.dialogue = dialogue
        self.item = item  # Optional item dict

    def interact(self, player):
        print(f"\n{self.name} says: '{self.dialogue}'")
        if self.item:
            print(f"{self.name} gives you a {self.item['name']}!")
            player['inventory'].append(self.item)
            self.item = None  # Remove item after giving


MAP_FILE = "map_state.json"

# ---------------------------------------------------
# Player management
# ---------------------------------------------------
def create_player():
    return {
        "name": "",
        "hp": 30,
        "gold": 10,
        "damage": 5,
        "inventory": [],
        "equipped_weapon": None
    }

# ---------------------------------------------------
# Save and Load Game
# ---------------------------------------------------
def save_game(player, filename="savegame.json"):
    data = {
        "name": player["name"],
        "hp": player["hp"],
        "gold": player["gold"],
        "damage": player["damage"],
        "inventory": player["inventory"],
        "equipped_weapon": (
            player["equipped_weapon"]["name"]
            if player["equipped_weapon"] else None
        )
    }
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)
    print(f"\nGame saved to {filename}!\n")

def load_game(filename="savegame.json"):
    if not os.path.exists(filename):
        print("No save file found.")
        return None

    with open(filename, "r") as f:
        data = json.load(f)

    weapon_name = data["equipped_weapon"]
    data["equipped_weapon"] = None

    if weapon_name:
        for item in data["inventory"]:
            if item["name"] == weapon_name:
                data["equipped_weapon"] = item
                break

    return data

# ---------------------------------------------------
# Map state persistence
# ---------------------------------------------------
def load_map_state():
    if os.path.exists(MAP_FILE):
        with open(MAP_FILE, "r") as f:
            return json.load(f)
    else:
        return {"player_pos": [0, 0], "monsters": []}

def save_map_state(state):
    with open(MAP_FILE, "w") as f:
        json.dump(state, f)

# ---------------------------------------------------
# Combat
# ---------------------------------------------------
def random_monster():
    return {
        "name": random.choice(["Goblin", "Orc", "Troll", "Dragon", "Zombie"]),
        "hp": random.randint(10, 20),
        "damage": random.randint(2, 7)
    }

def fight_monster(player):
    monster = random_monster()
    mhp = monster["hp"]
    mdmg = monster["damage"]
    print(f"\nA {monster['name']} appears! HP: {mhp} | Damage: {mdmg}")

    while mhp > 0 and player["hp"] > 0:
        print(f"\nYour HP: {player['hp']}")
        action = input("(A)ttack, (R)un: ").lower()
        if action == "r":
            print("You ran away!")
            return

        for item in player["inventory"]:
            if item["type"] == "special" and item["effect"] == "auto_kill":
                print("Your Monster Charm activates! The monster dies instantly!")
                player["inventory"].remove(item)
                mhp = 0
                break

        if mhp <= 0:
            break

        dmg = player["damage"]
        if player["equipped_weapon"]:
            dmg += player["equipped_weapon"]["damage_bonus"]
            player["equipped_weapon"]["currentDurability"] -= 1
            if player["equipped_weapon"]["currentDurability"] <= 0:
                print(f"Your {player['equipped_weapon']['name']} broke!")
                player["inventory"].remove(player["equipped_weapon"])
                player["equipped_weapon"] = None

        mhp -= dmg
        print(f"You hit the {monster['name']} for {dmg} damage!")

        if mhp <= 0:
            break

        player["hp"] -= mdmg
        print(f"The monster hits you for {mdmg} damage!")

    if player["hp"] <= 0:
        print("\nYou died!")
        exit()

    gold_gain = random.randint(5, 20)
    player["gold"] += gold_gain
    print(f"\nYou defeated the monster and earned {gold_gain} gold!")

# ---------------------------------------------------
# Inventory and equipment
# ---------------------------------------------------
def show_inventory(player):
    print("\n=== Inventory ===")
    if not player["inventory"]:
        print("Your inventory is empty.")
        return

    for i, item in enumerate(player["inventory"], 1):
        if item["type"] == "weapon":
            print(f"{i}. {item['name']} (Damage +{item['damage_bonus']}, Durability {item['currentDurability']}/{item['maxDurability']})")
        elif item["type"] == "special":
            print(f"{i}. {item['name']} (Special Item)")
        else:
            print(f"{i}. {item['name']}")

    print("\nE. Equip a weapon\nX. Exit inventory")
    choice = input("Choose an option: ")
    if choice.lower() == "e":
        equip_weapon(player)
    else:
        print("Closing inventory...")

def equip_weapon(player):
    print("\n=== Equip Weapon ===")
    weapons = [item for item in player["inventory"] if item["type"] == "weapon"]
    if not weapons:
        print("No weapons in inventory.")
        return
    for i, weapon in enumerate(weapons, 1):
        print(f"{i}. {weapon['name']} (+{weapon['damage_bonus']} dmg)")
    try:
        idx = int(input("Choose weapon number: "))
        if 1 <= idx <= len(weapons):
            player["equipped_weapon"] = weapons[idx - 1]
            print(f"You equipped {weapons[idx - 1]['name']}!")
        else:
            print("Invalid choice.")
    except ValueError:
        print("Invalid input.")

# ---------------------------------------------------
# Shop
# ---------------------------------------------------
def shop(player):
    print("\n=== Game Shop ===")
    print("1. Sword (50 gold) – Weapon +5 dmg, 10 durability")
    print("2. Monster Charm (40 gold) – One-use instant kill")
    print("3. Exit shop")

    choice = input("Choose item: ")

    if choice == "1":
        if player["gold"] >= 50:
            player["gold"] -= 50
            item = {
                "name": "Sword",
                "type": "weapon",
                "damage_bonus": 5,
                "maxDurability": 10,
                "currentDurability": 10
            }
            player["inventory"].append(item)
            print("You bought a Sword!")
        else:
            print("Not enough gold.")

    elif choice == "2":
        if player["gold"] >= 40:
            player["gold"] -= 40
            item = {
                "name": "Monster Charm",
                "type": "special",
                "effect": "auto_kill"
            }
            player["inventory"].append(item)
            print("You bought a Monster Charm!")
        else:
            print("Not enough gold.")
    else:
        print("Leaving shop...")

# ---------------------------------------------------
# Rest
# ---------------------------------------------------
def rest(player):
    print("You take a rest... +10 HP")
    player["hp"] += 10

# ---------------------------------------------------
# Wandering Monster Combat
# ---------------------------------------------------
def fight_wandering_monster(player, monster):
    print(f"\nA {monster.name} appears! HP: 20 | Damage: 5")
    monster_hp = 20
    monster_dmg = 5

    while monster_hp > 0 and player["hp"] > 0:
        print(f"\nYour HP: {player['hp']}")
        action = input("(A)ttack, (R)un: ").lower()
        if action == "r":
            print("You ran away!")
            return

        for item in player["inventory"]:
            if item["type"] == "special" and item["effect"] == "auto_kill":
                print("Your Monster Charm activates! The monster dies instantly!")
                player["inventory"].remove(item)
                monster_hp = 0
                break

        if monster_hp <= 0:
            break

        dmg = player["damage"]
        if player["equipped_weapon"]:
            dmg += player["equipped_weapon"]["damage_bonus"]
            player["equipped_weapon"]["currentDurability"] -= 1
            if player["equipped_weapon"]["currentDurability"] <= 0:
                print(f"Your {player['equipped_weapon']['name']} broke!")
                player["inventory"].remove(player["equipped_weapon"])
                player["equipped_weapon"] = None

        monster_hp -= dmg
        print(f"You hit the {monster.name} for {dmg} damage!")

        if monster_hp <= 0:
            break

        player["hp"] -= monster_dmg
        print(f"The {monster.name} hits you for {monster_dmg} damage!")

    if player["hp"] <= 0:
        print("\nYou died!")
        exit()

    player["gold"] += monster.gold
    print(f"\nYou defeated the {monster.name} and earned {monster.gold} gold!")

# ---------------------------------------------------
# Run map
# ---------------------------------------------------
npcs = [
    NPC("Old Man", (3, 3), "Beware the forest! Take this potion.", {"name": "Health Potion", "type": "special", "effect": "heal"}),
    NPC("Merchant", (6, 7), "I sell rare items. Visit my shop!")
]
def run_map(state, player):
    GRID_WIDTH = 10
    GRID_HEIGHT = 10
    TILE = 32
    TOWN_LOC = (0, 0)

    pygame.init()
    screen = pygame.display.set_mode((GRID_WIDTH * TILE, GRID_HEIGHT * TILE))
    clock = pygame.time.Clock()
    running = True

    px, py = state["player_pos"]
    player_move_count = 0

    # Load monsters
    monsters = []
    if state.get("monsters"):
        for m in state["monsters"]:
            mon = WanderingMonster(GRID_WIDTH, GRID_HEIGHT, TOWN_LOC, m["name"])
            mon.x, mon.y = m["pos"]
            monsters.append(mon)
    else:
        monsters = WanderingMonster.spawn_monsters(2, GRID_WIDTH, GRID_HEIGHT, TOWN_LOC)

    action = None

    while running:
        screen.fill((0, 0, 0))
        for x in range(GRID_WIDTH):
            for y in range(GRID_HEIGHT):
                pygame.draw.rect(screen, (50, 50, 50), (x * TILE, y * TILE, TILE, TILE), 1)

        pygame.draw.circle(screen, (0, 255, 0), (TOWN_LOC[0] * TILE + TILE // 2, TOWN_LOC[1] * TILE + TILE // 2), TILE // 2 - 2)

        for mon in monsters:
            pygame.draw.circle(screen, mon.color, (mon.x * TILE + TILE // 2, mon.y * TILE + TILE // 2), TILE // 2 - 2)

        for npc in npcs:
            pygame.draw.rect(screen, (255, 255, 0), (npc.position[0]*TILE, npc.position[1]*TILE, TILE, TILE))

        pygame.draw.rect(screen, (0, 0, 255), (px, py, TILE, TILE))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                action = "quit"
                running = False
            elif event.type == pygame.KEYDOWN:
                moved = False
                if event.key == pygame.K_UP and py > 0:
                    py -= TILE
                    moved = True
                elif event.key == pygame.K_DOWN and py < (GRID_HEIGHT - 1) * TILE:
                    py += TILE
                    moved = True
                elif event.key == pygame.K_LEFT and px > 0:
                    px -= TILE
                    moved = True
                elif event.key == pygame.K_RIGHT and py < (GRID_WIDTH - 1) * TILE:
                    px += TILE
                    moved = True

                if moved:
                    player_move_count += 1
                    if player_move_count % 2 == 0:
                        for mon in monsters:
                            mon.move()

                player_tile = (px // TILE, py // TILE)

                # Check for NPC interaction
                for npc in npcs:
                    if player_tile == npc.position:
                        npc.interact(player)

                # Check if player returned to town
                if player_tile == TOWN_LOC:
                    action = "town"
                    running = False
                else:
                    # Check for monsters
                    for mon in monsters[:]:
                        if player_tile == mon.position():
                            fight_wandering_monster(player, mon)
                            monsters.remove(mon)

        # Respawn monsters if none left
        if not monsters:
            monsters = WanderingMonster.spawn_monsters(2, GRID_WIDTH, GRID_HEIGHT, TOWN_LOC)

        clock.tick(10)

    pygame.quit()
    state["player_pos"] = [px // TILE, py // TILE]
    state["monsters"] = [{"name": m.name, "pos": m.position()} for m in monsters]
    save_map_state(state)
    return action, state



# ---------------------------------------------------
# Main Game
# ---------------------------------------------------
def main():
    print("=== Adventure Game ===")

    print("1. New Game")
    print("2. Load Game")
    start_choice = input("> ")

    if start_choice == "2":
        player = load_game()
        if player:
            print(f"Welcome back, {player['name']}!")
        else:
            print("No save file found. Starting a new game instead.")
            player = create_player()
            player["name"] = input("Enter your name: ")
    else:
        player = create_player()
        player["name"] = input("Enter your name: ")

    map_state = load_map_state()

    while True:
        print("\n=== Town Menu ===")
        print("1. Leave town (Explore Map)")
        print("2. Fight a monster directly")
        print("3. Rest")
        print("4. Shop")
        print("5. Inventory")
        print("6. Save and Quit")

        choice = input("> ")

        if choice == "1":
            action, map_state = run_map(map_state, player)
            if action == "town":
                print("You returned to town.")
            elif action == "quit":
                print("Game exited abruptly.")
                break

        elif choice == "2":
            fight_monster(player)
        elif choice == "3":
            rest(player)
        elif choice == "4":
            shop(player)
        elif choice == "5":
            show_inventory(player)
        elif choice == "6":
            save_game(player)
            print("Goodbye!")
            break
        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()
