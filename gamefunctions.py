"""
gamefunctions.py

Contains utility functions for a simple text-based game. Provides functions 
for greeting, farewells, welcome messages, displaying a shop menu, purchasing 
items, and generating random monsters. Designed to be imported as a module.

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
