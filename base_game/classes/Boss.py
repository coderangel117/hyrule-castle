from .Character import Character


class Boss(Character):
    def __init__(self, name, hp, str_, def_, spd, luck):
        super().__init__(name, hp, str_, def_, spd, luck)
