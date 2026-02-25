from .Character import Character


class Boss(Character):
    def __init__(self, name, health, max_health, strength, defense):
        super().__init__(name, health, max_health, strength, defense)
