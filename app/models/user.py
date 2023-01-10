from app import db
from app.models.game import Game


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
            "games": [game.to_json() for game in self.games]
        }

    def sort_games(self):
        games = self.to_json()["games"]
        games.sort(key=lambda game: game["id"])
        for game in games:
            game["plays"].sort(key=lambda play: play["id"])

        return games

    def win_streak(self):
        games = self.sort_games()
        i = len(games)-1
        count = 0
        while i >= 0 and games[i]["plays"] and games[i]["plays"][-1]["win"] == True:
            count += 1
            i -= 1

        return count

    def win_percentage(self):
        win = total = 0
        games = self.sort_games()
        for game in games:
            if game["plays"] and game["plays"][-1]["win"] == True:
                win += 1
                total += 1
            elif len(game["plays"]) == game["level_params"]["max_guesses"]:
                total += 1

        if total > 0:
            return {"percent": round(win/total*100, 2), "total": total, "win": win}
        else:
            return win

    def summary(self):
        return {
            "Win Streak":  self.win_streak(),
            "Win %": self.win_percentage()["percent"],
            "Games won": self.win_percentage()["win"],
            "Total games": self.win_percentage()["total"]
        }
