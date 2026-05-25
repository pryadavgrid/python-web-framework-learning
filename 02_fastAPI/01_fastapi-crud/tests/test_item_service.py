import pytest
from fastapi import HTTPException

from crud.items import create_items, get_item_by_id
from services.item_service import (
    create_items_service,
    delete_item_service,
    update_items_service,
)


def test_create_items_service_creates_item(db):
    item = create_items_service(db, item_name="Notebook", item_detail="Ruled")

    assert item.id is not None
    assert item.item_name == "Notebook"
    assert item.item_detail == "Ruled"


def test_update_items_service_updates_existing_item(db):
    item = create_items(db, item_name="Pen", item_detail="Blue")

    updated_item = update_items_service(
        db,
        item.id,
        item_name="Gel Pen",
        item_detail="Black",
    )

    assert updated_item.id == item.id
    assert updated_item.item_name == "Gel Pen"
    assert updated_item.item_detail == "Black"


def test_update_items_service_raises_404_for_missing_item(db):
    with pytest.raises(HTTPException) as exc_info:
        update_items_service(db, 999, item_name="Missing")

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "User not found"


def test_delete_item_service_removes_existing_item(db):
    item = create_items(db, item_name="Eraser", item_detail="Small")

    result = delete_item_service(db, item.id)

    assert result == {"message": "User deleted successfully"}
    assert get_item_by_id(db, item.id) is None


def test_delete_item_service_raises_404_for_missing_item(db):
    with pytest.raises(HTTPException) as exc_info:
        delete_item_service(db, 999)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "User not found"
