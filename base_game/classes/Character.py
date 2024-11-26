class Character:
    def __init__(self, name, health, max_health, strength):
        self.name = name
        self.health = health
        self.max_health = max_health
        self.strength = strength


    def attack(self, target):
        print(f"{self.name} attacks {target.name}!")
        target.take_damage(self.strength)
    def defend(self, enemy):
        enemy.attack()
        self.health -= enemy.strength
        print(f"{self.name} defends!")


    def health_check(self):
        print(f"{self.name} has {self.health} health left")

    def die(self):
        print(f"{self.name} has died!")

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.die()
        else:
            print(f"{self.name} takes {damage} damage!")
            self.health_check()

    def reload_health(self):
        self.health = self.max_health