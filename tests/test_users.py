# tests/test_users.py

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_register_user():
    response = client.post(
        "/register",
        json={
            "username": "testuser",
            "password": "testpass"
        }
    )

    assert response.status_code == 200
    data = response.json()

    assert data["username"] == "testuser"


def test_login_user():

    response = client.post(
        "/login",
        json={
            "username": "testuser",
            "password": "testpass"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data