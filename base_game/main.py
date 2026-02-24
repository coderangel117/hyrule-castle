import time
import curses
import subprocess
from classes.Castle import Castle
from classes.character_manager import CharacterManager
from utils import clear_screen, display_ascii_art, handle_exit, typewriter_effect

is_paused = False
from pick import pick


def pause_menu(stdscr):
    """Affiche le menu pause."""
    stdscr.clear()
    title = "=== Menu Pause ==="
    options = ["Sauvegarder", "Quitter", "Reprendre le jeu"]
    _, choice = pick(options, title, screen=stdscr)
    stdscr.refresh()
    if choice == 0:
        stdscr.addstr("Sauvegarde en cours...\n")
        stdscr.refresh()
        curses.napms(1000)  # Simule un délai
        return "resume"
    elif choice == 1:
        return "quit"
    elif choice == 2:
        return "resume"
    else:
        return ""


# TODO: Gestion des utilisateurs, reprendre le module du projet multigame(python_game)
def options_menu(manager, stdscr):
    """Display the options menu."""
    stdscr.clear()
    options = ["Changer la difficulté", "Retourner au menu principal"]
    _, choice = pick(options, screen=stdscr)
    stdscr.refresh()
    if choice == 0:
        stdscr.clear()
        title = "Choisissez la difficulté"
        options = ["Facile", "Normal", "Difficile", "legendaire"]
        level, choice = pick(options, title, screen=stdscr)
        stdscr.refresh()
        stdscr.addstr("Vous jouez maintenant en difficulté {}".format(level))
        stdscr.refresh()
        curses.napms(1000)
        stdscr.clear()
        main_menu(stdscr)
    elif choice == 1:
        stdscr.clear()
        main_menu(stdscr)


def main_menu(stdscr):
    """Display the main menu."""
    manager = CharacterManager()
    title = "=== Menu Principal ==="
    options = ["Lancer le jeu", "Options", "Quitter"]
    _, index = pick(options, title, screen=stdscr)
    stdscr.refresh()
    if index == 0:
        game_loop(manager, stdscr)
    elif index == 1:
        options_menu(manager, stdscr)
    elif index == 2:
        pass


def choice_action(stdscr):
    """Define the action to take."""
    title = "---Choisissez votre action---"
    options = ["Attaquer", "Se soigner", "Fuir"]
    _, choice = pick(options, title, screen=stdscr)
    stdscr.refresh()
    return choice


def display_status(stdscr, enemy, player):
    enemy_hp = "❤️" * int(enemy.health)
    player_hp = "❤️" * int(player.health)
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
    stdscr.refresh()


def game_loop(manager, stdscr):
    """Main game loop."""
    curses.curs_set(0)  # Désactiver le curseur
    stdscr.clear()  # Nettoyer l'écran au début
    hyrule = Castle(10)
    boss_level = hyrule.nb_level
    manager.initialize_characters()
    player = manager.player
    stdscr.addstr(0, 0, f"Vous jouez: {player.name}")
    stdscr.refresh()
    curses.napms(1000)
    for i in range(1, boss_level + 1):
        stdscr.clear()
        manager.enemy.health = manager.enemy.max_health
        enemy = manager.enemy
        if i == boss_level:
            enemy = manager.boss
            manager.boss.health = manager.boss.health
            stdscr.addstr(0, 0, "Vous avez atteint l'étage du boss!\n")
        else:
            stdscr.addstr(0, 0, f"========== Combat {i} ==========\n")
        stdscr.refresh()
        while enemy.health > 0 and player.health > 0:
            clear_screen(stdscr)
            enemy_hp = "❤️" * int(enemy.health)
            player_hp = "❤️" * int(player.health)
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
            stdscr.refresh()
            curses.napms(2000)
            choice = choice_action(stdscr)
            stdscr.refresh()
            # Actions du joueur
            if choice == 0:
                player.attack(enemy)
                stdscr.addstr(
                    8,
                    0,
                    f"{player.name} attaque {enemy.name} and inflige {player.strength} de degats!\n",
                )
            elif choice == 1:
                player.self_heal()
                stdscr.addstr(8, 0, f"{player.name} utilise une potion et regagne des points de vie !\n")
                stdscr.refresh()
            elif choice == 2:
                stdscr.addstr(8, 0, f"Vous etes lache ! Vous vous  brisez la nuque dans les escalier en fuyant")
                stdscr.refresh()
                player.health = 0
            stdscr.refresh()
            curses.napms(500)
            if enemy.health <= 0:
                if i < boss_level:
                    stdscr.addstr(
                        9, 0, f"{enemy.name} est battu! Allez à l'étage suivant\n"
                    )
                    stdscr.refresh()
                    curses.napms(500)
                    break
                else:
                    stdscr.addstr(8, 0, "Vous avez battu le boss! Bravo!\n")
                    stdscr.refresh()
                    curses.napms(2000)
                    subprocess.Popen(
                        [
                            "mpg123",
                            "/srv/http/hyrule-castle/base_game/victory_8bit.mp3",
                        ],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                    )
                    return
            # L'ennemi attaque
            stdscr.addstr(9, 0, f"{enemy.name} attaque...\n")
            stdscr.refresh()
            curses.napms(500)
            stdscr.clrtoeol()
            enemy.attack(player)
            stdscr.addstr(
                9,
                0,
                f"{enemy.name} attaque {player.name} et inflige {enemy.strength} de degat!\n",
            )
            stdscr.refresh()
            curses.napms(500)
            clear_screen(stdscr)
            curses.napms(500)
            if player.health <= 0:
                stdscr.addstr(10, 0, "Vous avez perdu.\n")
                stdscr.refresh()
                subprocess.Popen(
                    [
                        "mpg123",
                        "/srv/http/hyrule-castle/base_game/game_over.mp3",
                    ],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
                curses.napms(2000)
                return
        stdscr.refresh()
    stdscr.refresh()


def main():
    """Main function."""
    typewriter_effect("Bienvenue")
    time.sleep(0.5)
    display_ascii_art("base_game/Title.txt")
    time.sleep(1)
    curses.wrapper(main_menu)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        handle_exit()
