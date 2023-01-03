from app.models.play import Play
from app.models.game import Game

# create play
def test_new_game_1111(client):

    # Act
    response = client.post("/plays/",json={"code": "1111", "level": "standard"})
    response_body = response.get_json()
    print(response)

    # Assert
    assert response_body["game_id"] == 1
    assert response_body["code"] == "1111"

    play = Play.query.first()
    assert play.code == "1111"
    game = Game.query.first()
    assert game.id == 1

def test_1234_1234(client, game1234, play1111):
    # Arrange
    game = Game.query.first()
    game_id = game.id

    # Act
    response = client.post("/plays/",json={"code": "1234", "game_id": game_id})
    response_body = response.get_json()

    # Assert
    assert response_body["game_id"] == game_id
    assert response_body["code"] == "1234"
    assert response_body["correct_nums"] == 4
    assert response_body["correct_pos"] == 4
    assert response_body["win"]

    play = Play.query.get(2)
    assert play.code == "1234"


# correct nums
def test_correct_nums_1(client, game1234, play1111):
    play = Play.query.first()
    assert play.correct_nums() == 1

def test_correct_nums_4(client, game1234, play1234):
    play = Play.query.first()
    assert play.correct_nums() == 4


def test_correct_nums_2(client, game1234, play2100):
    play = Play.query.first()
    assert play.correct_nums() == 2

def test_correct_nums_2b(client, game1234, play1200):
    play = Play.query.first()
    assert play.correct_nums() == 2

# correct pos
def test_correct_pos_0(client, game1234, play2100):
    play = Play.query.first()
    assert play.correct_pos() == 0

def test_correct_pos_1(client, game1234, play1111):
    play = Play.query.first()
    assert play.correct_pos() == 1

def test_correct_pos_2(client, game1234, play1200):
    play = Play.query.first()
    assert play.correct_pos() == 2


# win
def test_correct_pos_4(client, game1234, play1234):
    play = Play.query.first()
    assert play.correct_pos() == 4
    
def test_not_win_1234_1111(client, game1234, play1111):
    play = Play.query.first()
    assert not play.win()

def test_not_win_1234_2100(client, game1234, play2100):
    play = Play.query.first()
    assert not play.win()

def test_not_win_1234_1111(client, game1234, play1200):
    play = Play.query.first()
    assert not play.win()

def test_win(client, game1234, play1234):
    play = Play.query.first()
    assert play.win()
    