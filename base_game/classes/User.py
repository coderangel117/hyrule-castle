class User:

    def __init__(self, username: str, greatest_score=None, played_games: int = 0, nbfail: int = 0,
                 nbwin: int = 0) -> None:
        if greatest_score is None:
            greatest_score = []
        self.username = username
        self.greatest_score = greatest_score
        self.played_games = played_games
        self.nbfail = nbfail
        self.nbwin = nbwin

    def tostring(self):
        return f" Joueur {self.username} a {self.nbfail} défaites et {self.nbwin} victoires"

    def getusername(self):
        return self.username

    def getplayedgames(self):
        return self.played_games

    def getgreatestscore(self):
        return self.greatest_score

    def getnbwin(self):
        return self.nbwin

    def getnbfail(self):
        return self.nbfail

    def add_win(self):
        self.nbwin += 1

    def add_fail(self):
        self.nbfail += 1
