from fastapi.testclient import TestClient
import main

client = TestClient(app)

def test_get_users():
    response = client.get("/api/users")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_user():
    response = client.get("/api/users/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1