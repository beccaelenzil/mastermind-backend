from app.models.user import User


def test_existing_user(client, user1):
    # Act
    response = client.post(
        "/users/login", json={"username": "becca"})

    assert response.status_code == 200
    response_body = response.get_json()
    response_body["username"] = "becca"


def test_new_user(client):
    # Act
    response = client.post(
        "/users/login", json={"username": "becca"})

    assert response.status_code == 201
    response_body = response.get_json()
    response_body["username"] = "becca"

    users = User.query.all()
    assert len(users) == 1
    assert users[0].username == "becca"


def test_no_request_body(client):
    # Act
    response = client.post(
        "/users/login", json={"nothing": "nothing"})

    assert response.status_code == 400
