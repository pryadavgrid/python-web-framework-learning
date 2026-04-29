from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200

def test_create_user():
    response = client.post(
        "/api/v1/users/",
        json={"name": "John", "email": "john@test.com"}
    )
    assert response.status_code == 200