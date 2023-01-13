from app import db
import requests
from app.models.level import Level
import os


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String, default="****")
    level_id = db.Column(db.Integer, db.ForeignKey('level.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.uid'))
    plays = db.relationship('Play', backref='game', lazy=True)

    def to_json(self):
        return {
            "id": self.id,
            "code": self.display_code(),
            "user_id": self.user_id,
            "level_params": self.get_level().params() if self.get_level() else None,
            "level": self.get_level().name if self.get_level() else None,
            "plays": [play.to_json() for play in self.plays]
        }

    def get_level(self):
        return Level.query.get(self.level_id)

    def generate_code(self):
        level = self.get_level()
        response = requests.get(os.environ.get(
            "RANDOM_URL"), params=level.params())
        code = response.text.replace('\n', '')
        return code

    def display_code(self):
        level = Level.query.get(self.level_id)
        if not level:
            return None

        params = level.params()
        max_guesses = params["max_guesses"]
        plays = self.plays
        plays.sort(key=lambda play: play.id)
        print(len(plays), plays[-1].win)
        if len(plays) == max_guesses or plays[-1].win():
            return self.code
        else:
            return "hidden"
