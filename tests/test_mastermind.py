import pytest
from app.models.game import Game
from app.utils import utils

def test_root_route(client):
    # Act
    response = client.get("/")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body["name"] == "Mastermind API"

def test_create_easy_game(client):
    # Act
    response = client.post("/games", json={
        "level": "easy",
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert response_body["id"] == 1
    assert utils.validate_code(response_body["code"], "easy")

    new_game = Game.query.get(1)
    assert new_game.code == response_body["code"]