# tests/test_tasks.py

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def get_token():

    response = client.post(
        "/login",
        json={
            "username": "testuser",
            "password": "testpass"
        }
    )

    token = response.json()["access_token"]

    return token


def test_create_task():

    token = get_token()

    response = client.post(
        "/tasks",
        json={
            "title": "Finish backend project"
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200


def test_get_tasks():

    token = get_token()

    response = client.get(
        "/tasks",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200


def test_delete_task():

    token = get_token()

    create = client.post(
        "/tasks",
        json={
            "title": "Task to delete"
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    task_id = create.json()["id"]

    response = client.delete(
        f"/tasks/{task_id}",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200