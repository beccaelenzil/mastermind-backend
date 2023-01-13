from app.models.play import Play
from app.models.game import Game

# create play


def test_new_standard_game(client, levels):
    # arrange
    code = "5555"
    level = "standard"

    # Act
    response = client.post(
        "/plays/", json={"code": code, "level": level, "game_id": None})

    assert response.status_code == 201

    response_body = response.get_json()

    # Assert
    assert response_body["game_id"] == 1
    assert response_body["code"] == "5555"

    play = Play.query.first()
    assert play.code == code
    game = Game.query.first()
    assert game.id == 1


def test_new_easy_game(client, levels):
    # arrange
    code = "1111"
    level = "easy"

    # Act
    response = client.post(
        "/plays/", json={"code": code, "level": level, "game_id": None})

    assert response.status_code == 201

    response_body = response.get_json()

    # Assert
    assert response_body["game_id"] == 1
    assert response_body["code"] == code

    play = Play.query.first()
    assert play.code == code
    game = Game.query.first()
    assert game.id == 1


def test_new_hard_game(client, levels):
    # arrange
    code = "777777"
    level = "hard"

    # Act
    response = client.post(
        "/plays/", json={"code": code, "level": level, "game_id": None})

    assert response.status_code == 201

    response_body = response.get_json()

    # Assert
    assert response_body["game_id"] == 1
    assert response_body["code"] == code

    play = Play.query.first()
    assert play.code == code
    game = Game.query.first()
    assert game.id == 1


def test_new_game_with_user_1111(client, user1, levels):

    # Act
    response = client.post(
        "/plays/", json={"code": "1111", "level": "standard", "game_id": None, "user_id": 1})

    assert response.status_code == 201

    response_body = response.get_json()

    # Assert
    assert response_body["game_id"] == 1
    assert response_body["code"] == "1111"

    play = Play.query.first()
    assert play.code == "1111"
    game = Game.query.first()
    assert game.id == 1
    assert game.user_id == 1


def test_1234_1234(client, game1234, play1111, levels):
    # Arrange
    game = Game.query.first()
    game_id = game.id

    # Act
    response = client.post(
        "/plays/", json={"code": "1234", "game_id": game_id})
    assert response.status_code == 201

    response_body = response.get_json()
    # Assert
    assert response_body["game_id"] == game_id
    assert response_body["code"] == "1234"
    assert response_body["correct_nums"] == 4
    assert response_body["correct_pos"] == 4
    assert response_body["win"]
    assert response_body["answer"] == "1234"

    play = Play.query.get(2)
    assert play.code == "1234"


def test_answer_hidden_for_wrong_guess(client, game1234, play1111, levels):
    # Arrange
    game = Game.query.first()
    game_id = game.id

    # Act
    response = client.post(
        "/plays/", json={"code": "1111", "game_id": game_id})
    assert response.status_code == 201

    response_body = response.get_json()
    # Assert
    assert response_body["game_id"] == game_id
    assert not response_body["win"]
    assert response_body["answer"] == "hidden"

    play = Play.query.get(2)
    assert play.code == "1111"


def test_invalid_XXXX(client, game1234):
    # Arrange
    game = Game.query.first()
    game_id = game.id

    response = client.post(
        "/plays/", json={"code": "XXXX", "game_id": game_id})

    assert response.status_code == 400


def test_invalid_9999(client, game1234):
    # Arrange
    game = Game.query.first()
    game_id = game.id

    response = client.post(
        "/plays/", json={"code": "9999", "game_id": game_id})

    assert response.status_code == 400


def test_invalid_00000000(client, game1234):
    # Arrange
    game = Game.query.first()
    game_id = game.id

    response = client.post(
        "/plays/", json={"code": "00000000", "game_id": game_id})

    assert response.status_code == 400


# 400 level errors
def test_create_play_missing_game_id(client):
    # Act
    response = client.post(
        "/plays/", json={"code": "1111", "level": "standard"})

    # Assert
    assert response.status_code == 400


def test_create_play_missing_level(client, levels):
    # Act
    response = client.post("/plays/", json={"code": "1111", "game_id": None})

    # Assert
    assert response.status_code == 400


def test_create_play_missing_code(client, levels):
    # Act
    response = client.post(
        "/plays/", json={"level": "standard", "game_id": None})

    # Assert
    assert response.status_code == 400


def test_create_play_game_not_found(client, game1234):
    # Act
    response = client.post(
        "/plays/", json={"code": "1111", "game_id": 2})

    # Assert
    assert response.status_code == 404
