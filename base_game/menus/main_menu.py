from pick import pick

from base_game.classes.character_manager import CharacterManager
from base_game.game import Game
from base_game.menus.options_menu import OptionsMenu


class MainMenu:
    def __init__(self):
        self.game = Game()
    def show(self, stdscr):
        while True:
            manager = CharacterManager()
            title = "=== Menu Principal ==="
            options = ["Lancer le jeu", "Options", "Quitter"]
            _, index = pick(options, title, screen=stdscr)
            stdscr.refresh()
            if index == 0:
                self.game.game_loop()
            elif index == 1:
                OptionsMenu.show(self, stdscr)
            elif index == 2:
                return "Quit"
