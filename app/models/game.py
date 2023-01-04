from app import db
import requests
from app.utils.utils import *
from app.models.level import Level
import os


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String, default="****")
    level_id = db.Column(db.Integer, db.ForeignKey('level.id'))
    plays = db.relationship('Play', backref='game', lazy=True)

    def to_json(self):
        return {
            "id": self.id,
            "code": self.code,
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
