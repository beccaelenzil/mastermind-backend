# import pytest
# from app.models.game import Game
# from app.utils import utils


# def test_root_route(client):
#     # Act
#     response = client.get("/")
#     response_body = response.get_json()

#     # Assert
#     assert response.status_code == 200
#     assert response_body["name"] == "Mastermind API"


# def test_create_game_with_code(client, levels):
#     # Arrange
#     level = "standard"

#     # Act
#     response = client.post("/games/", json={"level": level, "code": "1234"})
#     response_body = response.get_json()

#     # Assert
#     assert response.status_code == 201
#     assert response_body["id"] == 1
#     assert response_body["code"] == "1234"

#     new_game = Game.query.get(1)
#     assert new_game.code == "1234"


# def test_read_games(client, levels, play1111, play1234, game1234):
#     # Act
#     response = client.get("/games/")
#     response_body = response.get_json()

#     # Assert
#     assert response.status_code == 200
#     assert len(response_body) == 1
#     assert response_body[0]["code"] == "1234"
#     assert response_body[0]["id"] == 1
#     assert len(response_body[0]["plays"]) == 2
#     assert response_body[0]["plays"][0]["code"] == "1111"
#     assert not response_body[0]["plays"][0]["win"]
#     assert response_body[0]["plays"][1]["code"] == "1234"
#     assert response_body[0]["plays"][1]["win"]


# def test_read_one_game(client, levels, play1111, play1234, game1234):
#     # Act
#     response = client.get("/games/1")
#     response_body = response.get_json()

#     # Assert
#     assert response.status_code == 200
#     assert response_body["code"] == "1234"
#     assert response_body["id"] == 1
#     assert len(response_body["plays"]) == 2
#     assert response_body["plays"][0]["code"] == "1111"
#     assert not response_body["plays"][0]["win"]
#     assert response_body["plays"][1]["code"] == "1234"
#     assert response_body["plays"][1]["win"]


# def test_read_one_game_not_found(client, game1234):
#     # Act
#     response = client.get("/games/2")

#     # Assert
#     assert response.status_code == 404
