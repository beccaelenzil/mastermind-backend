
from flask import Blueprint, jsonify, abort, make_response, session
from ..models.game import Game
from ..models.play import Play
from app import db
import os

game_bp = Blueprint("game_bp", __name__, url_prefix="/games")


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


@game_bp.route("/<admin_id>", methods=["DELETE"])
def delete_all_games(admin_id):
    if admin_id != os.environ.get("SECRET_KEY"):
        return {"error": "must be admin to delete games"}, 400
    # Delete existing
    games = Game.query.all()
    for game in games:
        plays = Play.query.filter_by(game_id=game.id)
        for play in plays:
            db.session.delete(play)
        db.session.delete(game)
        db.session.commit()

    return {"success": "delete all games"}, 200
