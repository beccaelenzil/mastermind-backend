from app import db
import requests
from app.models.constants import PARAMS, LEVELS, RANDOM_URL

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String,default="****")
    max_guesses = db.Column(db.Integer,default=10)
    code_length = db.Column(db.Integer,default=PARAMS["num"])
    n_choices = db.Column(db.Integer,default=PARAMS["max"]+1)
    level = db.Column(db.Integer,default="standard")
    plays = db.relationship('Play', backref='game', lazy=True)

    def to_json(self):
        return {
            "id": self.id,
            "code": self.code,
        }

    def generate_code(self):
        PARAMS["max"] = LEVELS[self.level]["max"]
        response = requests.get(RANDOM_URL, params=PARAMS)
        




    