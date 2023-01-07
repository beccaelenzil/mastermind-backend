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
        i = len(self.games)
        count = 0
        while i > 0 and self.games[i].plays[-1] == True:
            count += 1
            i -= 1

        return count

    def win_percentage(self):
        win = total = 0
        for game in self.games:
            if game.plays[-1] == True:
                win += 1
                total += 1
            elif len(game.plays) == game.get_max_guesses():
                total += 1

        return round(win/total*100, 2)

    def summary(self):
        print("Win Streak: ", self.win_streak(),
              "Win %", self.win_percentage())
