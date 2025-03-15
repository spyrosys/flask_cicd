import pytest
from app import app, db, Task

@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    with app.app_context():
        db.create_all()
    client = app.test_client()
    yield client
    with app.app_context():
        db.drop_all()

def test_create_task(client):
    response = client.post("/tasks", json={"title": "Test Task", "description": "Test Desc", "completed": False})
    assert response.status_code == 201
    assert response.json["message"] == "Task created"

def test_get_tasks(client):
    client.post("/tasks", json={"title": "Sample Task", "description": "Sample", "completed": False})
    response = client.get("/tasks")
    assert response.status_code == 200
    assert len(response.json) == 1

def test_update_task(client):
    client.post("/tasks", json={"title": "Sample Task", "description": "Sample", "completed": False})
    response = client.put("/tasks/1", json={"title": "Updated", "description": "Updated Desc", "completed": True})
    assert response.status_code == 200
    assert response.json["message"] == "Task updated"

def test_delete_task(client):
    client.post("/tasks", json={"title": "Delete Me", "description": "To be deleted", "completed": False})
    response = client.delete("/tasks/1")
    assert response.status_code == 200
    assert response.json["message"] == "Task deleted"

