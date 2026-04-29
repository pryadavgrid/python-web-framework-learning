from sqlalchemy.orm import Session
from models.items import Items

# CREATE
def create_items(db: Session, item_name: str, item_detail : str):
    item = Items(item_name=item_name, item_detail=item_detail)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


# READ ALL
def get_items(db: Session):
    return db.query(Items).all()


# READ ONE
def get_item_by_id(db: Session, item_id: int):
    return db.query(Items).filter(Items.id == item_id).first()


# UPDATE
def update_items(db: Session, item_id: int, item_name: str = None, item_detail: str = None):
    item = db.query(Items).filter(Items.id == item_id).first()

    if not item:
        return None

    if item_name is not None:
        item.item_name = item_name

    if item_detail is not None:
        item.item_detail = item_detail

    db.commit()
    db.refresh(item)
    return item


# DELETE
def delete_items(db: Session, user_id: int):
    item = db.query(Items).filter(Items.id == user_id).first()

    if not item:
        return None

    db.delete(item)
    db.commit()
    return item