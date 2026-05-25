from crud.items import (
    create_items,
    delete_items,
    get_item_by_id,
    get_items,
    update_items,
)


def test_create_item_persists_item(db):
    item = create_items(db, item_name="Laptop", item_detail="16GB RAM")

    assert item.id is not None
    assert item.item_name == "Laptop"
    assert item.item_detail == "16GB RAM"


def test_get_items_returns_all_items(db):
    create_items(db, item_name="Mouse", item_detail="Wireless")
    create_items(db, item_name="Keyboard", item_detail="Mechanical")

    items = get_items(db)

    assert len(items) == 2
    assert {item.item_name for item in items} == {"Mouse", "Keyboard"}


def test_get_item_by_id_returns_matching_item(db):
    item = create_items(db, item_name="Monitor", item_detail="4K")

    found_item = get_item_by_id(db, item.id)

    assert found_item is not None
    assert found_item.id == item.id
    assert found_item.item_detail == "4K"


def test_get_item_by_id_returns_none_for_missing_item(db):
    assert get_item_by_id(db, 999) is None


def test_update_items_changes_only_passed_fields(db):
    item = create_items(db, item_name="Old Item", item_detail="Original detail")

    updated_item = update_items(db, item.id, item_name="New Item")

    assert updated_item.item_name == "New Item"
    assert updated_item.item_detail == "Original detail"


def test_update_items_returns_none_for_missing_item(db):
    assert update_items(db, 999, item_name="Missing") is None


def test_delete_items_removes_item(db):
    item = create_items(db, item_name="Delete Item", item_detail="Temporary")

    deleted_item = delete_items(db, item.id)

    assert deleted_item.id == item.id
    assert get_item_by_id(db, item.id) is None


def test_delete_items_returns_none_for_missing_item(db):
    assert delete_items(db, 999) is None
