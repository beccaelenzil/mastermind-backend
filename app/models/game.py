from app import db
import requests
from app.models.constants import PARAMS, LEVELS, RANDOM_URL
from app.utils.utils import *

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String,default="****")
    max_guesses = db.Column(db.Integer,default=10)
    code_length = db.Column(db.Integer,default=PARAMS["num"])
    n_choices = db.Column(db.Integer,default=PARAMS["max"]+1)
    level = db.Column(db.String)
    plays = db.relationship('Play', backref='game', lazy=True)

    def to_json(self):
        return {
            "id": self.id,
            "code": self.code,
            "plays": [play.to_json() for play in self.plays]
        }

    #TODO: move this method into the constructor
    @classmethod
    def generate_code(cls, level):
        PARAMS = return_params(level)
        response = requests.get(RANDOM_URL, params=PARAMS)
        code = response.text.replace('\n','')
        return code
        




    