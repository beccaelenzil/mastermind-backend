
from flask import Blueprint, request, jsonify, session, abort, make_response
from ..models.user import User
from ..models.game import Game
from app import db
import os

user_bp = Blueprint("user_bp", __name__, url_prefix="/users")


@user_bp.route("/login", methods=["POST"])
def login():
    request_body = request.get_json()
    if "email" not in request_body:
        return {"error": "request body must include email"}, 400

    user = User.query.filter_by(email=request_body["email"]).first()
    if not user:
        user = User(email=request_body["email"])
        db.session.add(user)
        db.session.commit()
        return user.to_json(), 201

    return user.to_json(), 200


@user_bp.route("/<id>", methods=["GET"])
def get_user(id):
    user = User.query.get(id)
    if not user:
        return {"error": "no user with that id"}, 404

    return {"performance summary": user.summary(),
            "games": user.to_json()["games"]}, 200


@user_bp.route("/", methods=["GET"])
def get_all_users():
    users = User.query.all()
    user_json = []
    for user in users:
        user_json.append(user.to_json_less_detail())

    return jsonify(user_json), 200


@user_bp.route("/<admin_id>", methods=["DELETE"])
def delete_all_users(admin_id):
    if admin_id != os.environ.get("SECRET_KEY"):
        return {"error": "must be admin to delete users"}, 400
    # Delete existing
    users = User.query.all()
    for user in users:
        games = Game.query.filter_by(user_id=user.uid)
        for game in games:
            db.session.delete(game)
        db.session.delete(user)
        db.session.commit()

    return {"success": "delete all users"}, 200
