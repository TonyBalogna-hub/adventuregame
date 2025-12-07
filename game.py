"""Main game file for the Adventure Game.

This program runs a simple text-based RPG where the player can fight
monsters, rest to regain health, or quit the game. It imports functions
from gamefunctions.py and demonstrates loops, input validation, and
basic combat logic.
"""

import random
import gamefunctions

# ---------------------------------------------------
# Create player with stats and inventory
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
# Shop functionality
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
            item = {"name": "Monster Charm", "type": "special", "effect": "auto_kill"}
            player["inventory"].append(item)
            print("You bought a Monster Charm!")
        else:
            print("Not enough gold.")
    else:
        print("Leaving shop...")

# ---------------------------------------------------
# Show inventory
# ---------------------------------------------------
def show_inventory(player):
    print("\n=== Inventory ===")
    if not player["inventory"]:
        print("Inventory is empty.\n")
        return
    for item in player["inventory"]:
        if item["type"] == "weapon":
            print(f"{item['name']} (Weapon, {item['currentDurability']} durability)")
        elif item["type"] == "special":
            print(f"{item['name']} (Special Item)")
        else:
            print(f"{item['name']} ({item['type']})")
    print()

# ---------------------------------------------------
# Equip weapon
# ---------------------------------------------------
def equip_weapon(player):
    weapons = [i for i in player["inventory"] if i["type"] == "weapon"]
    if not weapons:
        print("\nYou have no weapons to equip.\n")
        return
    print("\n=== Equip Weapon ===")
    for i, w in enumerate(weapons, start=1):
        print(f"{i}. {w['name']} ({w['currentDurability']} durability)")
    choice = input("Choose weapon number: ")
    if not choice.isdigit():
        print("Invalid input.")
        return
    idx = int(choice) - 1
    if 0 <= idx < len(weapons):
        player["equipped_weapon"] = weapons[idx]
        print(f"You equipped the {weapons[idx]['name']}!")
    else:
        print("Invalid selection.")

# ---------------------------------------------------
# Fight monster
# ---------------------------------------------------
def fight_monster(player):
    print("\nA monster attacks!")
    # Check for Monster Charm
    for item in player["inventory"]:
        if item["type"] == "special" and item["effect"] == "auto_kill":
            use = input("Use Monster Charm for instant kill? (y/n): ")
            if use.lower() == "y":
                print("You used the Monster Charm! Monster destroyed instantly!")
                player["inventory"].remove(item)
                return

    # Normal fight
    monster_hp = random.randint(10, 20)
    print(f"Monster HP: {monster_hp}")
    weapon = player["equipped_weapon"]
    dmg = player["damage"] + (weapon["damage_bonus"] if weapon else 0)

    while monster_hp > 0:
        monster_hp -= dmg
        print(f"You hit for {dmg}!")
        if monster_hp <= 0:
            print("Monster defeated!")
            if weapon:
                weapon["currentDurability"] -= 1
                print(f"{weapon['name']} durability is now {weapon['currentDurability']}")
                if weapon["currentDurability"] <= 0:
                    print("Your weapon breaks!")
                    player["inventory"].remove(weapon)
                    player["equipped_weapon"] = None
            gold_reward = random.randint(5, 15)
            player["gold"] += gold_reward
            print(f"You earned {gold_reward} gold.")
            return
        # Monster hits back
        monster_attack = random.randint(3, 8)
        player["hp"] -= monster_attack
        print(f"Monster hits you for {monster_attack} damage!")
        if player["hp"] <= 0:
            print("You were defeated and wake up back in town...")
            player["hp"] = 30
            return

# ---------------------------------------------------
# Main loop
# ---------------------------------------------------
def main():
    player = create_player()
    player["name"] = input("Enter your name, adventurer: ")
    gamefunctions.print_greeting(player["name"])
    print("\nWelcome to the town!")

    while True:
        print(f"\nHP: {player['hp']} | Gold: {player['gold']}")
        print("1. Go to Shop")
        print("2. Show Inventory")
        print("3. Equip Weapon")
        print("4. Fight Monster")
        print("5. Sleep (Restore HP for 5 Gold)")
        print("6. Quit")

        choice = input("Choose an action: ")
        if choice == "1":
            shop(player)
        elif choice == "2":
            show_inventory(player)
        elif choice == "3":
            equip_weapon(player)
        elif choice == "4":
            fight_monster(player)
        elif choice == "5":
            if player["gold"] >= 5:
                player["gold"] -= 5
                player["hp"] = 30
                print("You rested and restored your health.")
            else:
                print("Not enough gold to rest.")
        elif choice == "6":
            gamefunctions.print_farewell(player["name"], player["gold"])
            break
        else:
            print("Invalid choice. Please select 1-6.")

if __name__ == "__main__":
    main()
