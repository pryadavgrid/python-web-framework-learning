# Real Project Unit Testing Guide for Your FastAPI CRUD Project

This guide is based on your actual FastAPI CRUD application.

We will build:

* Proper pytest structure
* Real database testing
* API endpoint testing
* Service layer testing
* CRUD testing
* Dependency override
* Test fixtures
* Temporary test database
* Mock-style isolated testing
* Industry-level project structure

---

# 1. Why Your Current Test is NOT Enough

Your current test:

```python
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
```

This only checks:

* endpoint responds
* status code exists

But real companies test:

* database operations
* invalid data
* edge cases
* service logic
* CRUD logic
* failure handling
* response structure
* business rules

---

# 2. Real Testing Architecture

We will test your project in 3 layers.

```text
API Layer Tests
       ↓
Service Layer Tests
       ↓
CRUD Layer Tests
       ↓
Database
```

---

# 3. Final Recommended Project Structure

```text
01_fastapi-crud/
│
├── api/
├── crud/
├── services/
├── models/
├── db/
├── schemas/
│
├── tests/
│   ├── conftest.py
│   ├── test_users_api.py
│   ├── test_user_service.py
│   ├── test_user_crud.py
│
├── pytest.ini
├── requirements.txt
```

---

# 4. Install Testing Dependencies

Add this inside requirements.txt

```text
pytest
pytest-cov
httpx
```

Install:

```bash
pip install pytest pytest-cov httpx
```

---

# 5. Create pytest.ini

Create file:

```text
pytest.ini
```

Code:

```ini
[pytest]
pythonpath = .
testpaths = tests
```

## Why This is Important

### pythonpath = .

Allows pytest to import your app modules.

Without this:

```python
from main import app
```

may fail.

---

# 6. Most Important File → conftest.py

This is the heart of pytest setup.

Create:

```text
tests/conftest.py
```

Full Code:

```python
# tests/conftest.py

# pytest fixture library
import pytest

# FastAPI test client
from fastapi.testclient import TestClient

# SQLAlchemy imports
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Import your app
from main import app

# Import Base model
from db.base import Base

# Import dependency function
from api.deps import get_db


# -----------------------------
# TEST DATABASE
# -----------------------------

# SQLite test database
# This database is only for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"


# Create engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)


# Create session
TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# -----------------------------
# CREATE TEST DATABASE TABLES
# -----------------------------

# Create all tables before tests start
Base.metadata.create_all(bind=engine)


# -----------------------------
# DATABASE FIXTURE
# -----------------------------

@pytest.fixture()
def db():
    """
    Create a fresh database session
    for every test.
    """

    # create session
    db = TestingSessionLocal()

    try:
        yield db

    finally:
        db.close()


# -----------------------------
# OVERRIDE FASTAPI DATABASE
# -----------------------------

# Replace original database with test database

def override_get_db():
    db = TestingSessionLocal()

    try:
        yield db

    finally:
        db.close()


# Override dependency
app.dependency_overrides[get_db] = override_get_db


# -----------------------------
# TEST CLIENT FIXTURE
# -----------------------------

@pytest.fixture()
def client():
    """
    FastAPI test client fixture.
    """

    with TestClient(app) as c:
        yield c
```

---

# 7. Understanding conftest.py Deeply

This file is EXTREMELY IMPORTANT.

## What pytest does internally

```text
pytest starts
      ↓
reads conftest.py
      ↓
creates fixtures
      ↓
injects fixtures into tests
      ↓
runs tests
```

---

# 8. Why We Use Separate Test Database

NEVER use production DB in testing.

Bad:

```python
postgres://real-production-db
```

Why?

Because tests:

* create data
* delete data
* modify data

You can destroy production data accidentally.

---

# 9. API Testing

Create:

```text
tests/test_users_api.py
```

Full Code:

```python
# tests/test_users_api.py

# Test client fixture automatically comes from conftest.py


def test_create_user_success(client):
    """
    Test successful user creation.
    """

    # Send POST request
    response = client.post(
        "/api/v1/users/",
        json={
            "name": "Prateek",
            "email": "prateek@test.com"
        }
    )

    # Check status code
    assert response.status_code == 200

    # Convert response into JSON
    data = response.json()

    # Validate response data
    assert data["name"] == "Prateek"
    assert data["email"] == "prateek@test.com"



def test_create_user_invalid_email(client):
    """
    Test invalid email validation.
    """

    response = client.post(
        "/api/v1/users/",
        json={
            "name": "Prateek",
            "email": "invalid-email"
        }
    )

    # Service layer should reject invalid email
    assert response.status_code == 400

    data = response.json()

    assert data["detail"] == "Invalid email"



def test_get_all_users(client):
    """
    Test fetching all users.
    """

    response = client.get("/api/v1/users/")

    assert response.status_code == 200

    # Should return list
    assert isinstance(response.json(), list)



def test_get_single_user(client):
    """
    Test fetching one user.
    """

    # First create user
    create_response = client.post(
        "/api/v1/users/",
        json={
            "name": "John",
            "email": "john@test.com"
        }
    )

    user_id = create_response.json()["id"]

    # Fetch same user
    response = client.get(f"/api/v1/users/{user_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == user_id
    assert data["name"] == "John"



def test_update_user(client):
    """
    Test updating user.
    """

    # Create user first
    create_response = client.post(
        "/api/v1/users/",
        json={
            "name": "Old Name",
            "email": "old@test.com"
        }
    )

    user_id = create_response.json()["id"]

    # Update user
    response = client.put(
        f"/api/v1/users/{user_id}",
        json={
            "name": "New Name",
            "email": "new@test.com"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "New Name"
    assert data["email"] == "new@test.com"



def test_delete_user(client):
    """
    Test deleting user.
    """

    # Create user
    create_response = client.post(
        "/api/v1/users/",
        json={
            "name": "Delete Me",
            "email": "delete@test.com"
        }
    )

    user_id = create_response.json()["id"]

    # Delete user
    response = client.delete(f"/api/v1/users/{user_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "User deleted successfully"
```

---

# 10. What You Learned From API Testing

You learned:

* endpoint testing
* request testing
* response testing
* validation testing
* CRUD flow testing
* status code testing
* JSON validation

This is REAL industry-level testing.

---

# 11. Service Layer Testing

Now we test ONLY business logic.

This is actual UNIT TESTING.

Create:

```text
tests/test_user_service.py
```

Code:

```python
# tests/test_user_service.py

import pytest

from fastapi import HTTPException

from services.user_service import (
    create_user_service,
    update_user_service,
    delete_user_service
)

from crud.user import create_user



def test_create_user_service_success(db):
    """
    Test service creates user successfully.
    """

    user = create_user_service(
        db,
        name="Prateek",
        email="prateek@test.com"
    )

    assert user.name == "Prateek"
    assert user.email == "prateek@test.com"



def test_create_user_service_invalid_email(db):
    """
    Service should raise exception
    for invalid email.
    """

    with pytest.raises(HTTPException) as exc:

        create_user_service(
            db,
            name="Prateek",
            email="wrong-email"
        )

    assert exc.value.status_code == 400
    assert exc.value.detail == "Invalid email"



def test_update_user_not_found(db):
    """
    Test updating non-existing user.
    """

    with pytest.raises(HTTPException) as exc:

        update_user_service(
            db,
            user_id=999,
            name="New Name"
        )

    assert exc.value.status_code == 404
    assert exc.value.detail == "User not found"



def test_delete_user_not_found(db):
    """
    Test deleting non-existing user.
    """

    with pytest.raises(HTTPException) as exc:

        delete_user_service(db, user_id=999)

    assert exc.value.status_code == 404
```

---

# 12. Why Service Testing is IMPORTANT

Service layer contains:

* business logic
* validations
* rules
* workflows
* conditions

This is MOST important layer in real backend systems.

---

# 13. CRUD Layer Testing

Now test direct database operations.

Create:

```text
tests/test_user_crud.py
```

Code:

```python
# tests/test_user_crud.py

from crud.user import (
    create_user,
    get_users,
    get_user_by_id,
    update_user,
    delete_user
)



def test_create_user(db):
    """
    Test direct database user creation.
    """

    user = create_user(
        db,
        name="Database User",
        email="db@test.com"
    )

    assert user.id is not None
    assert user.name == "Database User"



def test_get_users(db):
    """
    Test fetching all users.
    """

    create_user(db, "User1", "user1@test.com")
    create_user(db, "User2", "user2@test.com")

    users = get_users(db)

    assert len(users) >= 2



def test_get_user_by_id(db):
    """
    Test fetching user by ID.
    """

    user = create_user(
        db,
        name="Find Me",
        email="find@test.com"
    )

    found_user = get_user_by_id(db, user.id)

    assert found_user.id == user.id
    assert found_user.name == "Find Me"



def test_update_user(db):
    """
    Test database update operation.
    """

    user = create_user(
        db,
        name="Old",
        email="old@test.com"
    )

    updated_user = update_user(
        db,
        user.id,
        name="Updated"
    )

    assert updated_user.name == "Updated"



def test_delete_user(db):
    """
    Test deleting user.
    """

    user = create_user(
        db,
        name="Delete",
        email="delete@test.com"
    )

    deleted_user = delete_user(db, user.id)

    assert deleted_user.id == user.id

    # Verify user is removed
    user_check = get_user_by_id(db, user.id)

    assert user_check is None
```

---

# 14. How pytest Fixtures Work Internally

Example:

```python
def test_create_user(db):
```

Pytest sees:

```python
db
```

Then automatically searches fixture:

```python
@pytest.fixture()
def db():
```

Then injects database object.

This is called:

# Dependency Injection

Very important concept.

---

# 15. Test Execution Flow

Actual pytest workflow:

```text
pytest starts
     ↓
finds test files
     ↓
imports conftest.py
     ↓
creates fixtures
     ↓
runs test function
     ↓
injects db/client fixture
     ↓
executes assertions
     ↓
shows pass/fail report
```

---

# 16. Run Tests

Run all:

```bash
pytest
```

Verbose:

```bash
pytest -v
```

Coverage:

```bash
pytest --cov=.
```

---

# 17. Example Real Output

```text
=================== test session starts ===================

collected 10 items

tests/test_users_api.py .....
tests/test_user_service.py ...
tests/test_user_crud.py ..

=================== 10 passed ===================
```

---

# 18. Mentor-Level Explanation

If mentor asks:

## Why use conftest.py?

Answer:

```text
conftest.py is used to store reusable fixtures and common test setup.
pytest automatically discovers it and injects fixtures into tests.
```

---

## Why override dependency?

Answer:

```text
We override FastAPI database dependency so tests use isolated test database instead of production database.
```

---

## Why fixtures?

Answer:

```text
Fixtures provide reusable setup and cleanup logic.
They reduce duplicate code and improve maintainability.
```

---

## Why separate test database?

Answer:

```text
Tests should never affect production data.
Separate DB ensures isolation and reliability.
```

---

## What is unit testing?

Answer:

```text
Unit testing verifies smallest isolated units of code like functions or services.
```

---

## Difference between API test and Unit test?

Answer:

```text
API tests verify endpoints and HTTP responses.
Unit tests verify isolated business logic.
```

---

# 19. Advanced Improvement (Industry Level)

Later you can add:

* pytest-mock
* async testing
* GitHub Actions
* Docker test pipeline
* coverage reports
* in-memory database
* factory pattern
* faker data generation
* integration testing

---

# 20. Most Important Learning

Testing is NOT only:

```python
assert status_code == 200
```

Real testing means:

* verify business logic
* verify validation
* verify edge cases
* verify failure handling
* verify database operations
* verify API contracts
* verify system reliability

---

# 21. Final Understanding

Your project now demonstrates:

* FastAPI testing
* pytest mastery
* fixture usage
* dependency injection
* database testing
* CRUD testing
* service testing
* API testing
* industry project structure
* backend testing workflow

This is strong enough to explain confidently to:

* mentors
* interviewers
* internship reviewers
* backend teams
