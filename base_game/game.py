import curses
from collections import namedtuple

from base_game.classes.Player import Player
from base_game.classes.character_manager import CharacterManager
from base_game.menus.settings import GameSettings
from base_game.utils import clear_screen


class Game:

    def __init__(self, audio):
        self.settings = GameSettings()
        self.manager = CharacterManager()
        self.audio = audio
        self.is_running = False
        self.player = Player("", 0, 0, 0, 0)
        self.player = namedtuple("Player", "name, health, max_health, strength, defense")

    def show_intro(self, stdscr, lines, title=None, delay_ms=0):
        clear_screen(stdscr)
        h, w = stdscr.getmaxyx()
        block = []
        if title:
            block.append(title)
            block.append("")
        block.extend(lines)
        block.append("")
        block.append("Appuie sur une touche pour continuer…")

        y = max(0, (h - len(block)) // 2)

        for i, line in enumerate(block):
            x = max(0, (w - len(line)) // 2)
            stdscr.addstr(y + i, x, line)
            stdscr.refresh()
            if delay_ms > 0:
                curses.napms(delay_ms)
        stdscr.getch()

    def intro(self, stdscr):
        self.audio.play("menu")
        lines = [
            "Bienvenue au château d'Hyrule.",
            "",
            "Pour finir le jeu, tu dois reprendre le contrôle du Château d'Hyrule.",
            "",
            "Pour y arriver, des épreuves t'attendent à chaque salle…",
            "",
            "Ennemis, pièges, coffres, marchands : reste sur tes gardes.",
            "",
            "Mais vous avez votre épée, votre bouclier et quelques potions.",
            "",
            "Bonne chance, héros.",
        ]
        clear_screen(stdscr)
        self.show_intro(stdscr, lines, delay_ms=120)
        self.audio.stop()

    def choose_character(self, stdscr):
        players = self.manager.get_players()
        screen_h, screen_w = stdscr.getmaxyx()
        start_y = (screen_h // 2) - (12 // 2)
        start_x = (screen_w // 2) - (35 // 2)
        selected_index = 0
        while True:
            stdscr.clear()
            stdscr.addstr(start_y -2, start_x + 4, f"Choisissez votre personnage")
            stdscr.refresh()
            self.manager.display_player_card(stdscr, players[selected_index], start_y, start_x)
            key = stdscr.getkey()
            if key == "KEY_UP":
                selected_index = (selected_index - 1) % len(players)
            elif key == "KEY_DOWN":
                selected_index = (selected_index + 1) % len(players)
            elif key == "\n":
                return players[selected_index]

    def start(self, stdscr):
        self.intro(stdscr)
        self.manager.choose_player()
        clear_screen(stdscr)
        stdscr.addstr(10, 65, f"Choisissez votre personnage")
        stdscr.refresh()
        self.player = self.choose_character(stdscr)
        stdscr.clear()
        stdscr.addstr(4, 65, f"Vous incarnez {self.player['name']}")
        stdscr.addstr(6, 65, f"Appuyer pour continuer")
        stdscr.refresh()
        stdscr.getkey()
