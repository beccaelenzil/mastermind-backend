import pytest
from app import create_app
from app import db
from datetime import datetime
from flask.signals import request_finished
from app.models.game import Game
from app.models.play import Play
from app.models.user import User


@pytest.fixture
def app():
    # create the app with a test config dictionary
    app = create_app({"TESTING": True})

    @request_finished.connect_via(app)
    def expire_session(sender, response, **extra):
        db.session.remove()

    with app.app_context():
        db.create_all()
        yield app

    # close and remove the temporary database
    with app.app_context():
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()

# game fixture
@pytest.fixture
def one_game(app):
    new_game = Game()
    db.session.add(new_game)
    db.session.commit()