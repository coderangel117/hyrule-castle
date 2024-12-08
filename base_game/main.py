import time
import curses
import subprocess
from classes.Castle import Castle
from classes.character_manager import CharacterManager
from utils import clear_screen, display_ascii_art, typewriter_effect


# TODO: Gestion des utilisateurs, reprendre le module du projet multigame(python_game)
is_paused = False


def pause_menu(manager, stdscr):
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


def options_menu(manager, stdscr):
    """Display the options menu."""
    stdscr.clear()
    stdscr.addstr("1. Difficulty level\n2. Return to main menu\n")
    stdscr.refresh()
    # Attendre une réponse valide
    while True:
        choice = stdscr.getkey()
        if choice == "1":
            stdscr.clear()
            stdscr.addstr("Choose difficulty level: \n")
            stdscr.addstr("1. Easy\n2. Normal\n3. Hard\n4. Legendary\n")
            stdscr.refresh()
            choice = stdscr.getkey()
            tab = ["easy", "normal", "hard", "legendary"]
            if choice in ["1", "2", "3", "4"]:
                choice = tab[int(choice) - 1]
                stdscr.addstr("You now playing on {} level".format(choice))
                stdscr.refresh()
                curses.napms(1000)
                stdscr.clear()
                main_menu(stdscr)
                break
            else:
                stdscr.addstr("Invalid choice. Please enter 1, 2, 3 or 4.\n")
                stdscr.refresh()
        elif choice == "2":
            stdscr.clear()
            main_menu(stdscr)
            break
        else:
            stdscr.addstr("Invalid choice. Please enter 1 or 2.\n")
            stdscr.refresh()


def main_menu(stdscr):
    """Display the main menu."""
    manager = CharacterManager()
    stdscr.addstr("=== Menu Principal ===\n")
    stdscr.addstr("1. Lancer le jeu\n")
    stdscr.addstr("2. Options\n")
    stdscr.addstr("3. Quitter\n")
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
            # Afficher les PV du joueur et de l'ennemi
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
            # Indiquer que c'est le tour du joueur
            stdscr.addstr(5, 0, "Your turn! [1] Attack | [2] Heal")
            stdscr.addstr(6, 0, "[>>> Waiting for input <<<]")  # Message dynamique
            stdscr.refresh()
            # Vider le buffer d'entrée
            curses.flushinp()

            key = stdscr.getkey()
            # Vérifier si la touche Échap a été pressée
            if key == "\x1b":  # '\x1b' est le code pour Échap
                pause_menu(manager, stdscr)
                stdscr.clear()
                break  # Reprendre là où on s'était arrêté

            stdscr.addstr(6, 0, " " * 30)  # Effacer le message "Waiting for input"
            stdscr.move(6, 0)
            # Actions du joueur
            if key == "1":
                player.attack(enemy)
                stdscr.addstr(
                    8,
                    0,
                    f"{player.name} attacked {enemy.name} and dealt {player.strength} damage!\n",
                )
            elif key == "2":
                player.self_heal()
                stdscr.addstr(8, 0, f"{player.name} used heal and regained health!\n")
                stdscr.refresh()
            else:
                stdscr.addstr(8, 0, "Invalid action! Try again.\n")
                stdscr.refresh()
                curses.napms(500)
                continue
            stdscr.refresh()
            curses.napms(500)
            if enemy.health <= 0:
                if i < boss_level:
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
            # L'ennemi attaque
            #
            stdscr.addstr(9, 0, f"{enemy.name} is attacking...\n")
            stdscr.refresh()
            curses.napms(300)
            stdscr.clrtoeol()
            enemy.attack(player)
            stdscr.addstr(
                9,
                0,
                f"{enemy.name} attacked {player.name} and dealt {enemy.strength} damage!\n",
            )
            stdscr.refresh()
            curses.napms(500)
            clear_screen(stdscr)
            curses.napms(500)
            if player.health <= 0:
                stdscr.addstr(10, 0, "You have been defeated. Game over.\n")
                stdscr.refresh()
                curses.napms(2000)
                return
        stdscr.refresh()
    stdscr.addstr(10, 0, "You have conquered Hyrule Castle!\n")
    stdscr.refresh()


def main():
    """Main function."""
    typewriter_effect("Welcome to")
    time.sleep(0.5)
    display_ascii_art("base_game/Title.txt")
    time.sleep(2)
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
