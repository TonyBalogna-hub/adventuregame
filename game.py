"""Main game file for the Adventure Game.

This program runs a simple text-based RPG where the player can fight
monsters, rest to regain health, or quit the game. It imports functions
from gamefunctions.py and demonstrates loops, input validation, and
basic combat logic.
"""

import random
import gamefunctions

def fight_monster(player_hp: int, player_gold: int):
    """
    Handles a fight between the player and a random monster.

    Parameters:
        player_hp (int): The player's current health.
        player_gold (int): The player's current gold.

    Returns:
        tuple: (updated_hp, updated_gold)
    """
    monster = gamefunctions.random_monster()
    monster_hp = random.randint(10, 30)
    player_damage = random.randint(5, 10)
    monster_damage = random.randint(3, 8)

    print(f"You encounter a {monster} with {monster_hp} HP!")

    # Fight loop
    while player_hp > 0 and monster_hp > 0:
        print(f"\nYour HP: {player_hp} | {monster}'s HP: {monster_hp}")
        print("1) Attack")
        print("2) Run away")
        action = input("Choose an action: ")

        if action == "1":
            monster_hp -= player_damage
            print(f"You strike the {monster} for {player_damage} damage!")

            if monster_hp <= 0:
                print(f"You defeated the {monster}!")
                reward = random.randint(3, 8)
                player_gold += reward
                print(f"You earned {reward} gold.")
                break

            player_hp -= monster_damage
            print(f"The {monster} hits you for {monster_damage} damage!")

        elif action == "2":
            print("You ran away safely!")
            break
        else:
            print("Invalid choice. Try again.")

    if player_hp <= 0:
        print("You were defeated and wake up back in town...")
        player_hp = 20  # respawn health

    return player_hp, player_gold


def main():
    """Main game loop."""
    name = input("Enter your name, adventurer: ")
    gamefunctions.print_greeting(name)

    player_hp = 30
    player_gold = 10

    print("\nWelcome to the town!")

    # Main loop
    while True:
        print("\nYou are in town.")
        print(f"Current HP: {player_hp}, Current Gold: {player_gold}")
        print("1) Leave town (Fight Monster)")
        print("2) Sleep (Restore HP for 5 Gold)")
        print("3) Quit")

        choice = input("What would you like to do? ")

        if choice == "1":
            player_hp, player_gold = fight_monster(player_hp, player_gold)
        elif choice == "2":
            if player_gold >= 5:
                player_gold -= 5
                player_hp = 30
                print("You rest at the inn and restore your health.")
            else:
                print("Not enough gold to rest.")
        elif choice == "3":
            gamefunctions.print_farewell(name, player_gold)
            break
        else:
            print("Invalid option. Please choose 1, 2, or 3.")

if __name__ == "__main__":
    main()
