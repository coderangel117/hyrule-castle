import curses
import subprocess

from base_game.classes.Castle import Castle
from base_game.menus.settings import GameSettings
from base_game.utils import clear_screen


class Game:

    def __init__(self):
        self.settings = GameSettings()

    def display_status(self, stdscr, enemy, player):
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

    def game_loop(self, manager, stdscr):
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
                self.display_status(stdscr, enemy, player)
                # Indiquer que c'est le tour du joueur
                stdscr.addstr(5, 0, "A vous de jouer ! [1] Attaquer | [2] Se soigner")
                # stdscr.addstr(6, 0, "[>>> En attente<<<]")  # Message dynamique
                stdscr.refresh()
                # Vider le buffer d'entrée
                curses.flushinp()

                try:
                    choice = int(stdscr.getkey())  # Lire une touche et convertir en entier
                except ValueError:
                    # stdscr.addstr(7, 0, "Invalid input! Press 1 or 2.\n")
                    stdscr.refresh()
                    curses.napms(500)
                    continue
                stdscr.addstr(6, 0, " " * 30)  # Effacer le message "Waiting for input"
                stdscr.move(6, 0)
                # Actions du joueur
                if choice == 1:
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
                                "/srv/http/hyrule-castle/base_game/assets/victory_8bit.mp3",
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
                            "/srv/http/hyrule-castle/base_game/assets/game_over.mp3",
                        ],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                    )
                    curses.napms(2000)
                    return
            stdscr.refresh()
        stdscr.refresh()
