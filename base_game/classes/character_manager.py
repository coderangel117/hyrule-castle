import json
import os
import random

from .Boss import Boss
from .Enemy import Enemy
from .Player import Player

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class CharacterManager:
    """Manage character selection for player, enemies, and bosses."""

    def __init__(self):
        self.rarity_weights = [0, 50, 30, 15, 4, 1]
        self.player = Player("", 0, 0, 0)
        self.enemy = Enemy("", 0, 0, 0)
        self.boss = Boss("", 0, 0, 0)

    def load_character(self, file_path, character_class):
        """Load a character from a JSON file based on rarity."""
        abs_path = os.path.join(BASE_DIR, file_path)
        with open(abs_path) as f:
            characters = json.load(f)
            weights = [self.rarity_weights[char["rarity"]] for char in characters]
            chosen = random.choices(characters, weights=weights, k=1)[0]
            return character_class(
                chosen["name"], chosen["hp"], chosen["hp"], chosen["str"]
            )

    def choose_player(self):
        """Choose a random player."""
        self.player = self.load_character("data/players.json", Player)

    def choose_enemy(self):
        """Choose a random enemy."""
        self.enemy = self.load_character("data/enemies.json", Enemy)

    def choose_boss(self):
        """Choose a random boss."""
        self.boss = self.load_character("data/bosses.json", Boss)

    def initialize_characters(self):
        """Initialize player, enemy, and boss at the start of the game."""
        self.choose_player()
        self.choose_enemy()
        self.choose_boss()
