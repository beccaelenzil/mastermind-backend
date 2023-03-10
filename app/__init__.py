
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

    app.config['CORS_HEADERS'] = 'Content-Type'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config['SECRET_KEY'] = os.environ.get("secretKey")  # <-- random string
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    app.config['CORS_HEADERS'] = 'Content-Type'

    CORS(app)

    if test_config is None:
        uri = os.environ.get(
            "SQLALCHEMY_DATABASE_URI") + "?sslmode=require"
        if uri.startswith("postgres://"):
            uri = uri.replace("postgres://", "postgresql://", 1)
        app.config["SQLALCHEMY_DATABASE_URI"] = uri
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
    from .routes.routes import root_bp
    from .routes.game_routes import game_bp
    from .routes.user_routes import user_bp
    from .routes.play_routes import play_bp
    from .routes.level_routes import level_bp
    app.register_blueprint(root_bp)
    app.register_blueprint(game_bp)
    app.register_blueprint(play_bp)
    app.register_blueprint(level_bp)
    app.register_blueprint(user_bp)

    return app
