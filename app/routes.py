
from flask import Blueprint, request, jsonify, Response, make_response
import requests
import os

from .models.game import Game
from .models.play import Play
from .models.user import User
from app import db

root_bp = Blueprint("root_bp", __name__)
game_bp = Blueprint("game_bp", __name__,url_prefix="/games")

@root_bp.route("/", methods=["GET"])
def root():
    return {
        "name": "Mastermind API"
    }

@game_bp.route("/", methods=["POST"])
def create_game():
    pass
    
