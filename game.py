"""Main game file for the Adventure Game.

This program imports functions from gamefunctions.py and provides a basic
interactive game experience for the player. It demonstrates module import,
function calls, and user interaction.

Typical usage example:
    python game.py
"""

import gamefunctions

def main():
    """Run a simple game using functions from gamefunctions.py."""
    print("=== Welcome to the Adventure Game! ===\n")

    # Ask for player's name
    name = input("Enter your name, brave adventurer: ")
    gamefunctions.print_greeting(name)

    # Show shop menu
    print("\nHere’s what’s available in the shop today:")
    gamefunctions.print_shop_menu("Sword", 50, "Shield", 40)

    # Example gold amount
    gold = 100
    print(f"\nYou have {gold} gold.\n")

    # Try purchasing something
    choice = input("What would you like to buy (1 for Sword, 2 for Shield, or 0 for nothing)? ")

    if choice == "1":
        gold = gamefunctions.purchase_item("Sword", 50, gold)
    elif choice == "2":
        gold = gamefunctions.purchase_item("Shield", 40, gold)
    else:
        print("Maybe next time!")

    print(f"\nYou now have {gold} gold remaining.")

    # Random monster encounter
    print("\nAs you leave the shop...")
    monster = gamefunctions.random_monster()

    # Farewell
    gamefunctions.print_farewell(name, 150)
    print("\n=== Game Over ===")

if __name__ == "__main__":
    main()
