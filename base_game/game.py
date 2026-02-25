from base_game.classes.character_manager import CharacterManager
from base_game.menus.settings import GameSettings
from base_game.utils import clear_screen


class Game:

    def __init__(self):
        self.settings = GameSettings()
        self.manager = CharacterManager()

    def intro(self, stdscr):
        clear_screen(stdscr)
        stdscr.refresh()
        stdscr.addstr(4, 65, f"Bienvenue au château d'Hyrule.")
        stdscr.addstr(6, 40, f"Pour finir le jeu il faut battre le boss situé en haut de sa tour.")
        stdscr.addstr(7, 40, f"Pour arriver jusqu'à lui, pas mal d'épreuve vous attendent...")
        stdscr.addstr(8, 40, f"Vous trouverez sur votre passage des ennemis prêt a défendre leur tour à tout prix.")
        stdscr.addstr(9, 40, f"Heureusement vous avez avec vous votre épée, votre bouclier (bien qu'un peu usé) et des potions de soin.")
        stdscr.addstr(10, 40, f"Je peux que vous souhaiter bonne chance.")
        stdscr.addstr(12, 40, f"Appuyer pour continuer")
        stdscr.refresh()
        stdscr.getkey()

    def start(self, stdscr):
        self.intro(stdscr)
        self.manager.choose_player()
        player = self.manager.player
        clear_screen(stdscr)
        stdscr.addstr(4, 65, f"Vous incarnez {player.name}")
        stdscr.addstr(6, 65, f"Appuyer pour continuer")
        stdscr.refresh()
        stdscr.getkey()