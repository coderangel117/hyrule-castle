class Character:
    def __init__(self, name, hp, str_, def_, spd, luck):
        self.name = name
        self.hp = hp
        self.max_health = hp
        self.strength = str_
        self.defense = def_
        self.spd = spd
        self.luck = luck

    def attack(self, target):
        target.take_damage(self.strength)

    def health_check(self):
        print("{} a {} points de vie restants".format(self.name, self.hp))

    def take_damage(self, damage):
        final_damage = damage - self.def_
        self.hp -= final_damage

    def reload_health(self):
        self.hp = self.max_health
