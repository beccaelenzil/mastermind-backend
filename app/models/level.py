from app import db

LEVELS = {
    "easy": {
        "max": 3,
        "num": 4
    },
    "standard": {
        "max": 7,
        "num": 4
    },
    "hard": {
        "max": 7,
        "num": 6
    },
}


class Level(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, default="standard")
    games = db.relationship('Game', backref='level', lazy=True)

    def params(self):
        return {
            "num":  LEVELS[self.name]["num"],
            "min": 0,
            "max": LEVELS[self.name]["max"],
            "col": 1,
            "base": 10,
            "format": "plain",
            "rnd": "new",
            "max_guesses": 10
        }

    def validate_code(self, code):
        params = self.params()

        if len(code) != params["num"]:
            return False

        for char in code:
            try:
                i = int(char)
            except:
                return False

            if i < 0 or int(char) > params["max"]:
                return False

        return True
