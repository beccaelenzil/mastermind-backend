from app.models.level import Level
from app.models.game import Game


def test_create_levels(client):
    # Act
    response = client.post("/levels/")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert len(response_body) == 3

    easy = response_body[0]
    standard = response_body[1]
    hard = response_body[2]

    assert easy["name"] == "easy"
    assert standard["name"] == "standard"
    assert hard["name"] == "hard"


def test_create_levels_when_there_are_already_levels_in_db(client, levels):
    # Act
    response = client.post("/levels/")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert len(response_body) == 3

    easy = response_body[0]
    standard = response_body[1]
    hard = response_body[2]

    assert easy["name"] == "easy"
    assert standard["name"] == "standard"
    assert hard["name"] == "hard"


def test_read_levels(client):
    response = client.get("/levels/")
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body) == 0


def test_read_levels_3(client, levels):
    response = client.get("/levels/")
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body.keys()) == 3


def test_read_one_level(client, levels):
    response = client.get("/levels/1")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body["name"] == "easy"
    params = response_body["params"]
    assert params == {
        "num":  4,
        "min": 0,
        "max": 3,
        "col": 1,
        "base": 10,
        "format": "plain",
        "rnd": "new",
        "max_guesses": 10
    }


def test_read_one_level_not_found(client, levels):
    response = client.get("/levels/10")

    assert response.status_code == 404
