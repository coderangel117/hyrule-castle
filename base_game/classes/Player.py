from base_game.classes.Character import Character


class Player(Character):
    def __init__(self, name, health, max_health, strength):
        super().__init__(name, health, max_health, strength)

    def self_heal(self):
        heal_point = self.max_health - self.health
        hp = self.max_health / 2
        if self.health + hp > self.max_health:
            self.health = self.max_health
            int(self.health)
        else:
            self.health += hp
            int(self.health)
