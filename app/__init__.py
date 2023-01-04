
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from dotenv import load_dotenv
from flask_cors import CORS


db = SQLAlchemy()
migrate = Migrate()
load_dotenv()


def create_app(test_config=None):
    app = Flask(__name__)
    CORS(app)
    app.config['CORS_HEADERS'] = 'Content-Type'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    if test_config is None:
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
            "SQLALCHEMY_DATABASE_URI")
    else:
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
            "SQLALCHEMY_TEST_DATABASE_URI")

    # Import models here for Alembic setup
    from app.models.game import Game
    from app.models.play import Play
    from app.models.user import User
    from app.models.level import Level

    db.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints here
    from .routes import root_bp, game_bp, play_bp, l_bp
    app.register_blueprint(root_bp)
    app.register_blueprint(game_bp)
    app.register_blueprint(play_bp)
    app.register_blueprint(l_bp)

    return app
