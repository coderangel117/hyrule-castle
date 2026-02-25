class Character:
    def __init__(self, name, health, max_health, strength, defense):
        self.name = name
        self.health = health
        self.max_health = max_health
        self.strength = strength
        self.defense = defense

    def attack(self, target):
        target.take_damage(self.strength)

    def health_check(self):
        print("{} a {} points de vie restants".format(self.name, self.health))

    def take_damage(self, damage):
        final_damage = damage - self.defense
        self.health -= final_damage

    def reload_health(self):
        self.health = self.max_health
