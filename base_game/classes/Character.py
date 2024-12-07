class Character:
    def __init__(self, name, health, max_health, strength):
        self.name = name
        self.health = health
        self.max_health = max_health
        self.strength = strength

    def attack(self, target):
        target.take_damage(self.strength)

    def health_check(self):
        print("{} has {} health left".format(self.name, self.health))

    def take_damage(self, damage):
        self.health -= damage

    def relmad_health(self):
        self.health = self.max_health
