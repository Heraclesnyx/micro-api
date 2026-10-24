from fastapi.testclient import TestClient
import pytest

import main
from main import app

client = TestClient(app)

@pytest.fixture(autouse=True)
def reset_tasks():
    main.tasks = []
    main.next_id = 1


def test_health_return_ok():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}



def test_get_task_with_unknown_id_returns_404():
    response = client.get("/tasks/99")
    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}


def test_post_task_with_valid_title_returns_201():
    response = client.post("/tasks", json={"title": "Hello"})
    assert response.status_code == 201  
    assert response.json() == {"id": 1, "title": "Hello", "done": False}
