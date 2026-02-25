from .Character import Character


class Player(Character):
    def __init__(self, name, health, max_health, strength, defense):
        super().__init__(name, health, max_health, strength, defense)

    def self_heal(self):
        """
        The player use heal power
        Heal permit to recovers half max point
        """
        hp = self.max_health / 4
        if self.health + hp > self.max_health:
            self.health = self.max_health
            int(self.health)
        else:
            self.health += hp
            int(self.health)
