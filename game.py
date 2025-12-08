"""
Main game file for the Adventure Game.

This version includes saving and loading your game using JSON.
"""

import random
import json
import os
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
# SAVE GAME
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


# ---------------------------------------------------
# LOAD GAME
# ---------------------------------------------------
def load_game(filename="savegame.json"):
    if not os.path.exists(filename):
        print("No save file found.")
        return None

    with open(filename, "r") as f:
        data = json.load(f)

    print("\nSave file loaded!")

    # Fix equipped weapon reference
    weapon_name = data["equipped_weapon"]
    data["equipped_weapon"] = None

    if weapon_name:
        for item in data["inventory"]:
            if item["name"] == weapon_name:
                data["equipped_weapon"] = item
                break

    return data


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
# Show inventory
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

    print("\nE. Equip a weapon")
    print("X. Exit inventory")

    choice = input("Choose an option: ")

    if choice.lower() == "e":
        equip_weapon(player)
    else:
        print("Closing inventory...")


# ---------------------------------------------------
# Equip a weapon
# ---------------------------------------------------
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
# Fight monster
# ---------------------------------------------------
def fight_monster(player):
    monster = gamefunctions.random_monster()
    mhp = monster["hp"]
    mdmg = monster["damage"]

    print(f"\nA {monster['name']} appears!")
    print(f"HP: {mhp} | Damage: {mdmg}")

    while mhp > 0 and player["hp"] > 0:
        print(f"\nYour HP: {player['hp']}")
        action = input("(A)ttack, (R)un: ").lower()

        if action == "r":
            print("You ran away!")
            return

        # Check auto-kill item
        for item in player["inventory"]:
            if item["type"] == "special" and item["effect"] == "auto_kill":
                print("Your Monster Charm activates! The monster dies instantly!")
                player["inventory"].remove(item)
                mhp = 0
                break

        if mhp <= 0:
            break

        # Player attack
        dmg = player["damage"]
        if player["equipped_weapon"]:
            dmg += player["equipped_weapon"]["damage_bonus"]
            player["equipped_weapon"]["currentDurability"] -= 1

            # Weapon breaks
            if player["equipped_weapon"]["currentDurability"] <= 0:
                print(f"Your {player['equipped_weapon']['name']} broke!")
                player["inventory"].remove(player["equipped_weapon"])
                player["equipped_weapon"] = None

        mhp -= dmg
        print(f"You hit the {monster['name']} for {dmg} damage!")

        if mhp <= 0:
            break

        # Monster attacks back
        player["hp"] -= mdmg
        print(f"The monster hits you for {mdmg} damage!")

    if player["hp"] <= 0:
        print("\nYou died!")
        exit()

    gold_gain = random.randint(5, 20)
    player["gold"] += gold_gain
    print(f"\nYou defeated the monster and earned {gold_gain} gold!")


# ---------------------------------------------------
# Rest
# ---------------------------------------------------
def rest(player):
    print("You take a rest... +10 HP")
    player["hp"] += 10


# ---------------------------------------------------
# Main game loop
# ---------------------------------------------------
def main():
    print("=== Adventure Game ===")

    # Load or New Game
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


    # Main loop
    while True:
        print("\n=== Main Menu ===")
        print("1. Fight a monster")
        print("2. Rest")
        print("3. Shop")
        print("4. Inventory")
        print("5. Save and Quit")

        choice = input("> ")

        if choice == "1":
            fight_monster(player)
        elif choice == "2":
            rest(player)
        elif choice == "3":
            shop(player)
        elif choice == "4":
            show_inventory(player)
        elif choice == "5":
            save_game(player)
            print("Goodbye!")
            break
        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()
