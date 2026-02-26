from .Character import Character


class Player(Character):
    def __init__(self, name, hp, str_, def_, spd, luck):
        super().__init__(name, hp, str_, def_, spd, luck)

    def self_heal(self):
        """
        The player use heal power
        Heal permit to recovers half max point
        """
        hp = self.max_health / 4
        if self.hp + hp > self.max_health:
            self.hp = self.max_health
            int(self.hp)
        else:
            self.hp += hp
            int(self.hp)
