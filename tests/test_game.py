import pytest
from app.models.game import Game
from app.models.play import Play
import os


def test_root_route(client):
    # Act
    response = client.get("/")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body["name"] == "Mastermind API"


def test_read_games(client, levels, play1111, play1234, game1234):
    # Act
    response = client.get("/games/")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body[0]["code"] == "1234"
    assert response_body[0]["id"] == 1
    assert len(response_body[0]["plays"]) == 2
    assert response_body[0]["plays"][0]["code"] == "1111"
    assert not response_body[0]["plays"][0]["win"]
    assert response_body[0]["plays"][1]["code"] == "1234"
    assert response_body[0]["plays"][1]["win"]


def test_code_hidden_for_incomplete_game(client, levels, play1111, game1234):
    # Act
    response = client.get("/games/")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body[0]["code"] == "hidden"


def test_read_one_game(client, levels, play1111, play1234, game1234):
    # Act
    response = client.get("/games/1")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body["code"] == "1234"
    assert response_body["id"] == 1
    assert len(response_body["plays"]) == 2
    assert response_body["plays"][0]["code"] == "1111"
    assert not response_body["plays"][0]["win"]
    assert response_body["plays"][1]["code"] == "1234"
    assert response_body["plays"][1]["win"]


def test_read_one_game_not_found(client, game1234):
    # Act
    response = client.get("/games/2")

    # Assert
    assert response.status_code == 404


def test_delete_games_not_admin(client, game1234, play1111):
    # Act
    response = client.delete("/games/1", json={"admin_key": 1})

    # Assert
    assert response.status_code == 400


def test_delete_games_admin(client, game1234, play1111):
    # Act
    response = client.delete(
        "/games/", json={"admin_key": os.environ.get('SECRET_KEY')})

    # Assert
    assert response.status_code == 200
    games = Game.query.all()
    assert not games


def test_delete_1_game_admin(client, game1234, play1111):
    # Act
    response = client.delete(
        "/games/1", json={"admin_key": os.environ.get('SECRET_KEY')})

    # Assert
    assert response.status_code == 200
    games = Game.query.all()
    assert not games
    plays = Play.query.all()
    assert not plays
