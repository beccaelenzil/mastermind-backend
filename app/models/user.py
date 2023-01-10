from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    username = db.Column(db.String)
    games = db.relationship('Game', backref='user', lazy=True)

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "username": self.username,
        }

    def win_streak(self):
        i = len(self.games)-1
        count = 0
        while i > 0 and self.games[i].plays and self.games[i].plays[-1].to_json()["win"] == True:
            count += 1
            i -= 1

        return count

    def win_percentage(self):
        win = total = 0
        for game in self.games:
            if game.plays and game.plays[-1].to_json()["win"] == True:
                win += 1
                total += 1
            elif len(game.plays) == game.get_max_guesses():
                total += 1

        if total > 0:
            return round(win/total*100, 2)
        else:
            return win

    def summary(self):
        return f"Win Streak:  {self.win_streak()}, Win % {self.win_percentage()}"
