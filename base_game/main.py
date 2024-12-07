import time
import curses
import subprocess
from classes.Castle import Castle
from classes.character_manager import CharacterManager
from utils import clear_screen, display_ascii_art, typewriter_effect

is_paused = False


def pause_menu(stdscr):
    """Affiche le menu pause."""
    stdscr.clear()
    stdscr.addstr("=== Menu Pause ===\n")
    stdscr.addstr("1. Sauvegarder la partie\n")
    stdscr.addstr("2. Quitter le jeu\n")
    stdscr.addstr("3. Reprendre\n")
    stdscr.refresh()

    while True:
        key = stdscr.getkey()
        if key == "1":
            stdscr.addstr("Sauvegarde en cours...\n")
            stdscr.refresh()
            curses.napms(1000)  # Simule un délai
            return "resume"
        elif key == "2":
            return "quit"
        elif key == "3":
            return "resume"


# TODO: Gestion des utilisateurs, reprendre le module du projet multigame(python_game)
def options_menu(manager, stdcr):
    """Display the options menu."""
    print("1. Dificulty level\n2. Return to main menu")
    choice = input()

    while choice not in ["1", "2"]:
        print("Invalid choice. Please enter 1 or 2.")
        choice = input()
    if choice == "1":
        print("Choose difficulty level: ")
        print("1. Easy")
        print("2. Normal")
        print("3. Hard")
        print("4. Legendary")
        choice = input()
        tab = ["easy", "normal", "hard", "legendary"]
        choice = tab[int(choice) - 1]
        while choice not in ["1", "2", "3", "4"]:
            print("Invalid choice. Please enter 1 or 2 or 3 or 4.")
            choice = input()
    if choice == "2":
        main_menu(manager)


def main_menu(stdscr):
    """Display the main menu."""
    manager = CharacterManager()
    # display_ascii_art("base_game/Title.txt")
    # typewriter_effect("Welcome to Hyrule Castle!")
    stdscr.clear()
    stdscr.addstr("=== Menu Principal ===\n")
    stdscr.addstr("1. Lancer le jeu\n")
    stdscr.addstr("2. Quitter\n")
    stdscr.refresh()

    while True:
        key = stdscr.getkey()
        if key == "1":
            game_loop(manager, stdscr)
            break
        elif key == "2":
            options_menu(manager, stdscr)
        elif key == "3":
            break


def choice_action():
    """Define the action to take."""
    choice = 0
    while choice not in ["1", "2"]:
        print("---OPTIONS---- 1. Attack 2. Heal")
        choice = input()
    return int(choice)


def game_loop(manager, stdscr):
    """Main game loop."""
    curses.curs_set(0)  # Désactiver le curseur
    stdscr.clear()  # Nettoyer l'écran au début
    hyrule = Castle(10)
    boss_level = hyrule.nb_level
    manager.initialize_characters()
    player = manager.player

    # Afficher le personnage choisi
    stdscr.addstr(0, 0, f"Your character is: {player.name}")
    stdscr.refresh()
    curses.napms(1000)  # Pause de 1 seconde pour que l'utilisateur voie le message
    for i in range(1, boss_level + 1):
        stdscr.clear()
        manager.enemy.health = manager.enemy.max_health
        enemy = manager.enemy
        if i == boss_level:
            enemy = manager.boss
            manager.boss.health = manager.boss.health
            stdscr.addstr(0, 0, "You have reached the boss level!\n")
        else:
            stdscr.addstr(0, 0, f"========== FIGHT {i} ==========\n")
        stdscr.refresh()
        while enemy.health > 0 and player.health > 0:
            # Nettoyer les lignes pour éviter les résidus de texte
            clear_screen(stdscr)
            # Afficher les HP de l'ennemi
            enemy_hp = "I" * int(enemy.health)
            player_hp = "I" * int(player.health)
            stdscr.addstr(
                2,
                0,
                f"{enemy.name} HP: {enemy_hp} ({enemy.health}/{enemy.max_health})\n",
            )
            stdscr.addstr(
                3,
                0,
                f"{player.name} HP: {player_hp} ({player.health}/{player.max_health})\n",
            )
            stdscr.addstr(5, 0, "Choose an action: [1] Attack | [2] Heal\n")
            stdscr.refresh()
            curses.flushinp()
            try:
                choice = int(stdscr.getkey())  # Lire une touche et convertir en entier
            except ValueError:
                stdscr.addstr(6, 0, "Invalid input! Press 1 or 2.\n")
                stdscr.refresh()
                curses.napms(500)
                continue
            if choice == 1:
                player.attack(enemy)
                stdscr.refresh()
                stdscr.addstr(
                    8,
                    0,
                    f"{player.name} attacked {enemy.name} and deals {player.strength} damages !\n",
                )
                stdscr.refresh()
                curses.napms(500)
            elif choice == 2:
                player.self_heal()
                stdscr.addstr(8, 0, f"{player.name} used heal!\n")
                stdscr.refresh()
                curses.napms(500)
            else:
                stdscr.addstr(8, 0, "Invalid action! Try again.\n")
                stdscr.refresh()
                curses.napms(500)
                continue
            if enemy.health <= 0:
                if i < boss_level:
                    stdscr.move(8, 0)
                    stdscr.clrtoeol()
                    stdscr.refresh()
                    stdscr.addstr(
                        9, 0, f"{enemy.name} died! Moving to the next level.\n"
                    )
                    stdscr.refresh()
                    curses.napms(500)
                    break
                else:
                    stdscr.addstr(8, 0, "You defeated the boss! Congratulations!\n")
                    stdscr.refresh()
                    subprocess.Popen(
                        [
                            "mpg123",
                            "/srv/http/hyrule-castle/base_game/victory_8bit.mp3",
                        ],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                    )
                    curses.napms(2000)
                    return
            stdscr.refresh()
            curses.napms(500)
            enemy.attack(player)
            stdscr.addstr(
                9,
                0,
                f"{enemy.name} attacked {player.name} and deals {enemy.strength} damages !\n",
            )
            stdscr.refresh()
            if player.health <= 0:
                stdscr.addstr(9, 0, "You have been defeated. Game over.\n")
                stdscr.refresh()
                curses.napms(2000)
                return
        stdscr.refresh()
    stdscr.addstr(10, 0, "You have conquered Hyrule Castle!\n")
    stdscr.refresh()


def main():
    """Main function."""
    # main_menu(manager)
    curses.wrapper(main_menu)


def handle_exit():
    print("\nSaving your progress...")
    # @TODO: Ajouter une logique de sauvegarde
    print("Progress saved.")
    print("Goodbye, adventurer!")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        handle_exit()
