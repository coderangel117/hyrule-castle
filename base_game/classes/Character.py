class Character:

    def __init__(self, name, health, max_health, strength):
        self.name = name
        self.health = health
        self.max_health = max_health
        self.strength = strength

    def attack(self, target):
        print(f"{self.name} attacks {target.name} and deals {self.strength} damages!")
        target.take_damage(self.strength)

    def health_check(self):
        print(f"{self.name} has {self.health} health left")

    def take_damage(self, damage):
        self.health -= damage

    def reload_health(self):
        self.health = self.max_health
