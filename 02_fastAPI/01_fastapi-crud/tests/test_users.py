def test_root_returns_dashboard_page(client):
    response = client.get("/")

    assert response.status_code == 200
    assert "FastAPI Dashboard" in response.text


def test_create_user_endpoint_returns_created_user(client):
    response = client.post(
        "/users/",
        json={"name": "John", "email": "john@test.com"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["id"] is not None
    assert data["name"] == "John"
    assert data["email"] == "john@test.com"


def test_create_user_endpoint_rejects_invalid_email(client):
    response = client.post(
        "/users/",
        json={"name": "Invalid", "email": "invalid-email"},
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid email"}


def test_read_users_endpoint_returns_created_users(client):
    client.post("/users/", json={"name": "Alice", "email": "alice@test.com"})
    client.post("/users/", json={"name": "Bob", "email": "bob@test.com"})

    response = client.get("/users/")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert {user["email"] for user in data} == {"alice@test.com", "bob@test.com"}


def test_read_user_endpoint_returns_single_user(client):
    created = client.post(
        "/users/",
        json={"name": "Single", "email": "single@test.com"},
    ).json()

    response = client.get(f"/users/{created['id']}")

    assert response.status_code == 200
    assert response.json() == created


def test_update_user_endpoint_changes_user(client):
    created = client.post(
        "/users/",
        json={"name": "Old", "email": "old@test.com"},
    ).json()

    response = client.put(
        f"/users/{created['id']}",
        json={"name": "Updated", "email": "updated@test.com"},
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Updated"
    assert response.json()["email"] == "updated@test.com"


def test_update_user_endpoint_returns_404_for_missing_user(client):
    response = client.put(
        "/users/999",
        json={"name": "Missing", "email": "missing@test.com"},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}


def test_delete_user_endpoint_deletes_user(client):
    created = client.post(
        "/users/",
        json={"name": "Delete", "email": "delete@test.com"},
    ).json()

    response = client.delete(f"/users/{created['id']}")

    assert response.status_code == 200
    assert response.json() == {"message": "User deleted successfully"}


def test_delete_user_endpoint_returns_404_for_missing_user(client):
    response = client.delete("/users/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}
