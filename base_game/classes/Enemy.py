from base_game.classes.Character import Character


class Enemy(Character):
    def __init__(self, name, health, max_health, strength):
        super().__init__(name, health, max_health, strength)
