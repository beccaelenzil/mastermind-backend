
from flask import Blueprint

root_bp = Blueprint("root_bp", __name__)


@root_bp.route("/", methods=["GET"])
def root():
    return {
        "name": "Mastermind API"
    }
