
from flask import Blueprint, request, jsonify, Response, make_response
import requests
import os

from .models.game import Game
from .models.play import Play
from .models.user import User
from app import db

root_bp = Blueprint("root_bp", __name__)
game_bp = Blueprint("game_bp", __name__,url_prefix="/games")

@root_bp.route("/", methods=["GET"])
def root():
    return {
        "name": "Mastermind API"
    }

@game_bp.route("/", methods=["POST"])
def create_game():
    request_body = request.get_json()
    if "level" not in request_body:
        level = "standard"
    else:
        level = request_body["level"]

    new_game = Game(level=level)
    if "code" not in request_body:
        #TODO: Move generate_code method into the constructor
        new_game.code = Game.generate_code(level)
    else:
        new_game.code = request_body["code"]

    db.session.add(new_game)
    db.session.commit()

    return {"id":new_game.id, "code": new_game.code}, 201



    

    
