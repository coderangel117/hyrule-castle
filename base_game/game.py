import curses

from base_game.classes.AudioManager import AudioManager
from base_game.classes.character_manager import CharacterManager
from base_game.menus.settings import GameSettings
from base_game.utils import clear_screen


class Game:

    def __init__(self, audio):
        self.settings = GameSettings()
        self.manager = CharacterManager()
        self.audio = audio
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

    def start(self, stdscr):
        self.intro(stdscr)
        self.manager.choose_player()
        player = self.manager.player
        clear_screen(stdscr)
        stdscr.addstr(4, 65, f"Vous incarnez {player.name}")
        stdscr.addstr(6, 65, f"Appuyer pour continuer")
        stdscr.getkey()
