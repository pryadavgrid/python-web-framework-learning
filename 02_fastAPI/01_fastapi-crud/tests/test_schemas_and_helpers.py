from schemas.items import ItemCreate, ItemResponse
from schemas.user import UserCreate, UserResponse
from utils.helpers import format_name


def test_user_create_schema_stores_name_and_email():
    user = UserCreate(name="Jane", email="jane@test.com")

    assert user.name == "Jane"
    assert user.email == "jane@test.com"


def test_user_response_schema_reads_from_object_attributes():
    user = type("UserObject", (), {"id": 1, "name": "Jane", "email": "jane@test.com"})()

    response = UserResponse.model_validate(user)

    assert response.model_dump() == {
        "id": 1,
        "name": "Jane",
        "email": "jane@test.com",
    }


def test_item_create_schema_stores_item_fields():
    item = ItemCreate(item_name="Book", item_detail="Python")

    assert item.item_name == "Book"
    assert item.item_detail == "Python"


def test_item_response_schema_reads_from_object_attributes():
    item = type(
        "ItemObject",
        (),
        {"id": 1, "item_name": "Book", "item_detail": "Python"},
    )()

    response = ItemResponse.model_validate(item)

    assert response.model_dump() == {
        "id": 1,
        "item_name": "Book",
        "item_detail": "Python",
    }


def test_format_name_strips_spaces_and_title_cases():
    assert format_name("  john doe  ") == "John Doe"
