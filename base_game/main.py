import curses
import time

from base_game.menus.main_menu import MainMenu
from base_game.utils import display_ascii_art, handle_exit, typewriter_effect


def main():
    """Main function."""
    typewriter_effect("Bienvenue")
    time.sleep(0.5)
    display_ascii_art("base_game/assets/Title.txt")
    time.sleep(1)
    menu = MainMenu()
    curses.wrapper(menu.show)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        handle_exit()
