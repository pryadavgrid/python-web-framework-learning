from sqlalchemy.orm import Session
from fastapi import HTTPException

from crud.user import create_user, update_user, delete_user


def create_user_service(db: Session, name: str, email: str):
    if "@" not in email:
        raise HTTPException(status_code=400, detail="Invalid email")

    return create_user(db, name, email)


def update_user_service(db: Session, user_id: int, name: str = None, email: str = None):
    user = update_user(db, user_id, name, email)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


def delete_user_service(db: Session, user_id: int):
    user = delete_user(db, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {"message": "User deleted successfully"}