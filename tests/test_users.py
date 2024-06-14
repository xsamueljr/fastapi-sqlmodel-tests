from enum import Enum

from fastapi.testclient import TestClient
from sqlmodel import Session, select

from db.models.user import User


class Endpoints(Enum):
    base = "/users"
    signup = f"{base}/signup"
    login = f"{base}/login"


GOOD_USERS: list[dict] = [
    {
        "email": "user1@example.com",
        "username": "imamazing",
        "password": "asecurepassword",
    },
    {
        "email": "user2@example.com",
        "username": "imsocool",
        "password": "youknowthat",
    },
    {
        "email": "user3@example.com",
        "username": "youarealsocool",
        "password": "imsureaboutit",
    },
]


def test_good_users_works():
    for user in GOOD_USERS:
        _ = User(**user)


def test_signup(client: TestClient, session: Session):
    response = client.post(
        Endpoints.signup.value,
        json={
            "username": "XXXX",
            "email": "user@example.com",
            "password": "XXXXXXXX",
        },
    )
    users_in_db = session.exec(select(User)).all()
    data: dict = response.json()
    assert response.status_code == 201, response.text
    assert len(users_in_db) == 1
    assert data["username"] == "XXXX"
    assert users_in_db[0].id == data["id"]
    assert users_in_db[0].username == "XXXX"


def test_cannot_signup_the_same_user_twice(client: TestClient, session: Session):
    payload = {
        "username": "XXXX",
        "email": "user@example.com",
        "password": "XXXXXXXX",
    }

    first_response = client.post(Endpoints.signup.value, json=payload)
    second_response = client.post(Endpoints.signup.value, json=payload)
    
    users_in_db = session.exec(
        select(User).where(User.username == "XXXX")).all()

    assert first_response.status_code == 201, first_response.text
    assert second_response.status_code == 409, second_response.text
    assert len(users_in_db) == 1


def test_two_users_cannot_have_the_same_email(client: TestClient, session: Session):
    payload = GOOD_USERS[0]

    first_response = client.post(Endpoints.signup.value, json=payload)
    second_payload = GOOD_USERS[0]
    second_payload["username"] = "anotheruser"
    second_response = client.post(Endpoints.signup.value, json=second_payload)

    users_in_db = session.exec(select(User)).all()

    assert first_response.status_code == 201, first_response.text
    assert second_response.status_code == 409, second_response.text
    assert len(users_in_db) == 1


def test_cannot_signup_with_invalid_payload(client: TestClient):
    response = client.post(Endpoints.signup.value, json={})
    assert response.status_code == 422, response.text


def test_login(client: TestClient, session: Session):
    user = GOOD_USERS[0]

    response = client.post(Endpoints.signup.value, json=user)
    assert response.status_code == 201, response.text

    response = client.post(
        Endpoints.login.value,
        json={
            "username": user["username"],
            "password": user["password"],
        },
    )

    assert response.status_code == 200, response.text


def test_cannot_login_without_signing_up(client: TestClient):
    response = client.post(
        Endpoints.login.value,
        json=GOOD_USERS[0],
    )

    assert response.status_code == 404, response.text