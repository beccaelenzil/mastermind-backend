
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
level_bp = Blueprint("level_bp", __name__, url_prefix="/levels")
user_bp = Blueprint("user_bp", __name__, url_prefix="/users")


@root_bp.route("/", methods=["GET"])
def root():
    return {
        "name": "Mastermind API"
    }

# TODO: Consider removing since it was replaced with creating game with the first play


# @game_bp.route("/", methods=["POST"])
# def create_game():
#     request_body = request.get_json()
#     if "level" not in request_body or request_body["level"] not in ["easy", "standard", "hard"]:
#         level_name = "standard"
#     else:
#         level_name = request_body["level"]

#     level = Level.query.filter_by(name=level_name).first()
#     new_game = Game(level_id=level.id)

#     if "code" not in request_body:
#         new_game.code = new_game.generate_code()
#     else:
#         new_game.code = request_body["code"]

#     db.session.add(new_game)
#     db.session.commit()

#     return new_game.to_json(), 201


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
        # find existing game
        game = Game.query.get(request_body["game_id"])
        if not game:
            return {"error": "could not find that game"}, 404
        level = Level.query.get(game.level_id)
    elif "level" not in request_body or request_body["level"] not in ["easy", "standard", "hard"]:
        return {"error": "must provide a level: easy, standard, or hard"}, 400
    else:

        # create new game
        level_name = request_body["level"]
        level = Level.query.filter_by(name=level_name).first()
        game = Game(level_id=level.id)
        game.code = game.generate_code()

        # validate code
        if "code" not in request_body:
            return {"error": "code must be in request_body"}, 400
        elif not level.validate_code(request_body["code"]):
            return {"error": f'{request_body["code"]} that is not a valid code'}, 400

        if "user_id" in request_body:
            user = User.query.get(request_body["user_id"])
            if user:
                game.user_id = user.id

        db.session.add(game)
        db.session.commit()
        print("adding game: ", game.id)

    # create play
    new_play = Play(game_id=game.id, code=request_body["code"])

    db.session.add(new_play)
    db.session.commit()

    return new_play.to_json(), 201


@level_bp.route("/", methods=["POST"])
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


@level_bp.route("/", methods=["GET"])
def read_levels():
    levels = Level.query.all()
    levels_json = {}
    for level in levels:
        levels_json[level.name] = level.params()

    return jsonify(levels_json), 200


@level_bp.route("/<level_id>", methods=["GET"])
def read_one_level(level_id):
    level = Level.query.get(level_id)
    if not level:
        return {"error": "no level with that id"}, 404

    return {"name": level.name, "params": level.params()}, 200


@user_bp.route("/login", methods=["POST"])
def login():
    request_body = request.get_json()
    if "username" not in request_body:
        return {"error": "request body must include user name"}, 400

    user = User.query.filter_by(username=request_body["username"]).first()
    if not user:
        user = User(username=request_body["username"])
        db.session.add(user)
        db.session.commit()
        return user.to_json(), 201

    return user.to_json(), 200


@user_bp.route("/<id>", methods=["GET"])
def get_user(id):
    user = User.query.get(id)
    if not user:
        return {"error": "no user with that id"}, 404

    return {"summary": user.summary()}, 200


@game_bp.route("/", methods=["DELETE"])
def delete_all_games():
    # Delete existing
    games = Game.query.all()
    for game in games:
        plays = Play.query.filter_by(game_id=game.id)
        for play in plays:
            db.session.delete(play)
        db.session.delete(game)
        db.session.commit()

    return {"success": "delete all games"}, 20
