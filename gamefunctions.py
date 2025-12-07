"""
gamefunctions.py

Functions:
    print_greeting(player_name)
    print_farewell(player_name, score)
    print_welcome(name, width)
    print_shop_menu(item1Name, item1Price, item2Name, item2Price)
    purchase_item(item_name, item_price, player_gold)
    random_monster()
"""

import random

# ---------------------------------------------------
# Function 1: print_greeting
# ---------------------------------------------------
def print_greeting(player_name: str) -> None:
    """
    Prints a personalized greeting message for the player.

    Parameters:
        player_name (str): The name of the player to greet.

    Returns:
        None
    """
    print(f"Hello, {player_name}! Welcome to the adventure.")


# ---------------------------------------------------
# Function 2: print_farewell
# ---------------------------------------------------
def print_farewell(player_name: str, score: int) -> None:
    """
    Prints a farewell message showing the player's name and score.

    Parameters:
        player_name (str): The name of the player.
        score (int): The player's final score.

    Returns:
        None
    """
    print(f"Goodbye, {player_name}! Your final score was {score}.")


# ---------------------------------------------------
# Function 3: print_welcome
# ---------------------------------------------------
def print_welcome(name: str, width: int) -> None:
    """
    Prints a welcome message centered within a specified width.

    Parameters:
        name (str): The name of the person to welcome.
        width (int): The total width of the printed output.

    Returns:
        None
    """
    message = f"Hello, {name}!"
    print(f"'{message.center(width)}'")


# ---------------------------------------------------
# Function 4: print_shop_menu
# ---------------------------------------------------
def print_shop_menu(item1Name: str, item1Price: float, item2Name: str, item2Price: float) -> None:
    """
    Prints a shop menu listing two items and their corresponding prices.

    Parameters:
        item1Name (str): Name of the first item.
        item1Price (float): Price of the first item.
        item2Name (str): Name of the second item.
        item2Price (float): Price of the second item.

    Returns:
        None
    """
    item_field = 12
    price_field = 8

    line1 = f"| {item1Name.ljust(item_field)}${item1Price:>{price_field - 1}.2f} |"
    line2 = f"| {item2Name.ljust(item_field)}${item2Price:>{price_field - 1}.2f} |"

    border_length = len(line1) - 2
    top_border = f"/{'-' * border_length}\\"
    bottom_border = f"\\{'-' * border_length}/"

    print(top_border)
    print(line1)
    print(line2)
    print(bottom_border)


# ---------------------------------------------------
# Function 5: purchase_item
# ---------------------------------------------------
def purchase_item(item_name: str, item_price: float, player_gold: float) -> float:
    """
    Deducts the item price from the player's gold if affordable.

    Parameters:
        item_name (str): Name of the item to purchase.
        item_price (float): Price of the item.
        player_gold (float): The player's current gold.

    Returns:
        float: Updated amount of gold after purchase.

    Example:
        >>> purchase_item('Sword', 50, 100)
        You purchased Sword for $50.00. Gold left: $50.00
        50.0
    """
    if player_gold >= item_price:
        player_gold -= item_price
        print(f"You purchased {item_name} for ${item_price:.2f}. Gold left: ${player_gold:.2f}")
    else:
        print(f"Not enough gold to purchase {item_name}. You have ${player_gold:.2f}")
    return player_gold


# ---------------------------------------------------
# Function 6: random_monster
# ---------------------------------------------------
def random_monster() -> str:
    """
    Returns the name of a random monster.

    Returns:
        str: The name of a randomly selected monster.

    Example:
        >>> random_monster()
        'Goblin'
    """
    monsters = ["Goblin", "Orc", "Troll", "Dragon", "Zombie"]
    monster = random.choice(monsters)
    print(f"A wild {monster} appears!")
    return monster


# ---------------------------------------------------
# Test client
# ---------------------------------------------------
def test_functions() -> None:
    """Runs test cases for all module functions."""
    print_greeting("Antonio")
    print_greeting("Bob")
    print_greeting("Billy")
    print()

    print_farewell("Antonio", 100)
    print_farewell("Bob", 250)
    print_farewell("Billy", 50)
    print()

    print_welcome("Antonio", 20)
    print_welcome("Bob", 30)
    print_welcome("Billy", 25)
    print()

    print_shop_menu("Apple", 31, "Pear", 1.234)
    print()
    print_shop_menu("Egg", 0.23, "Bag of Oats", 12.34)
    print()
    print_shop_menu("Milk", 2.5, "Cheese", 15.75)
    print()

    gold = 100
    gold = purchase_item("Sword", 50, gold)
    gold = purchase_item("Shield", 60, gold)
    print()

    random_monster()
    random_monster()


# Run test client if module is executed directly
if __name__ == "__main__":
    test_functions()

# ======================================================
# NEW FUNCTIONS FOR ASSIGNMENT 10
# ======================================================

def create_player():
    """Create a player with starting stats and inventory."""
    return {
        "hp": 30,
        "gold": 999,    # enough money for testing
        "damage": 5,
        "inventory": [],
        "equipped_weapon": None
    }


def shop(player):
    """Allow the player to purchase items from the shop."""
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


def show_inventory(player):
    """Display all items in the player's inventory."""
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


def equip_weapon(player):
    """Allow the player to equip a weapon from their inventory."""
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


def fight_monster(player):
    """Handle fighting a monster, including using weapons or special items."""
    print("\nA monster attacks!")

    # Check for special item first
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

            # Reduce weapon durability if equipped
            if weapon:
                weapon["currentDurability"] -= 1
                print(f"{weapon['name']} durability is now {weapon['currentDurability']}")
                if weapon["currentDurability"] <= 0:
                    print("Your weapon breaks!")
                    player["inventory"].remove(weapon)
                    player["equipped_weapon"] = None
            return
