import pytest
from app import create_app
from app import db
from datetime import datetime
from flask.signals import request_finished
from app.models.game import Game
from app.models.play import Play
from app.models.user import User
from app.models.level import Level


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

# levels fixture


@pytest.fixture
def levels(app):
    levels = ["easy", "standard", "hard"]
    for level in levels:
        db.session.add(Level(name=level))
        db.session.commit()


# game fixture

@pytest.fixture
def game1234(app, levels):
    level = Level.query.filter_by(name="standard").first()
    new_game = Game(level_id=level.id, code="1234")
    db.session.add(new_game)
    db.session.commit()

# play fixtures


@pytest.fixture
def play1111(app, game1234):
    game = Game.query.first()
    new_play = Play(game_id=game.id, code="1111")
    db.session.add(new_play)
    db.session.commit()


@pytest.fixture
def play2100(app, game1234):
    game = Game.query.first()
    new_play = Play(game_id=game.id, code="2100")
    db.session.add(new_play)
    db.session.commit()


@pytest.fixture
def play1200(app, game1234):
    game = Game.query.first()
    new_play = Play(game_id=game.id, code="1200")
    db.session.add(new_play)
    db.session.commit()


@pytest.fixture
def play1234(app, game1234):
    game = Game.query.first()
    new_play = Play(game_id=game.id, code="1234")
    db.session.add(new_play)
    db.session.commit()


@pytest.fixture
def playXXXX(app, game1234):
    game = Game.query.first()
    new_play = Play(game_id=game.id, code="XXXX")
    db.session.add(new_play)
    db.session.commit()


@pytest.fixture
def play9999(app, game1234):
    game = Game.query.first()
    new_play = Play(game_id=game.id, code="9999")
    db.session.add(new_play)
    db.session.commit()


@pytest.fixture
def play00000000(app, game1234):
    game = Game.query.first()
    new_play = Play(game_id=game.id, code="00000000")
    db.session.add(new_play)
    db.session.commit()

# user


@pytest.fixture
def user1(app):
    user = User(username="becca")
    db.session.add(user)
    db.session.commit()


@pytest.fixture
def user_win_2_lose_1(app, levels):
    user = User(username="becca")
    db.session.add(user)
    db.session.commit()
    level = Level.query.filter_by(name="easy").first()
    new_game = Game(level_id=level.id, code="1234", user_id=user.id)
    db.session.add(new_game)
    db.session.commit()
    # lost game
    for i in range(10):
        play1111 = Play(code="1111", game_id=new_game.id)
        db.session.add(play1111)
        db.session.commit()
    # 2 win games
    for i in range(2):
        new_game = Game(level_id=level.id, code="1234", user_id=user.id)
        db.session.add(new_game)
        db.session.commit()
        play1234 = Play(code="1234", game_id=new_game.id)
        db.session.add(play1234)
        db.session.commit()


@pytest.fixture
def users2(app):
    user = User(username="a")
    db.session.add(user)
    db.session.commit()

    user = User(username="b")
    db.session.add(user)
    db.session.commit()
