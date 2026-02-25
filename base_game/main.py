import curses
import time

from base_game.classes.AudioManager import AudioManager
from base_game.menus.main_menu import MainMenu
from base_game.utils import display_ascii_art, handle_exit, typewriter_effect


def main():
    """Main function."""
    typewriter_effect("Bienvenue")
    time.sleep(0.5)
    display_ascii_art("base_game/assets/ascii/Title.txt")
    time.sleep(1)
    audio = AudioManager({
        "menu": "base_game/assets/music/menu.mp3",
        "dungeon": "base_game/assets/music/dungeon.mp3",
        "battle": "base_game/assets/music/battle.mp3",
        "boss_generic_1": "base_game/assets/music/boss_generic_1.mp3",
        "boss_generic_1": "base_game/assets/music/boss_generic_2.mp3",
        "mini_boss": "base_game/assets/music/mini_boss.mp3",
        "ganondorf": "base_game/assets/music/ganondorf.mp3",
        "victory": "base_game/assets/music/victory.mp3",
        "game_over": "base_game/assets/music/game_over.mp3"
    })
    menu = MainMenu(audio)
    try:
        curses.wrapper(menu.show)
    finally:
        audio.stop()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        handle_exit()