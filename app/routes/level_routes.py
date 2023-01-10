
from flask import Blueprint, request, jsonify, Response, make_response
from ..models.level import Level
from app import db

level_bp = Blueprint("level_bp", __name__, url_prefix="/levels")


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
