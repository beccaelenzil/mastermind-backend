from app.models.play import Play


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
