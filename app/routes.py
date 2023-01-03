
from flask import Blueprint, request, jsonify, Response, make_response
import requests
import os

from .models.game import Game
from .models.play import Play
from .models.user import User
from app import db
from app.utils import utils

root_bp = Blueprint("root_bp", __name__)
game_bp = Blueprint("game_bp", __name__,url_prefix="/games")
play_bp = Blueprint("play_bp", __name__,url_prefix="/plays")

@root_bp.route("/", methods=["GET"])
def root():
    return {
        "name": "Mastermind API"
    }

#TODO: Consider removing since it was replaced with creating game with the first play
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

    return new_game.to_json(), 201

@game_bp.route("/", methods=["GET"])
def read_game():
    games = Game.query.all()
    game_json = []
    for game in games:
        game_json.append(game.to_json())
    
    return jsonify(game_json), 200

@game_bp.route("/<game_id>", methods=["GET"])
def read_one_game(game_id):
    game = Game.query.get(game_id)
    if not game:
        return {"error": "No game with that game_id"}, 404
    
    return game.to_json(), 200


@play_bp.route("/", methods=["POST"])
def create_play():
    request_body = request.get_json()
    if "game_id" not in request_body:
        return {"error": "game_id must be in request_body"}, 400
    elif request_body["game_id"]:
        # find game in database
        game = Game.query.get(request_body["game_id"])
        if not game:
            return {"error": "could not find that game"}, 400
    elif "level" not in request_body:
        return {"error": "must provide a level"}, 400
    else:
        # create game with first play
        level=request_body["level"]
        game = Game(level=level)
        game.code = Game.generate_code(level)
        db.session.add(game)
        db.session.commit()
    
    game_id = game.id
    if "code" not in request_body:
        return {"error": "code must be in request_body"}, 400
    elif not utils.validate_code(request_body["code"], game.level):
        return {"error": f'{request_body["code"]} that is not a valid code' }, 400
    

    new_play = Play(game_id=game_id, code=request_body["code"])

    db.session.add(new_play)
    db.session.commit()

    return new_play.to_json(), 201



    

    
