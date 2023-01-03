import pytest
from app.models.game import Game
from app.utils import utils

#TODO: refactor these tests to test the create game by making 1 play route
def test_create_standard_game(client):
    # Arrange
    level = "standard"

    # Act
    response = client.post("/games/",json={"level": level})
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert response_body["id"] == 1
    assert utils.validate_code(response_body["code"], level)

    new_game = Game.query.get(1)
    assert new_game.code == response_body["code"]

def test_create_easy_game(client):
    # Arrange
    level = "easy"

    # Act
    response = client.post("/games/",json={"level": level})
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert response_body["id"] == 1
    assert utils.validate_code(response_body["code"], level)

    new_game = Game.query.get(1)
    assert new_game.code == response_body["code"]

def test_create_hard_game(client):
    # Arrange
    level = "hard"

    # Act
    response = client.post("/games/",json={"level": level})
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert response_body["id"] == 1
    assert utils.validate_code(response_body["code"], level)

    new_game = Game.query.get(1)
    assert new_game.code == response_body["code"]