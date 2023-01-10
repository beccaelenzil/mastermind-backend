
from flask import Blueprint, request, jsonify, Response, make_response
from ..models.user import User
from app import db

user_bp = Blueprint("user_bp", __name__, url_prefix="/users")


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

    return {"username": user.username,
            "performance summary": user.summary(),
            "games": user.to_json()["games"]}, 200


@user_bp.route("/", methods=["GET"])
def get_all_users():
    users = User.query.all()
    user_json = []
    for user in users:
        user_json.append({"user_id": user.id, "username": user.username})

    return jsonify(user_json), 200
