from app.models.user import User


def test_existing_user(client, user1):
    # Act
    response = client.post(
        "/users/login", json={"email": "becca"})

    assert response.status_code == 200
    response_body = response.get_json()
    response_body["email"] = "becca"


def test_new_user(client):
    # Act
    response = client.post(
        "/users/login", json={"email": "becca"})

    assert response.status_code == 201
    response_body = response.get_json()
    response_body["email"] = "becca"

    users = User.query.all()
    assert len(users) == 1
    assert users[0].email == "becca"


def test_no_request_body(client):
    # Act
    response = client.post(
        "/users/login", json={"nothing": "nothing"})

    assert response.status_code == 400


def test_user_not_found(client):
    # Act
    response = client.get(f"/users/1")

    # Assert
    response.status_code == 404


def test_get_all_users_no_users(client):
    # Act
    response = client.get(f"/users/")

    # Assert
    assert response.status_code == 200
    response_body = response.get_json()
    assert len(response_body) == 0


def test_get_all_users_2_users(client, users2):
    # Act
    response = client.get(f"/users/")

    # Assert
    assert response.status_code == 200
    response_body = response.get_json()
    assert len(response_body) == 2

    users = User.query.all()
    assert len(users) == 2


def test_win_2_lose_1(client, user_win_2_lose_1):
    users = User.query.all()
    user = users[0]

    # Act
    response = client.get(f"/users/{user.uid}")
    response.status_code == 200

    response_body = response.get_json()
    summary = response_body["performance summary"]

    assert summary["Games won"] == 2
    assert summary["Win Streak"] == 2
    assert summary["Total games"] == 3
    assert summary["Win %"] == 66.67
    assert response_body["email"] == user.email
    assert len(response_body["games"]) == 3


def test_user_no_games(client, users2):
    users = User.query.all()
    user = users[0]

    # Act
    response = client.get(f"/users/{user.uid}")
    response.status_code == 200

    response_body = response.get_json()
    summary = response_body["performance summary"]

    assert summary["Games won"] == 0
    assert summary["Win Streak"] == 0
    assert summary["Total games"] == 0
    assert summary["Win %"] == 0
    assert response_body["email"] == user.email
    assert len(response_body["games"]) == 0
