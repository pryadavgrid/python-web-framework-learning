from crud.user import (
    create_user,
    delete_user,
    get_user_by_id,
    get_users,
    update_user,
)


def test_create_user_persists_user(db):
    user = create_user(db, name="Database User", email="db@test.com")

    assert user.id is not None
    assert user.name == "Database User"
    assert user.email == "db@test.com"


def test_get_users_returns_all_users(db):
    create_user(db, name="User One", email="one@test.com")
    create_user(db, name="User Two", email="two@test.com")

    users = get_users(db)

    assert len(users) == 2
    assert {user.email for user in users} == {"one@test.com", "two@test.com"}


def test_get_user_by_id_returns_matching_user(db):
    user = create_user(db, name="Find Me", email="find@test.com")

    found_user = get_user_by_id(db, user.id)

    assert found_user is not None
    assert found_user.id == user.id
    assert found_user.name == "Find Me"


def test_get_user_by_id_returns_none_for_missing_user(db):
    assert get_user_by_id(db, 999) is None


def test_update_user_changes_only_passed_fields(db):
    user = create_user(db, name="Old Name", email="old@test.com")

    updated_user = update_user(db, user.id, name="New Name")

    assert updated_user.name == "New Name"
    assert updated_user.email == "old@test.com"


def test_update_user_returns_none_for_missing_user(db):
    assert update_user(db, 999, name="Nobody") is None


def test_delete_user_removes_user(db):
    user = create_user(db, name="Delete Me", email="delete@test.com")

    deleted_user = delete_user(db, user.id)

    assert deleted_user.id == user.id
    assert get_user_by_id(db, user.id) is None


def test_delete_user_returns_none_for_missing_user(db):
    assert delete_user(db, 999) is None
