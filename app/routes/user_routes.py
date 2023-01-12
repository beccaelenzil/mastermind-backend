
from flask import Blueprint, request, jsonify, session, abort, make_response
from ..models.user import User
from app import db

user_bp = Blueprint("user_bp", __name__, url_prefix="/users")


def require_login(user):
    if "google_uid" in session and session["google_uid"] != user.google_uid:
        abort(make_response(
            {"error": "must be logged in to see user details"}, 400))


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

    require_login(user)

    return {"email": user.email,
            "performance summary": user.summary(),
            "games": user.to_json()["games"]}, 200


@user_bp.route("/email/<email>", methods=["GET"])
def get_user_by_email(email):
    user = User.query.filter_by(email=email).first()
    if not user:
        return {"error": "no user with that email"}, 404

    require_login(user)

    return {"email": user.email,
            "performance summary": user.summary(),
            "games": user.to_json()["games"],
            "user_id": user.uid}, 200


@user_bp.route("/", methods=["GET"])
def get_all_users():
    users = User.query.all()
    user_json = []
    for user in users:
        user_json.append(user.to_json_less_detail())

    return jsonify(user_json), 200
