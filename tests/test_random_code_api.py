# import pytest
# from app.models.game import Game
# from app.models.level import Level
# from app.utils import utils

# # TODO: refactor these tests to test the create game by making 1 play route


# def test_create_standard_game(client, levels):
#     # Arrange
#     level = "standard"
#     l = Level.query.filter_by(name=level).first()

#     # Act
#     response = client.post("/games/", json={"level": level})
#     response_body = response.get_json()

#     # Assert
#     assert response.status_code == 201
#     assert response_body["id"] == 1
#     assert l.validate_code(response_body["code"])

#     new_game = Game.query.get(1)
#     assert new_game.code == response_body["code"]


# def test_create_easy_game(client, levels):
#     # Arrange
#     level = "easy"
#     l = Level.query.filter_by(name=level).first()

#     # Act
#     response = client.post("/games/", json={"level": level})
#     response_body = response.get_json()

#     # Assert
#     assert response.status_code == 201
#     assert response_body["id"] == 1
#     assert l.validate_code(response_body["code"])

#     new_game = Game.query.get(1)
#     assert new_game.code == response_body["code"]


# def test_create_hard_game(client, levels):
#     # Arrange
#     level = "hard"
#     l = Level.query.filter_by(name=level).first()

#     # Act
#     response = client.post("/games/", json={"level": level})
#     response_body = response.get_json()

#     # Assert
#     assert response.status_code == 201
#     assert response_body["id"] == 1
#     assert l.validate_code(response_body["code"])

#     new_game = Game.query.get(1)
#     assert new_game.code == response_body["code"]
