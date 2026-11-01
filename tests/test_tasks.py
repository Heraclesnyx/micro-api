from fastapi.testclient import TestClient
import pytest

import main
from main import app

client = TestClient(app)

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

def test_post_task_without_title_returns_422():
    response = client.post("/tasks", json={})
    assert response.status_code == 422

def test_get_tasks_returns_empty_list():
    response = client.get("/tasks")

    assert response.status_code == 200
    assert response.json() == []

def test_get_tasks_returns_created_task():
    client.post("/tasks", json={"title": "Ma première tâche"})

    response = client.get("/tasks")

    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 1,
            "title": "Ma première tâche",
            "done": False
        }
    ]

def test_get_task_with_valid_id_return_task():
    created_task =client.post("/tasks", json={"title": "Ma première tâche"})
    task_id = created_task.json()["id"]

    response = client.get(f"/tasks/{task_id}")

    assert response.status_code == 200
    assert response.json() == {
        "id": task_id,
        "title": "Ma première tâche",
        "done": False
    }

def test_put_task_with_valid_id_updates_task():

    # Création d'une 1ère tache
    created_task =client.post("/tasks", json={"title": "Ma première tâche", "done": False})
    
    # Récupération de son id
    task_id = created_task.json()["id"]

    # Modification du titre et de l'état
    response = client.put(f"/tasks/{task_id}", json={"title": "Ma deuxième tâche","done": True})

    # Vérification du résultat
    assert response.status_code == 200
    assert response.json() == {
        "id": task_id,
        "title": "Ma deuxième tâche",
        "done": True
    }


def test_put_task_with_unknown_id_returns_404():
    response = client.put("/tasks/99", json={"title": "Ma deuxième tâche", "done": False})
    assert response.status_code == 404


def test_delete_task_with_valid_id_return_204():
    # Création d'une tache
    created_task =client.post("/tasks", json={"title": "Ma première tâche"})
    task_id = created_task.json()["id"]

    # Suppression de la tâche
    response = client.delete(f"/tasks/{task_id}")

    # Vérification de la suppression
    assert response.status_code == 204

    # Vérification que la tâche n'existe plus
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 404


def test_delete_task_with_unknown_id_returns_404(db_session):
    response = client.delete("/tasks/99")
    assert response.status_code == 404