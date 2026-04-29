from sqlalchemy.orm import Session
from models.user import User

# CREATE
def create_user(db: Session, name: str, email: str):
    user = User(name=name, email=email)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


# READ ALL
def get_users(db: Session):
    return db.query(User).all()


# READ ONE
def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


# UPDATE
def update_user(db: Session, user_id: int, name: str = None, email: str = None):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        return None

    if name is not None:
        user.name = name

    if email is not None:
        user.email = email

    db.commit()
    db.refresh(user)
    return user


# DELETE
def delete_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        return None

    db.delete(user)
    db.commit()
    return user