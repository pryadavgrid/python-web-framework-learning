import pytest
from fastapi import HTTPException

from crud.user import create_user, get_user_by_id
from services.user_service import (
    create_user_service,
    delete_user_service,
    update_user_service,
)


def test_create_user_service_accepts_valid_email(db):
    user = create_user_service(db, name="Service User", email="service@test.com")

    assert user.id is not None
    assert user.name == "Service User"
    assert user.email == "service@test.com"


def test_create_user_service_rejects_invalid_email(db):
    with pytest.raises(HTTPException) as exc_info:
        create_user_service(db, name="Bad Email", email="invalid-email")

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Invalid email"


def test_update_user_service_updates_existing_user(db):
    user = create_user(db, name="Before", email="before@test.com")

    updated_user = update_user_service(
        db,
        user.id,
        name="After",
        email="after@test.com",
    )

    assert updated_user.id == user.id
    assert updated_user.name == "After"
    assert updated_user.email == "after@test.com"


def test_update_user_service_raises_404_for_missing_user(db):
    with pytest.raises(HTTPException) as exc_info:
        update_user_service(db, 999, name="Missing")

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "User not found"


def test_delete_user_service_removes_existing_user(db):
    user = create_user(db, name="Delete Service", email="delete.service@test.com")

    result = delete_user_service(db, user.id)

    assert result == {"message": "User deleted successfully"}
    assert get_user_by_id(db, user.id) is None


def test_delete_user_service_raises_404_for_missing_user(db):
    with pytest.raises(HTTPException) as exc_info:
        delete_user_service(db, 999)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "User not found"
