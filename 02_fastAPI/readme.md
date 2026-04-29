# 🚀 FastAPI 

**FastAPI** is a modern, high-performance Python web framework used to build APIs quickly and efficiently. It is built on top of Starlette (for web handling) and Pydantic (for data validation).

### 🔥 Why FastAPI?

* ⚡ **Fast** – One of the fastest Python frameworks
* 🧠 **Easy to use** – Uses Python type hints (clean & readable)
* 📄 **Auto Documentation** – Swagger UI (`/docs`) generated automatically
* ✅ **Validation** – Built-in request validation using Pydantic
* 🔄 **Async Support** – Handles high concurrency with async/await
* 🔐 **Security Ready** – Supports OAuth2, JWT, etc.

### ⚙️ Important Functionalities

* Request & response validation
* Dependency Injection system
* Middleware support
* Background tasks
* Authentication & authorization
* API versioning (like `/api/v1/`)

---

# 📁 FastAPI File Structure

```
fastapi_project/
│
├── app/
│   ├── main.py
│   ├── core/
│   │   ├── config.py
│   │   ├── security.py
│   │
│   ├── api/
│   │   ├── deps.py
│   │   ├── v1/
│   │       ├── endpoints/
│   │       │   ├── users.py
│   │       │   ├── items.py
│   │       ├── router.py
│   │
│   ├── models/
│   │   ├── user.py
│   │   ├── item.py
│   │
│   ├── schemas/
│   │   ├── user.py
│   │   ├── item.py
│   │
│   ├── crud/
│   │   ├── user.py
│   │   ├── item.py
│   │
│   ├── db/
│   │   ├── base.py
│   │   ├── session.py
│   │
│   ├── services/
│   │   ├── user_service.py
│   │
│   └── utils/
│       ├── helpers.py
│
├── tests/
│   ├── test_users.py
│
├── requirements.txt
├── .env
└── alembic/   (for migrations)
```

---

# 🔗 How Everything Connects (Big Picture)

Think of the flow like this:

```
Client Request → API Endpoint → Service/CRUD → DB → Response Schema → Client
```

---

# 📂 Folder-by-Folder Explanation

## 1. `main.py` (Entry Point)

* This is where your FastAPI app starts.
* Creates the app instance and includes routers.

```python
from fastapi import FastAPI
from app.api.v1.router import api_router

app = FastAPI()
app.include_router(api_router, prefix="/api/v1")
```

👉 It connects all routes into one application.

---

## 2. `core/` (Configuration & Security)

Handles global settings.

### `config.py`

* Loads environment variables (from `.env`)
* Stores settings like DB URL, secret keys

### `security.py`

* Authentication logic (JWT, password hashing)

👉 Used across the entire project.

---

## 3. `api/` (Routing Layer)

### `deps.py`

* Shared dependencies (e.g., DB session, auth)

### `v1/endpoints/`

* Contains route files (like controllers)

Example:

```python
@router.get("/users")
def get_users():
    ...
```

### `router.py`

* Combines all endpoint routes

```python
from fastapi import APIRouter
from app.api.v1.endpoints import users

api_router = APIRouter()
api_router.include_router(users.router, prefix="/users")
```

👉 This layer receives HTTP requests.

---

## 4. `models/` (Database Models)

* Defines database tables using ORM (usually SQLAlchemy)

```python
class User(Base):
    id = Column(Integer, primary_key=True)
```

👉 Directly maps to database tables.

---

## 5. `schemas/` (Pydantic Models)

* Defines request & response formats

```python
class UserCreate(BaseModel):
    name: str
```

👉 Ensures data validation and serialization.

---

## 6. `crud/` (Database Operations)

* Handles direct DB queries (Create, Read, Update, Delete)

```python
def get_user(db, user_id):
    return db.query(User).filter(User.id == user_id).first()
```

👉 Keeps DB logic separate from routes.

---

## 7. `db/` (Database Connection)

### `session.py`

* Creates DB session

### `base.py`

* Imports all models (needed for migrations)

👉 This is the bridge to your database.

---

## 8. `services/` (Business Logic Layer)

* Contains complex logic (not just DB queries)

Example:

```python
def create_user_service():
    # validation + business rules + DB call
```

👉 Separates logic from endpoints and CRUD.

---

## 9. `utils/` (Helper Functions)

* Common reusable utilities

Examples:

* Date formatting
* File handling

---

## 10. `tests/`

* Unit & integration tests using `pytest`

---

## 11. `alembic/` (Migrations)

* Handles database schema changes

👉 Works with SQLAlchemy models.

---

## 🔄 Full Request Flow Example

Let’s say a user hits:

```
GET /api/v1/users
```

### Flow:

1. Request → `main.py`
2. Routed → `api/v1/router.py`
3. Endpoint → `endpoints/users.py`
4. Calls → `crud/user.py` or `services/user_service.py`
5. Queries DB → via `db/session.py`
6. Data → Returned as `schemas/user.py`
7. Response → Sent back to client

---

# 🧠 Key Design Principles

* **Separation of Concerns**
* **Scalability**
* **Reusability**
* **Testability**

---

# 🛠️ Setup & Run the Project

## 1. Clone the Repository

```bash
git clone https://github.com/pryadavgrid/python-web-framework-learning.git
cd python-web-framework-learning/02_fastAPI
```

---

## 2. Create Virtual Environment

### Linux / Mac

```bash
python3 -m venv venv
source venv/bin/activate
```

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Run the Application

```bash
uvicorn app.main:app --reload
```

---

## 5. Open in Browser

* Swagger UI: http://127.0.0.1:8000/docs
* ReDoc: http://127.0.0.1:8000/redoc

---
