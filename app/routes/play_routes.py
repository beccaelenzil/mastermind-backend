
from flask import Blueprint, request, jsonify, Response, make_response
from ..models.game import Game
from ..models.play import Play
from ..models.user import User
from ..models.level import Level
from app import db

play_bp = Blueprint("play_bp", __name__, url_prefix="/plays")


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
