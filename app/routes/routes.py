
from flask import Blueprint, request, jsonify, Response, make_response
from app import db

root_bp = Blueprint("root_bp", __name__)


@root_bp.route("/", methods=["GET"])
def root():
    return {
        "name": "Mastermind API"
    }
