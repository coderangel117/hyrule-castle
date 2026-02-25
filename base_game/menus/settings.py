class GameSettings:
    def __init__(self):
        self.sound = True
        self.music = True
        self.difficulty = {
            "easy": 0.8,
            "normal": 1.0,
            "hard": 1.5,
            "legendary": 2.0,
        }
