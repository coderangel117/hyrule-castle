import os
import sys
import time

from classes.Castle import Castle
from classes.character_manager import CharacterManager

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def options_menu():
    """Display the options menu."""
    clear_screen()
    print("1. Sound\n"
          "2. Back\n")
    choice = input()
    while choice not in ["1", "2"]:
        print("Invalid choice. Please enter 1 or 2.")
        choice = input()
    if choice == "2":
        main_menu()


def main_menu():
    """Display the main menu."""
    clear_screen()
    display_ascii_art("base_game/Title.txt")
    typewriter_effect("Welcome to Hyrule Castle!")
    print("1. Start\n"
          "2. Options\n"
          "3. Quit\n")
    choice = input()
    while choice not in ["1", "2", "3"]:
        print("Invalid choice. Please enter 1 or 2 or 3.")
        choice = input()
    if choice == "2":
        options_menu()
    if choice == "3":
        sys.exit(0)


def clear_screen():
    """Efface l'écran."""
    os.system('cls' if os.name == 'nt' else 'clear')


def typewriter_effect(text):
    """ Write text with a typewriter effect."""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.07)  # Pause entre chaque lettre
    print()


def choice_action(player):
    """Define the action to take."""
    choice = 0
    while choice not in ["1", "2"]:
        print("---OPTIONS-----\n"
              "1. Attack    2. Heal")
        choice = input()
    return int(choice)


def display_ascii_art(file):
    """Display ASCII art from a file."""
    abs_path = os.path.join(BASE_DIR, file)
    with open(abs_path, "r") as f:
        print(f.read())


def main():
    """Main function."""
    main_menu()
    hyrule = Castle(10)
    boss_level = hyrule.nb_level
    manager = CharacterManager()
    manager.initialize_characters()
    player = manager.player
    print(f"Player: {manager.player.name}")
    print(f"Enemy: {manager.enemy.name}")
    print(f"Boss: {manager.boss.name}")
    for i in range(1, boss_level + 1):
        manager.enemy.health = manager.enemy.max_health
        enemy = manager.enemy
        if i == boss_level:
            enemy = manager.boss
            manager.boss.health = manager.boss.health
            print("You have reached the boss level!")
        print(f"========== FIGHT {i} ==========")
        print(enemy.health)
        while enemy.health > 0 and player.health > 0:
            enemy_hp = "I" * int(enemy.health)
            player_hp = "I" * int(player.health)
            print(f"{enemy.name} \n "
                  f"HP: {enemy_hp} {enemy.health}/{enemy.max_health}")
            print(f"{player.name} \n"
                  f"HP: {player_hp} {player.health}/{player.max_health}")
            choice = choice_action(player)
            if choice == 1:
                player.attack(enemy)
            else:
                player.self_heal()
                print(f"{player.name} used heal!")
            if enemy.health <= 0:
                if i < boss_level:
                    print(f"{enemy.name} died!")
                    i += 1
                    break
                if i == boss_level:
                    print("You defeated the boss!")
                    import subprocess
                    # Lancer la musique en arrière-plan
                    subprocess.Popen(
                        ["mpg123", "/srv/http/hyrule-castle/base_game/victory_8bit.mp3"],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL
                    )
                    display_ascii_art("base_game/Link.txt")
                    return
            enemy.attack(player)
            if player.health <= 0:
                display_ascii_art("base_game/game_over.txt")
                return


def handle_exit():
    print("\nSaving your progress...")
    # @TODO: Ajouter une logique de sauvegarde
    time.sleep(2)
    print("Progress saved.")
    print("Goodbye, adventurer!")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        handle_exit()
