def test_create_item_endpoint_returns_created_item(client):
    response = client.post(
        "/items/",
        json={"item_name": "Laptop", "item_detail": "16GB RAM"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["id"] is not None
    assert data["item_name"] == "Laptop"
    assert data["item_detail"] == "16GB RAM"


def test_read_items_endpoint_returns_created_items(client):
    client.post("/items/", json={"item_name": "Mouse", "item_detail": "Wireless"})
    client.post("/items/", json={"item_name": "Keyboard", "item_detail": "Mechanical"})

    response = client.get("/items/")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert {item["item_name"] for item in data} == {"Mouse", "Keyboard"}


def test_item_update_route_is_not_registered(client):
    response = client.put(
        "/items/1",
        json={"item_name": "Updated", "item_detail": "Changed"},
    )

    assert response.status_code == 404


def test_item_delete_route_is_not_registered(client):
    response = client.delete("/items/1")

    assert response.status_code == 404
