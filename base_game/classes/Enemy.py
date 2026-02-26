from .Character import Character


class Enemy(Character):
    def __init__(self, name, hp, str_, def_, spd, luck):
        super().__init__(name, hp, str_, def_, spd, luck)
