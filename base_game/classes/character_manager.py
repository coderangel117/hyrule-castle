import json
import os

from .Boss import Boss
from .Enemy import Enemy
from .Player import Player
from ..menus.settings import GameSettings

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class CharacterManager:
    """Manage character selection for player, enemies, and bosses."""
    settings = GameSettings()

    def __init__(self, level="normal"):
        self.rarity_weights = [0, 50, 30, 15, 4, 1]
        self.player = Player("", 0, 0, 0, 0, 0)
        self.players = []
        self.enemy = Enemy("", 0, 0, 0, 0, 0)
        self.boss = Boss("", 0, 0, 0, 0, 0)
        self.level = level
        self.difficulty = self.settings.difficulty

    def get_players(self):
        with open("/srv/http/hyrule-castle/base_game/data/players.json") as f:
            data = json.load(f)
            for player in data:
                self.players.append(player)
        return self.players

    def get_level(self):
        """Get the level of the game."""
        return self.level

    def set_level(self, level):
        """Set the level of the game."""
        self.level = level

    def hp_to_hearts(self, hp: int, per_heart: int = 10, max_hearts: int = 15) -> str:
        hearts = int(round(hp / per_heart))
        hearts = max(0, min(hearts, max_hearts))
        return "♥" * hearts + "·" * (max_hearts - hearts)

    def draw_box(self, stdscr, y: int, x: int, h: int, w: int):
        stdscr.addstr(y, x, "┌" + "─" * (w - 2) + "┐")
        for i in range(1, h - 1):
            stdscr.addstr(y + i, x, "│" + " " * (w - 2) + "│")
        stdscr.addstr(y + h - 1, x, "└" + "─" * (w - 2) + "┘")

    def display_player_card(self, stdscr, player, y: int = 2, x: int = 2):
        w = 35
        h = 10
        self.draw_box(stdscr, y, x, h, w)
        name = player["name"] if isinstance(player, dict) else player.name
        hp = player["hp"] if isinstance(player, dict) else player.hp
        str_ = player["str_"] if isinstance(player, dict) else player.str_
        def_ = player["def_"] if isinstance(player, dict) else player.def_
        spd = player["spd"] if isinstance(player, dict) else player.spd
        luck = player["luck"] if isinstance(player, dict) else player.luck

        title = f" {name} "
        stdscr.addstr(y, x + (w - len(title)) // 2, title)
        stdscr.addstr(y + 2, x + 2, f"HP   : {self.hp_to_hearts(hp)}  ({hp})")
        stdscr.addstr(y + 3, x + 2, f"STR  : {str_}")
        stdscr.addstr(y + 4, x + 2, f"DEF  : {def_}")
        stdscr.addstr(y + 5, x + 2, f"SPD  : {spd}")
        stdscr.addstr(y + 6, x + 2, f"LUCK : {luck}")
        stdscr.addstr(y + 8, x + 2, "↑↓ choisir   ENTER confirmer")
