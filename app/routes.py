
from flask import Blueprint, request, jsonify, Response, make_response
import requests
import os

from .models.game import Game
from .models.play import Play
from .models.user import User
from .models.level import Level
from app import db
from app.utils import utils

root_bp = Blueprint("root_bp", __name__)
game_bp = Blueprint("game_bp", __name__, url_prefix="/games")
play_bp = Blueprint("play_bp", __name__, url_prefix="/plays")
l_bp = Blueprint("l_bp", __name__, url_prefix="/levels")


@root_bp.route("/", methods=["GET"])
def root():
    return {
        "name": "Mastermind API"
    }

# TODO: Consider removing since it was replaced with creating game with the first play


@game_bp.route("/", methods=["POST"])
def create_game():
    request_body = request.get_json()
    if "level" not in request_body or request_body["level"] not in ["easy", "standard", "hard"]:
        level_name = "standard"
    else:
        level_name = request_body["level"]

    level = Level.query.filter_by(name=level_name).first()
    new_game = Game(level_id=level.id)

    if "code" not in request_body:
        new_game.code = new_game.generate_code()
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
    elif "level" not in request_body or request_body["level"] not in ["easy", "standard", "hard"]:
        return {"error": "must provide a level: easy, standard, or hard"}, 400
    elif request_body["game_id"]:
        # find existing game
        game = Game.query.get(request_body["game_id"])
        if not game:
            return {"error": "could not find that game"}, 40
    else:
        # create new game
        level_name = request_body["level"]
        level = Level.query.filter_by(name=level_name).first()
        game = Game(level_id=level.id)
        game.code = game.generate_code()
        db.session.add(game)
        db.session.commit()

    if "code" not in request_body:
        return {"error": "code must be in request_body"}, 400
    elif not level.validate_code(request_body["code"]):
        return {"error": f'{request_body["code"]} that is not a valid code'}, 400

    new_play = Play(game_id=game.id, code=request_body["code"])

    db.session.add(new_play)
    db.session.commit()

    return new_play.to_json(), 201


@l_bp.route("/", methods=["POST"])
def create_levels():
    # Delete existing
    levels = Level.query.all()
    for level in levels:
        db.session.delete(level)
        db.session.commit()

    level_names = ["easy", "standard", "hard"]
    levels_json = []
    for level_name in level_names:
        level = Level(name=level_name)
        levels_json.append({"name": level_name, "params": level.params()})
        db.session.add(level)
        db.session.commit()

    return jsonify(levels_json), 201


@l_bp.route("/", methods=["GET"])
def read_levels():
    levels = Level.query.all()
    levels_json = []
    for level in levels:
        levels_json.append(level.params())

    return jsonify(levels_json), 200


@l_bp.route("/<level_id>", methods=["GET"])
def read_one_level(level_id):
    level = Level.query.get(level_id)
    if not level:
        return {"error": "no level with that id"}, 404

    return {"name": level.name, "params": level.params()}, 200
