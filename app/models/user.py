from app import db
from app.models.game import Game


def get_user(google_uid):
    user = User.query.filter_by(google_uid=google_uid).first()
    return user


class User(db.Model):
    uid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    google_uid = db.Column(db.String)
    name = db.Column(db.String)
    email = db.Column(db.String)
    games = db.relationship('Game', backref='user', lazy=True)

    def to_json(self):
        return {
            "uid": self.uid,
            "name": self.name,
            "email": self.email,
            "google_uid": self.google_uid,
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
            return {"percent": 0, "total": 0, "win": 0}

    def make_histogram(self):
        games = self.sort_games()
        num_plays = []
        for game in games:
            if game["plays"] and game["plays"][-1]["win"] == True:
                num_plays.append(len(game["plays"]))

        freq = {}
        histogram = {}

        if num_plays:
            for num in range(0, max(num_plays)+1):
                freq[num] = 0

            for num in num_plays:
                freq[num] += 1

            for num in range(1, max(num_plays)+1):
                histogram[num] = f"{'x'*freq[num]}"

        sorted_hist = sorted(histogram.items(), key=lambda x: x[1])
        sorted_hist = dict(sorted_hist)
        return [histogram, freq]

    def summary(self):
        summary_json = {
            "Win Streak":  self.win_streak(),
            "Win %": self.win_percentage()["percent"],
            "Games won": self.win_percentage()["win"],
            "Total games": self.win_percentage()["total"],
        }

        if (len(self.games)):
            summary_json["Distribution of number of plays for winning games"] = self.make_histogram()[
                0]

        return summary_json
