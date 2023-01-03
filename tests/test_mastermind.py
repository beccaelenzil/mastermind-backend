import pytest
from app.models.game import Game
from app.utils import utils
from app.models.play import Play

def test_root_route(client):
    # Act
    response = client.get("/")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body["name"] == "Mastermind API"

def test_create_game_with_code(client):
    # Arrange
    level = "standard"

    # Act
    response = client.post("/games/",json={"level": level, "code": "1234"})
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert response_body["id"] == 1
    assert response_body["code"] == "1234"

    new_game = Game.query.get(1)
    assert new_game.code == "1234"

def test_correct_nums_1(client, game1234, play1111):
    play = Play.query.first()
    assert play.correct_nums() == 1

def test_correct_pos_1(client, game1234, play1111):
    play = Play.query.first()
    assert play.correct_pos() == 1

def test_not_win_1234_1111(client, game1234, play1111):
    play = Play.query.first()
    assert not play.win()

def test_correct_nums_2(client, game1234, play2100):
    play = Play.query.first()
    assert play.correct_nums() == 2

def test_correct_pos_0(client, game1234, play2100):
    play = Play.query.first()
    assert play.correct_pos() == 0

def test_not_win_1234_2100(client, game1234, play2100):
    play = Play.query.first()
    assert not play.win()

def test_correct_nums_2b(client, game1234, play1200):
    play = Play.query.first()
    assert play.correct_nums() == 2

def test_correct_pos_2(client, game1234, play1200):
    play = Play.query.first()
    assert play.correct_pos() == 2



def test_correct_nums_4(client, game1234, play1234):
    play = Play.query.first()
    assert play.correct_nums() == 4

def test_correct_pos_4(client, game1234, play1234):
    play = Play.query.first()
    assert play.correct_pos() == 4

def test_not_win_1234_1111(client, game1234, play1200):
    play = Play.query.first()
    assert not play.win()

def test_win(client, game1234, play1234):
    play = Play.query.first()
    assert play.win()
    