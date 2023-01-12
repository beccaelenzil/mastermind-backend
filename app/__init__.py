
from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
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

    app.config['SESSION_COOKIE_NAME'] = "session"
    app.config['SECRET_KEY'] = os.environ.get("secretKey")  # <-- random string
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    app.config['SESSION_TYPE'] = 'filesystem'

    sess = Session()
    sess.init_app(app)

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
    from .routes.login_routes import root_bp
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
