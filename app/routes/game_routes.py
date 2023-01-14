
from flask import Blueprint, jsonify, abort, make_response, request
from ..models.game import Game
from ..models.play import Play
from app import db
import os

game_bp = Blueprint("game_bp", __name__, url_prefix="/games")


def get_game(id):
    game = Game.query.get(id)
    if not game:
        abort(make_response({"error": "No game with that game_id"}, 404))

    return game


def require_admin(request_body):
    if "admin_key" not in request_body or request_body["admin_key"] != os.environ.get("SECRET_KEY"):
        abort(make_response({"error": "must be admin to delete games"}, 400))


@game_bp.route("/", methods=["GET"])
def read_game():
    games = Game.query.all()
    game_json = []
    for game in games:
        game_json.append(game.to_json())

    return jsonify(game_json), 200


@game_bp.route("/<id>", methods=["GET"])
def read_one_game(id):
    game = get_game(id)
    return game.to_json(), 200


@game_bp.route("/", methods=["DELETE"])
def delete_all_games():
    request_body = request.get_json()
    require_admin(request_body)

    games = Game.query.all()
    for game in games:
        plays = Play.query.filter_by(game_id=game.id)
        for play in plays:
            db.session.delete(play)
        db.session.delete(game)
        db.session.commit()

    return {"success": "delete all games"}, 200


@game_bp.route("/<id>", methods=["DELETE"])
def delete_one_game(id):
    request_body = request.get_json()
    require_admin(request_body)

    game = get_game(id)
    plays = Play.query.filter_by(game_id=game.id)
    for play in plays:
        db.session.delete(play)
    db.session.delete(game)
    db.session.commit()

    return {"success": f"delete game {id}"}, 200
